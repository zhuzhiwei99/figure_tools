from flask import Flask, render_template, request, jsonify, session
import os
import json
import re 
from werkzeug.utils import secure_filename # For output filenames, though not strictly needed here for input

app = Flask(__name__)
app.secret_key = "REPLACE_THIS_plotter_secret_key_with_a_very_strong_random_string_!@#$"

# --- Configuration ---
# CRITICAL: These MUST be ABSOLUTE PATHS on your server.
# BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS: The top-level directory users can browse within.
# Example: "/srv/data_projects/json_collections"
BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS = os.path.abspath("/work/Users/zhuzhiwei/project/3dRecon/compress/GSCodec_Studio/examples/results/gsc_compression_bartender")

# DEFAULT_BASE_JSON_DIRECTORY: Fallback if user doesn't select a base via browser.
# Can be the same as BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS or a specific subfolder within it.
# Example: "/srv/data_projects/json_collections/default_experiment_data"
DEFAULT_BASE_JSON_DIRECTORY = os.path.abspath("/work/Users/zhuzhiwei/project/3dRecon/compress/")

print(f"INFO: Plotter App Initialized.")
print(f"INFO: BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS (abs): {BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS}")
print(f"INFO: DEFAULT_BASE_JSON_DIRECTORY (abs): {DEFAULT_BASE_JSON_DIRECTORY}")

def setup_initial_directories():
    """Creates configured directories if they don't exist (for convenience, esp. local dev)."""
    paths_to_check = [BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS, DEFAULT_BASE_JSON_DIRECTORY]
    for path in paths_to_check:
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                print(f"INFO: Created directory: '{path}' (Please populate if it's a data source)")
            except OSError as e:
                print(f"FATAL ERROR: Could not create essential directory '{path}': {e}. Please check permissions or create manually.")
                # Consider raising an exception or exiting if this setup is critical.
        elif not os.path.isdir(path):
            print(f"FATAL ERROR: Configured path '{path}' exists but is NOT a directory. Application might not work correctly.")
setup_initial_directories()

def get_effective_base_json_directory():
    """
    Returns the absolute path to the current effective base JSON directory.
    This is either selected by the user (stored in session, relative to BROWSABLE_SERVER_ROOT)
    or defaults to DEFAULT_BASE_JSON_DIRECTORY.
    """
    abs_browsable_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    # Path from session is relative to abs_browsable_root
    relative_selected_path = session.get('plotter_selected_base_json_folder_rel', None) 
    
    if relative_selected_path is not None: # '' (empty string) is valid - means the browsable root itself
        effective_abs_path = os.path.normpath(os.path.join(abs_browsable_root, relative_selected_path))
        # Security: Final check that the resolved path is within the allowed browsable root and is a directory
        if os.path.abspath(effective_abs_path).startswith(abs_browsable_root) and os.path.isdir(effective_abs_path):
            return effective_abs_path
        else:
            print(f"WARNING: Invalid path derived from session. Rel='{relative_selected_path}', ResolvedAbs='{effective_abs_path}'. Defaulting.")
    return os.path.abspath(DEFAULT_BASE_JSON_DIRECTORY)

def is_number(s):
    try: float(s); return True
    except (ValueError, TypeError): return False

@app.route('/')
def plotter_home():
    # Clear session key for base folder selection when user visits home page for a "fresh start"
    if 'plotter_selected_base_json_folder_rel' in session:
        session.pop('plotter_selected_base_json_folder_rel', None)
    return render_template('plotter_index.html')

