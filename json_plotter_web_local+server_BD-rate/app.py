from flask import Flask, render_template, request, jsonify, session
import os
import json
import re
from werkzeug.utils import secure_filename 
import shutil # For clearing session upload directories
import uuid   # For unique session upload subdirectories

app = Flask(__name__)
app.secret_key = "FINAL_PLOTTER_APP_!@#$_VERY_STRONG_KEY_!@#$_SESSION_FIX"

# --- Configuration ---
# CRITICAL: These MUST be ABSOLUTE PATHS on your actual remote server.
# Example: BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS = "/srv/data_projects/json_collections"
# Example: DEFAULT_BASE_JSON_DIRECTORY = "/srv/data_projects/json_collections/default_exp_data"

BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS = os.path.abspath(
    os.getenv("PLOTTER_BROWSE_ROOT", "/work/Users/zhuzhiwei/project/3dRecon/compress/zju_gsc/GSCodec_Studio/examples/results") 
)
DEFAULT_BASE_JSON_DIRECTORY = os.path.abspath(
    os.getenv("PLOTTER_DEFAULT_JSON_DIR", "/work/Users/zhuzhiwei/project/3dRecon/compress/GSCodec_Studio/examples/results/gsc_compression_bartender")
)
DEFAULT_FILENAME_REGEX = r'.*rp_summary\.json$'
REMOTE_UPLOAD_STORAGE_ROOT = os.path.join(app.root_path, "user_plotter_uploads") 

print(f"INFO: Plotter App Initialized.")
print(f"INFO: BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS (abs path): {BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS}")
print(f"INFO: DEFAULT_BASE_JSON_DIRECTORY (abs path): {DEFAULT_BASE_JSON_DIRECTORY}")
print(f"INFO: REMOTE_UPLOAD_STORAGE_ROOT (abs path for session uploads): {REMOTE_UPLOAD_STORAGE_ROOT}")
print(f"INFO: Default Filename Regex: {DEFAULT_FILENAME_REGEX}")
print(f"INFO: App root_path: {app.root_path}") # For verifying relative paths

def setup_initial_directories():
    paths = [BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS, DEFAULT_BASE_JSON_DIRECTORY, REMOTE_UPLOAD_STORAGE_ROOT]
    for p in paths:
        if not os.path.exists(p):
            try: os.makedirs(p, exist_ok=True); print(f"INFO: Created dir: '{p}'")
            except OSError as e: print(f"FATAL ERROR creating dir '{p}': {e}. Create manually.")
        elif not os.path.isdir(p): print(f"FATAL ERROR: Path '{p}' not a dir.")
setup_initial_directories()

def get_effective_base_json_directory():
    abs_browsable_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    rel_sel_path = session.get('plotter_selected_base_json_folder_rel', None) 
    if rel_sel_path is not None:
        eff_abs_path = os.path.normpath(os.path.join(abs_browsable_root, rel_sel_path))
        if os.path.abspath(eff_abs_path).startswith(abs_browsable_root) and os.path.isdir(eff_abs_path):
            return eff_abs_path
    return os.path.abspath(DEFAULT_BASE_JSON_DIRECTORY)

def get_user_session_upload_path():
    """Generates or retrieves a unique upload path for the current user session."""
    # Use a plotter-specific session key for the upload subdirectory
    if 'plotter_user_upload_subdir' not in session:
        session['plotter_user_upload_subdir'] = f"plotter_uploads_{uuid.uuid4().hex[:12]}"
    
    user_specific_dir_name = session['plotter_user_upload_subdir']
    user_specific_upload_path = os.path.join(REMOTE_UPLOAD_STORAGE_ROOT, user_specific_dir_name)
    os.makedirs(user_specific_upload_path, exist_ok=True)
    return user_specific_upload_path

def is_number(s):
    try: float(s); return True
    except (ValueError, TypeError): return False

@app.route('/')
def plotter_home():
    # Optional: Clear previous session's uploaded files when a user revisits the home page
    # This requires careful thought on persistence. For now, manual clear or let them accumulate per session ID.
    # old_upload_subdir = session.pop('plotter_user_upload_subdir', None)
    # if old_upload_subdir:
    #     path_to_clear = os.path.join(REMOTE_UPLOAD_STORAGE_ROOT, old_upload_subdir)
    #     if os.path.exists(path_to_clear):
    #         try: shutil.rmtree(path_to_clear)
    #         except Exception as e: print(f"Warning: Could not clear old upload dir '{path_to_clear}': {e}")
    
    session.pop('plotter_selected_base_json_folder_rel', None) # Reset selected base path
    return render_template('plotter_index.html', default_regex=DEFAULT_FILENAME_REGEX)