@app.route('/browse_server_dirs_for_base', methods=['POST'])
def browse_server_dirs_for_base_api():
    abs_browsable_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    if not os.path.isdir(abs_browsable_root):
        return jsonify({"error": "Server misconfiguration: Main browsable root for JSON folders is invalid."}), 500

    data = request.get_json()
    # path_from_client is expected to be relative to abs_browsable_root
    path_from_client_rel = data.get('path', '') 
    safe_relative_path = path_from_client_rel.lstrip('/').lstrip('\\')
    path_to_list_abs = os.path.normpath(os.path.join(abs_browsable_root, safe_relative_path))

    # Security: Default to root if path attempts to go outside
    if not os.path.abspath(path_to_list_abs).startswith(abs_browsable_root):
        path_to_list_abs = abs_browsable_root 
    
    if not os.path.isdir(path_to_list_abs):
        return jsonify({"error": f"Path '{safe_relative_path}' is not a valid browsable directory."}), 400

    listed_dirs_for_client = []
    # This is the path of the directory currently being listed, relative to abs_browsable_root.
    # It's what JS uses to keep track and send for selection.
    current_listing_rel_to_root = os.path.relpath(path_to_list_abs, abs_browsable_root).replace('\\', '/')
    if current_listing_rel_to_root == '.': current_listing_rel_to_root = ''

    # Parent ("..") link
    if os.path.abspath(path_to_list_abs) != abs_browsable_root:
        parent_dir_abs = os.path.dirname(path_to_list_abs)
        parent_dir_rel_for_client = os.path.relpath(parent_dir_abs, abs_browsable_root).replace('\\', '/')
        if parent_dir_rel_for_client == '.': parent_dir_rel_for_client = '' 
        listed_dirs_for_client.append({"name": ".. (Parent)", "path": parent_dir_rel_for_client, "type": "parent_selectable"})

    for item_name in sorted(os.listdir(path_to_list_abs)):
        item_abs_path = os.path.join(path_to_list_abs, item_name)
        if os.path.isdir(item_abs_path):
            item_rel_for_client = os.path.relpath(item_abs_path, abs_browsable_root).replace('\\', '/')
            listed_dirs_for_client.append({"name": item_name, "path": item_rel_for_client, "type": "dir_selectable"})
    
    return jsonify({
        "current_browsing_path_rel": current_listing_rel_to_root,
        "directories": listed_dirs_for_client
    })

@app.route('/set_base_json_folder', methods=['POST'])
def set_base_json_folder_api():
    data = request.get_json()
    # This path is sent by JS and is relative to BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS
    selected_path_rel_from_client = data.get('selected_path_rel', None) 
    if selected_path_rel_from_client is None: return jsonify({"error": "No selection path."}), 400

    abs_browsable_root = os.path.abspath(BROWSABLE_SERVER_ROOT_FOR_JSON_FOLDERS)
    safe_selected_rel = selected_path_rel_from_client.lstrip('/').lstrip('\\') 
    prospective_new_base_abs = os.path.normpath(os.path.join(abs_browsable_root, safe_selected_rel))

    if not (os.path.abspath(prospective_new_base_abs).startswith(abs_browsable_root) and \
            os.path.isdir(prospective_new_base_abs)):
        return jsonify({"error": "Invalid or inaccessible folder selected as base."}), 400

    session['plotter_selected_base_json_folder_rel'] = safe_selected_rel 
    return jsonify({
        "message": f"Session base folder set to: .../{safe_selected_rel or '(Top Browsable Area)'}.",
        "selected_base_json_folder_rel_for_display": safe_selected_rel
    })