@app.route('/browse_server_dirs_for_base', methods=['POST'])
def browse_server_dirs_for_base_api():
    abs_browse_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    # print(f"DEBUG /browse_server_dirs: abs_browse_root = {abs_browse_root}")
    if not os.path.isdir(abs_browse_root):
        return jsonify({"error": "Server config: Browsable root inaccessible."}), 500

    path_from_client_rel = request.json.get('path', '')
    # print(f"DEBUG /browse_server_dirs: path_from_client_rel = '{path_from_client_rel}'")
    safe_rel_path = path_from_client_rel.lstrip('/').lstrip('\\')
    path_to_list_abs = os.path.normpath(os.path.join(abs_browse_root, safe_rel_path))

    if not os.path.realpath(path_to_list_abs).startswith(os.path.realpath(abs_browse_root)):
        # print(f"DEBUG /browse_server_dirs: Path traversal attempt or invalid. Defaulting to root.")
        path_to_list_abs = abs_browse_root 
    
    if not os.path.isdir(path_to_list_abs):
        return jsonify({"error": f"Path '{safe_rel_path}' is not a directory in browsable area."}), 400

    listed_dirs = []
    current_listing_rel_to_root = os.path.relpath(path_to_list_abs, abs_browse_root).replace('\\', '/')
    if current_listing_rel_to_root == '.': current_listing_rel_to_root = ''

    if os.path.abspath(path_to_list_abs) != abs_browse_root:
        parent_abs = os.path.dirname(path_to_list_abs)
        parent_rel = os.path.relpath(parent_abs, abs_browse_root).replace('\\', '/')
        if parent_rel == '.': parent_rel = '' 
        listed_dirs.append({"name": ".. (Parent)", "path": parent_rel, "type": "parent_selectable"})

    try:
        for item_name in sorted(os.listdir(path_to_list_abs)):
            item_abs = os.path.join(path_to_list_abs, item_name)
            if os.path.isdir(item_abs):
                item_rel = os.path.relpath(item_abs, abs_browse_root).replace('\\', '/')
                listed_dirs.append({"name": item_name, "path": item_rel, "type": "dir_selectable"})
    except OSError as e:
        print(f"ERROR /browse_server_dirs: Cannot list '{path_to_list_abs}': {e}")
        return jsonify({"error": f"Cannot access directory contents of '{current_listing_rel_to_root}'. Check server permissions."}), 500
    
    return jsonify({"current_browsing_path_rel": current_listing_rel_to_root, "directories": listed_dirs})

@app.route('/set_base_json_folder', methods=['POST'])
def set_base_json_folder_api():
    sel_path_rel = request.json.get('selected_path_rel', None) 
    if sel_path_rel is None: return jsonify({"error": "No selection path provided."}), 400
    abs_browse_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    safe_sel_rel = sel_path_rel.lstrip('/').lstrip('\\') 
    prosp_base_abs = os.path.normpath(os.path.join(abs_browse_root, safe_sel_rel))
    if not (os.path.abspath(prosp_base_abs).startswith(abs_browse_root) and os.path.isdir(prosp_base_abs)):
        return jsonify({"error": "Invalid or inaccessible folder for base."}), 400
    session['plotter_selected_base_json_folder_rel'] = safe_sel_rel 
    # print(f"INFO: Session plotter_selected_base_json_folder_rel set to '{safe_sel_rel}'")
    return jsonify({"message": f"Session base set to: .../{safe_sel_rel or '(Top Area)'}", "selected_base_json_folder_rel_for_display": safe_sel_rel})

@app.route('/upload_local_jsons', methods=['POST'])
def upload_local_jsons_api():
    user_session_upload_abs_path = get_user_session_upload_path() 
    if not request.files: return jsonify({"error": "No files in request."}), 400
    count, errors = 0, []
    for form_field_key, file_storage in request.files.items(): # Iterate all files sent
        if file_storage and file_storage.filename:
            original_fn = secure_filename(file_storage.filename)
            if not original_fn.lower().endswith('.json'): 
                errors.append(f"Skipped (not JSON): {original_fn}"); continue
            try:
                # Use form_field_key if it contains path info from webkitRelativePath
                # Otherwise, save directly with original_fn
                path_within_upload = form_field_key
                if path_within_upload == "blob" or path_within_upload == file_storage.filename : # "blob" can be default key for single file, or just filename
                    path_within_upload = original_fn # save flat
                
                # Construct save path carefully, ensuring subdirectories for uploads are created
                full_save_path = os.path.join(user_session_upload_abs_path, path_within_upload)
                save_dir = os.path.dirname(full_save_path)
                os.makedirs(save_dir, exist_ok=True)
                
                file_storage.save(full_save_path)
                count += 1
            except Exception as e: errors.append(f"Error saving {original_fn}: {str(e)}")
    if count == 0 and not errors: return jsonify({"error": "No JSONs uploaded."}), 400
    msg = f"Uploaded {count} JSON(s) to server session."
    if errors: msg += f" Encountered errors: {'; '.join(errors)}"
    return jsonify({"message": msg, "uploaded_count": count, "errors": errors or None})