@app.route('/list_json_keys', methods=['POST'])
def list_json_keys_api():
    try:
        data = request.get_json()
        sub_folder_path_rel_to_effective_base = data.get('folder_path', '') 
        filename_regex_str = data.get('filename_regex', r'.*rp_summary.json$') 
        effective_base_abs = get_effective_base_json_directory()

        if '..' in sub_folder_path_rel_to_effective_base: return jsonify({"error": "Invalid sub-folder path."}), 400
        try: filename_regex = re.compile(filename_regex_str, re.IGNORECASE)
        except re.error as e: return jsonify({"error": f"Invalid Regex: {str(e)}"}), 400
            
        # This is the absolute path from where the recursive search will begin.
        search_root_abs = os.path.normpath(os.path.join(effective_base_abs, sub_folder_path_rel_to_effective_base))

        if not os.path.abspath(search_root_abs).startswith(os.path.abspath(effective_base_abs)):
            return jsonify({"error": "Access Denied: Sub-folder is outside current base."}), 403
        if not os.path.isdir(search_root_abs):
            return jsonify({"error": f"Search path not found: '{sub_folder_path_rel_to_effective_base}' (relative to current base: '{os.path.basename(effective_base_abs)}')."}), 404

        all_rp_metric_keys, numeric_rp_metric_keys = set(), set()
        found_files_count = 0
        discovered_methods_info = {} # Key: method_id (unique path), Value: {display_name, file_count}

        for dirpath, _, filenames in os.walk(search_root_abs):
            for filename in filenames:
                if filename_regex.fullmatch(filename):
                    found_files_count += 1
                    file_abs_path = os.path.join(dirpath, filename)
                    
                    # Method ID needs to be unique and reconstructable/findable by get_plot_data
                    # Method Display Name is for the UI checkboxes
                    rel_dir_of_file_from_search_root = os.path.relpath(dirpath, search_root_abs).replace('\\', '/')
                    
                    method_id = os.path.abspath(dirpath) # Absolute path of the directory is a stable ID for a method
                    method_display_name = rel_dir_of_file_from_search_root
                    if rel_dir_of_file_from_search_root == '.': # Files directly in search_root_abs
                         # For files directly in search root, make the file itself a "method"
                         method_id = file_abs_path 
                         method_display_name = f"{filename} (in '{sub_folder_path_rel_to_effective_base or '(current base)'}')"

                    if method_id not in discovered_methods_info:
                         discovered_methods_info[method_id] = {"display_name": method_display_name, "files_contributing": 0}
                    discovered_methods_info[method_id]["files_contributing"] +=1
                    
                    try: 
                        with open(file_abs_path, 'r', encoding='utf-8') as f: content = json.load(f)
                        if isinstance(content, dict) and content: # JSON is a dict of ratepoints
                            first_rp_key = next(iter(content), None) # Get one ratepoint key
                            if first_rp_key and isinstance(content[first_rp_key], dict):
                                for metric_key, metric_value in content[first_rp_key].items():
                                    all_rp_metric_keys.add(metric_key)
                                    if is_number(metric_value): numeric_rp_metric_keys.add(metric_key)
                    except Exception as e: print(f"Warning (keys): Error parsing {file_abs_path}: {e}")
        
        if found_files_count == 0:
            return jsonify({"error": f"No files found matching '{filename_regex_str}' in the specified path and its subdirectories."}), 404
        
        plot_suitable_metric_keys = sorted(list(all_rp_metric_keys.intersection(numeric_rp_metric_keys)))
        
        methods_for_ui_selection = []
        for mid, mdata in discovered_methods_info.items():
            methods_for_ui_selection.append({"id": mid, "name": mdata["display_name"]})
        methods_for_ui_selection.sort(key=lambda x: x["name"]) # Sort for UI consistency

        msg = f"{found_files_count} files scanned. {len(methods_for_ui_selection)} potential data series (methods/files) identified. "
        if not plot_suitable_metric_keys: msg += "No common numeric metric keys for plotting."
        else: msg += f"{len(plot_suitable_metric_keys)} suitable X/Y metric keys found."
        return jsonify({
            "available_keys": plot_suitable_metric_keys, "methods_for_selection": methods_for_ui_selection, "message": msg
        })
    except Exception as e:
        print(f"CRITICAL ERROR in /list_json_keys: {e}"); import traceback; traceback.print_exc()
        return jsonify({"error": f"Server error in list_json_keys: {str(e)}"}), 500