@app.route('/list_json_keys', methods=['POST'])
def list_json_keys_api():
    try:
        data = request.get_json(); sub_rel = data.get('folder_path', ''); regex_s = data.get('filename_regex', DEFAULT_FILENAME_REGEX) 
        eff_base = get_effective_base_json_directory()
        search_server_root = os.path.normpath(os.path.join(eff_base, sub_rel))
        search_upload_root = get_user_session_upload_path() # For this session's uploads
        
        if '..' in sub_rel: return jsonify({"error":"Invalid sub-folder."}),400
        try: rgx=re.compile(regex_s, re.IGNORECASE)
        except re.error as e: return jsonify({"error": f"Regex Err: {e}"}),400
        if not os.path.abspath(search_server_root).startswith(os.path.abspath(eff_base)): return jsonify({"error":"Denied: Sub-folder outside base."}),403
        
        all_keys,num_keys,found_count = set(),set(),0
        methods = {} # id: display_name
        files_display = []

        def scan_dir(scan_base_abs, display_prefix, search_path_display_name_part):
            nonlocal found_count # Allow modification
            if not os.path.isdir(scan_base_abs):
                # Only print warning if it's not the (potentially empty) upload dir
                if scan_base_abs != search_upload_root or os.path.exists(search_upload_root) : 
                     print(f"Warning list_keys: Scan path '{scan_base_abs}' not a dir.")
                return

            for d_path,_,f_names in os.walk(scan_base_abs):
                for f_name in f_names:
                    if rgx.fullmatch(f_name):
                        found_count+=1; f_abs=os.path.join(d_path,f_name)
                        scan_base_abs_rel=os.path.relpath(f_abs,scan_base_abs).replace('\\','/')
                        files_display.append(f"{display_prefix}{scan_base_abs_rel}")
                        rel_d=os.path.relpath(d_path,scan_base_abs).replace('\\','/')
                        m_id,m_dsp=(os.path.abspath(d_path), f"{display_prefix}{rel_d}") if rel_d!='.' \
                            else (f_abs, f"{display_prefix}{f_name} (in '{search_path_display_name_part or '(base/uploads root)'}')")
                        if m_id not in methods: methods[m_id]=m_dsp
                        try:
                            with open(f_abs,'r',encoding='utf-8')as f:c=json.load(f)
                            if isinstance(c,dict)and c:
                                rp1k=next(iter(c),None)
                                if rp1k and isinstance(c[rp1k],dict):
                                    for k,v in c[rp1k].items():
                                        all_keys.add(k)
                                        if is_number(v):num_keys.add(k)
                        except Exception as e:print(f"W (keys): {f_abs}: {e}")
        
        scan_dir(search_server_root, "Server: ", sub_rel) # Scan server data path
        if os.path.exists(search_upload_root): # Only scan uploads if dir exists
            scan_dir(search_upload_root, "Uploaded: ", "uploads") # Scan session uploads path

        if found_count==0:return jsonify({"error":f"No files match '{regex_s}' in scanned paths."}),404
        s_keys=sorted(list(all_keys.intersection(num_keys)));m_ui=[{"id":mid,"name":dn}for mid,dn in methods.items()]
        m_ui.sort(key=lambda x:x["name"]);msg=f"{found_count} files. {len(m_ui)} series. ";
        msg+=f"{len(s_keys)} keys."if s_keys else "No numeric keys.";
        df_x,df_y="size","psnr"; # filesize(MB)
        if "size" not in s_keys and "filesize(MB)" in s_keys:df_x="filesize(MB)"
        return jsonify({"available_keys":s_keys,"methods_for_selection":m_ui,"processed_filenames":sorted(files_display),"default_x_key":df_x if df_x in s_keys else(s_keys[0]if s_keys else None),"default_y_key":df_y if df_y in s_keys else(s_keys[1]if len(s_keys)>1 else(s_keys[0]if s_keys else None)),"message":msg})
    except Exception as e:print(f"CRIT /list_json_keys:{e}");import traceback;traceback.print_exc();return jsonify({"error":f"Srv err keys:{e}"}),500