@app.route('/get_plot_data', methods=['POST'])
def get_plot_data_api():
    try:
        data = request.get_json()
        sub_folder_path = data.get('folder_path', '')
        filename_regex_str = data.get('filename_regex', r'.*rp_summary.json$')
        x_key, y_key = data.get('x_key'), data.get('y_key')
        selected_method_ids = data.get('selected_methods', []) # List of absolute paths (method_id from client)

        if not x_key or not y_key: return jsonify({"error": "X/Y metric keys required."}), 400
        if not selected_method_ids: return jsonify({"error": "No data series/methods selected."}), 404
        
        effective_base_abs = get_effective_base_json_directory()
        # search_root_abs is where the initial scan for methods was done.
        # We need it to correctly determine display names for methods if method_id is a file path.
        search_root_abs_for_display_names = os.path.normpath(os.path.join(effective_base_abs, sub_folder_path))

        try: filename_regex = re.compile(filename_regex_str, re.IGNORECASE)
        except re.error as e: return jsonify({"error": f"Invalid regex: {str(e)}"}), 400

        all_methods_plot_data = {} 
        tabular_data_for_view = [] 

        for method_id_abs_path in selected_method_ids:
            # method_id_abs_path is an absolute path to either a directory or a specific file
            # (if that file was directly in search_root_abs).
            
            # Determine display name for the plot legend/table
            method_display_name = ""
            if os.path.abspath(method_id_abs_path).startswith(os.path.abspath(search_root_abs_for_display_names)):
                 method_rel_path_for_display = os.path.relpath(method_id_abs_path, search_root_abs_for_display_names)
                 if os.path.isdir(method_id_abs_path): # If ID is a directory
                     method_display_name = method_rel_path_for_display.replace('\\','/')
                     if method_display_name == '.': method_display_name = "(files in search root)"
                 else: # If ID is a file path
                     method_display_name = f"{os.path.basename(method_id_abs_path)} (in '{sub_folder_path or '(current base)'}')"
            else: # Fallback, should ideally not happen if IDs are consistent
                 method_display_name = os.path.basename(method_id_abs_path)


            current_method_x, current_method_y, current_method_hover = [], [], []
            files_to_process_for_this_method = []

            if os.path.isdir(method_id_abs_path):
                # Process all matching JSON files directly within this directory
                # This assumes a "method" is defined by files in ONE directory level, not its sub-sub-dirs.
                for filename_in_dir in os.listdir(method_id_abs_path):
                    if filename_regex.fullmatch(filename_in_dir):
                        files_to_process_for_this_method.append(os.path.join(method_id_abs_path, filename_in_dir))
            elif os.path.isfile(method_id_abs_path): # method_id was a specific file
                files_to_process_for_this_method.append(method_id_abs_path)

            for file_path in files_to_process_for_this_method:
                file_display_name = os.path.basename(file_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f: json_content = json.load(f)
                    if isinstance(json_content, dict): # Expecting dict of ratepoints
                        for rp_id, rp_data in json_content.items(): 
                            if isinstance(rp_data, dict) and x_key in rp_data and y_key in rp_data:
                                x_orig, y_orig = rp_data[x_key], rp_data[y_key]
                                if is_number(x_orig) and is_number(y_orig):
                                    x_f, y_f = float(x_orig), float(y_orig)
                                    current_method_x.append(x_f); current_method_y.append(y_f)
                                    current_method_hover.append(f"Series: {method_display_name}<br>File: {file_display_name}<br>RP: {rp_id}<br>{x_key}: {x_f:.4g}<br>{y_key}: {y_f:.4g}")
                                    tabular_data_for_view.append({"Method": method_display_name, "File": file_display_name, "Rate Point": rp_id, x_key: x_f, y_key: y_f })
                except Exception as e: print(f"Warning (data): Error processing {file_path}: {e}")
            
            if current_method_x: # If data found for this method
                if method_display_name not in all_methods_plot_data: # Should be unique from list_keys if logic matches
                    all_methods_plot_data[method_display_name] = {"x": [], "y": [], "hovertext": []}
                all_methods_plot_data[method_display_name]["x"].extend(current_method_x)
                all_methods_plot_data[method_display_name]["y"].extend(current_method_y)
                all_methods_plot_data[method_display_name]["hovertext"].extend(current_method_hover)

        if not all_methods_plot_data:
            return jsonify({"error": f"No valid data found for selected methods and keys ({x_key}, {y_key})."}), 404
        return jsonify({"plot_traces": all_methods_plot_data, "tabular_data": tabular_data_for_view,
                         "x_axis_label": x_key, "y_axis_label": y_key })
    except Exception as e:
        print(f"CRITICAL ERROR in /get_plot_data: {e}"); import traceback; traceback.print_exc()
        return jsonify({"error": f"Server error in get_plot_data: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"--- JSON Plotter Application (Full Version with Method Selection) ---")
    app.run(host='0.0.0.0', port=5001, debug=True)