@app.route('/get_plot_data', methods=['POST'])
def get_plot_data_api(): # Keep this robust, uses method_ids from combined scan
    # ... (Identical to previous FULL version that handles various method_id sources)
    try:
        data=request.json;sub_f_rel=data.get('folder_path','');rgx_s=data.get('filename_regex',DEFAULT_FILENAME_REGEX);
        xk,yk=data.get('x_key'),data.get('y_key');sel_mids=data.get('selected_methods',[])
        if not xk or not yk:return jsonify({"error":"X/Y keys req."}),400
        if not sel_mids:return jsonify({"error":"No methods selected."}),404
        try:rgx=re.compile(rgx_s,re.IGNORECASE)
        except re.error as e:return jsonify({"error":f"Regex:{e}"}),400
        
        plots,table_data={},[]
        
        # Need these to reconstruct display names consistently with list_json_keys
        eff_base=get_effective_base_json_directory(); srv_search_root=os.path.normpath(os.path.join(eff_base,sub_f_rel))
        upl_search_root=get_user_session_upload_path()

        for mid_abs in sel_mids: # method_id is an absolute path from server
            m_dsp_name = os.path.basename(mid_abs) # Fallback
            is_upl = os.path.abspath(mid_abs).startswith(os.path.abspath(REMOTE_UPLOAD_STORAGE_ROOT))
            current_search_root_for_relpath = upl_search_root if is_upl else srv_search_root
            prefix = "Uploaded: " if is_upl else "Server: "
            
            # Reconstruct display name as done in list_json_keys
            if os.path.abspath(mid_abs).startswith(os.path.abspath(current_search_root_for_relpath)):
                temp_r = os.path.relpath(mid_abs, current_search_root_for_relpath)
                if os.path.isdir(mid_abs):
                    temp_r_rel = temp_r.replace('\\','/')
                    m_dsp_name = f"{prefix}{temp_r_rel}"
                    if m_dsp_name == f"{prefix}.": m_dsp_name = f"{prefix}(files in '{'uploads' if is_upl else sub_f_rel or '(base)'}')"
                else: # File ID
                     m_dsp_name = f"{prefix}{os.path.basename(mid_abs)} (in '{'uploads' if is_upl else sub_f_rel or '(base)'}')"
            
            mx,my,mh=[],[],[]
            files_to_proc=[]
            if os.path.isdir(mid_abs):
                for fn in os.listdir(mid_abs):
                    if rgx.fullmatch(fn):files_to_proc.append(os.path.join(mid_abs,fn))
            elif os.path.isfile(mid_abs):
                if rgx.fullmatch(os.path.basename(mid_abs)):files_to_proc.append(mid_abs)
            
            for fp in files_to_proc:
                f_disp=os.path.basename(fp)
                try:
                    with open(fp,'r',encoding='utf-8')as f:jd=json.load(f)
                    if isinstance(jd,dict):
                        for rpi,rpd in jd.items():
                            if isinstance(rpd,dict)and xk in rpd and yk in rpd:
                                xvo,yvo=rpd[xk],rpd[yk]
                                if is_number(xvo)and is_number(yvo):
                                    xf,yf=float(xvo),float(yvo);mx.append(xf);my.append(yf)
                                    mh.append(f"S:{m_dsp_name}<br>F:{f_disp}<br>RP:{rpi}<br>{xk}:{xf:.4g}<br>{yk}:{yf:.4g}")
                                    table_data.append({"Method":m_dsp_name,"File":f_disp,"Rate Point":rpi,xk:xf,yk:yf})
                except Exception as e:print(f"W(data):{fp}:{e}")
            if mx:
                if m_dsp_name not in plots:plots[m_dsp_name]={"x":[],"y":[],"hovertext":[]}
                plots[m_dsp_name]["x"].extend(mx);plots[m_dsp_name]["y"].extend(my);plots[m_dsp_name]["hovertext"].extend(mh)
        if not plots and sel_mids:return jsonify({"error":f"No data for keys('{xk}','{yk}') in sel series."}),404
        return jsonify({"plot_traces":plots,"tabular_data":table_data,"x_axis_label":xk,"y_axis_label":yk})
    except Exception as e: print(f"CRIT /get_plot_data:{e}");import traceback;traceback.print_exc();return jsonify({"error":f"Srv err plot data:{e}"}),500


if __name__ == '__main__':
    print(f"--- JSON Plotter Application (Server Upload Version) ---")
    app.run(host='0.0.0.0', port=5003, debug=True)