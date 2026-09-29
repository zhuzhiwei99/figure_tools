from flask import Flask, render_template, request, jsonify, send_from_directory, session
from PIL import Image, ImageDraw
import os
import json
# import shutil # Not strictly used in the current version, can be removed if not needed later
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
# IMPORTANT: Change this secret key in a production environment!
app.secret_key = "CHANGE_THIS_IN_PRODUCTION_a_very_long_and_random_string" 

# --- Configuration ---
# !!! CRITICAL FOR REMOTE SERVER: SET THIS TO THE ABSOLUTE PATH ON YOUR SERVER !!!
# Example: BASE_IMAGE_DIRECTORY = "/var/www/my_annotator_images"
# Example: BASE_IMAGE_DIRECTORY = "/home/username/image_projects/source_images"
BASE_IMAGE_DIRECTORY = os.path.abspath("/work/Users/zhuzhiwei/project/3dRecon/reconstruct/lowRankGS/results/figure") 
# If "./YOUR_BASE_IMAGE_FOLDER_ON_SERVER" is relative, it's relative to where app.py is run.
# For remote servers, an absolute path is highly recommended.

OUTPUT_BASE_DIR = os.path.abspath("./annotated_output") # Output relative to app.py
DRAW_SUBDIR = "draw"
CUT_SUBDIR = "cut"
PARAMS_FILE = "parameters.json"

TEMP_DISPLAY_DIR_NAME = 'temp_images' 
TEMP_UPLOAD_DIR_NAME = 'temp_uploads' 

TEMP_DISPLAY_DIR_ABSPATH = os.path.join(app.static_folder, TEMP_DISPLAY_DIR_NAME)
TEMP_UPLOAD_DIR_ABSPATH = os.path.join(app.root_path, TEMP_UPLOAD_DIR_NAME)

def setup_directories():
    """Creates necessary directories if they don't exist."""
    # Check and create BASE_IMAGE_DIRECTORY (this is for convenience during local dev)
    # On a remote server, this directory should ideally be pre-existing and configured.
    if not os.path.exists(BASE_IMAGE_DIRECTORY):
        print(f"WARNING: BASE_IMAGE_DIRECTORY '{BASE_IMAGE_DIRECTORY}' does not exist.")
        try:
            os.makedirs(BASE_IMAGE_DIRECTORY)
            print(f"Created empty BASE_IMAGE_DIRECTORY: '{BASE_IMAGE_DIRECTORY}'. "
                  f"Ensure this path is correct and populate it with images on your server.")
        except OSError as e:
            print(f"ERROR: Could not create BASE_IMAGE_DIRECTORY '{BASE_IMAGE_DIRECTORY}': {e}. "
                  f"Please create this directory manually on the server with appropriate permissions.")
            # In a production setting, you might want to exit if this critical path is not available.
    elif not os.path.isdir(BASE_IMAGE_DIRECTORY):
        print(f"ERROR: Configured BASE_IMAGE_DIRECTORY '{BASE_IMAGE_DIRECTORY}' is not a directory. "
              f"Please check the path and ensure it's a directory.")
    
    # Create output and temporary directories relative to the app's execution path
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    os.makedirs(TEMP_DISPLAY_DIR_ABSPATH, exist_ok=True)
    os.makedirs(TEMP_UPLOAD_DIR_ABSPATH, exist_ok=True)

setup_directories()

# --- Helper Functions ---
def get_display_path_and_original_pil(server_image_path):
    if not os.path.exists(server_image_path) or not os.path.isfile(server_image_path):
        print(f"Error in get_display_path_and_original_pil: File not found: {server_image_path}")
        return None, None, None
    try:
        original_pil_image = Image.open(server_image_path).convert("RGB")
        filename = os.path.basename(server_image_path)
        temp_display_image_name = f"display_{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
        web_accessible_path = os.path.join(TEMP_DISPLAY_DIR_ABSPATH, temp_display_image_name)
        original_pil_image.save(web_accessible_path)
        display_url = f"/static/{TEMP_DISPLAY_DIR_NAME}/{temp_display_image_name}"
        return display_url, original_pil_image, server_image_path
    except Exception as e:
        print(f"Error preparing image ('{server_image_path}') for display: {e}")
        return None, None, None

def process_image_data(image_pil, original_selection_coords, selection_shape, selection_color, line_width,
                       output_basename, base_output_path_for_job):
    if not original_selection_coords:
        return None, None, "No selection coordinates provided."
    try:
        line_width = int(line_width)
        if line_width <= 0: line_width = 2 
    except ValueError:
        line_width = 2 

    draw_dir = os.path.join(base_output_path_for_job, DRAW_SUBDIR)
    cut_dir = os.path.join(base_output_path_for_job, CUT_SUBDIR)
    os.makedirs(draw_dir, exist_ok=True)
    os.makedirs(cut_dir, exist_ok=True)

    annotated_image_pil = image_pil.copy()
    draw_obj = ImageDraw.Draw(annotated_image_pil)
    img_w, img_h = image_pil.size
    x1, y1, x2, y2 = original_selection_coords
    clamped_coords = (
        max(0, min(x1, img_w - 1)), max(0, min(y1, img_h - 1)),
        max(0, min(x2, img_w - 1)), max(0, min(y2, img_h - 1))
    )
    if clamped_coords[2] <= clamped_coords[0] or clamped_coords[3] <= clamped_coords[1]:
        return None, None, f"Selection region invalid for {output_basename}."

    if selection_shape == "Rectangle":
        draw_obj.rectangle(clamped_coords, outline=selection_color, width=line_width)
    elif selection_shape == "Circle":
        draw_obj.ellipse(clamped_coords, outline=selection_color, width=line_width)
    else:
        return None, None, f"Unknown shape: {selection_shape}"

    safe_output_basename = secure_filename(output_basename)
    annotated_image_filename = f"annotated_{safe_output_basename}"
    cropped_image_filename = f"cut_{safe_output_basename}"
    annotated_image_path = os.path.join(draw_dir, annotated_image_filename)
    cropped_image_path = os.path.join(cut_dir, cropped_image_filename)
    try:
        annotated_image_pil.save(annotated_image_path)
        cropped_image_pil = image_pil.crop(clamped_coords)
        cropped_image_pil.save(cropped_image_path)
    except Exception as e:
        print(f"Error saving processed images for {output_basename}: {e}")
        return None, None, f"Error saving images: {str(e)}"
    return annotated_image_path, cropped_image_path, "Success"

# --- Flask Routes ---
@app.route('/')
def index_route(): # Renamed to avoid conflict if 'index' is used elsewhere
    session.clear()
    return render_template('index.html')

@app.route('/list_dirs', methods=['POST'])
def list_dirs_api():
    try:
        # Use the configured BASE_IMAGE_DIRECTORY as the absolute root for browsing
        abs_browse_root = os.path.abspath(BASE_IMAGE_DIRECTORY)

        if not os.path.exists(abs_browse_root) or not os.path.isdir(abs_browse_root):
            error_msg = (f"Server configuration error: The defined BASE_IMAGE_DIRECTORY "
                         f"('{abs_browse_root}') was not found or is not a directory on the server. "
                         f"Please check the 'BASE_IMAGE_DIRECTORY' variable in app.py and server permissions.")
            print(f"CRITICAL ERROR in /list_dirs: {error_msg}")
            return jsonify({"error": error_msg}), 500

        data = request.get_json()
        # current_relative_req_path is the path *relative to abs_browse_root* that the client wants to browse
        current_relative_req_path = data.get('path', '') 
        
        # Sanitize and normalize the relative path
        # Remove leading slashes/backslashes to ensure os.path.join works correctly
        safe_relative_path = current_relative_req_path.lstrip('/').lstrip('\\')
        
        # Construct the full absolute path to the directory the user wants to view
        # os.path.normpath will handle '..' and '.' components
        requested_full_path = os.path.normpath(os.path.join(abs_browse_root, safe_relative_path))
        
        # CRITICAL SECURITY CHECK:
        # Ensure the final resolved path (requested_full_path) is still *within* or *is* our abs_browse_root.
        # This prevents directory traversal attacks (e.g., path = '../../../../etc').
        if not os.path.abspath(requested_full_path).startswith(abs_browse_root):
            print(f"WARNING: /list_dirs - Path traversal attempt or invalid path resolution. "
                  f"Requested relative: '{current_relative_req_path}', Resolved to: '{requested_full_path}', "
                  f"which is outside BASE_IMAGE_DIRECTORY ('{abs_browse_root}'). Defaulting to root.")
            # If an attempt is made to go outside, silently (or with a warning) show the root directory instead.
            current_full_path_to_list = abs_browse_root
        else:
            current_full_path_to_list = requested_full_path

        if not os.path.isdir(current_full_path_to_list):
            # This might happen if the path inside BASE_IMAGE_DIRECTORY is invalid
            # or if the default to root (abs_browse_root) itself is not a dir (covered by initial check).
            return jsonify({"error": f"The path '{os.path.relpath(current_full_path_to_list, abs_browse_root)}' "
                                     f"is not a directory within the allowed browse area."}), 400

        dirs_list = []
        files_list = []
        
        # Path to display in UI (relative to abs_browse_root, using forward slashes for web)
        displayed_relative_path = os.path.relpath(current_full_path_to_list, abs_browse_root).replace('\\', '/')
        if displayed_relative_path == '.': displayed_relative_path = '' # Represents the root itself

        # Add "Parent" (..) directory link if current directory is not the abs_browse_root
        if os.path.abspath(current_full_path_to_list) != abs_browse_root:
            parent_dir_full_path = os.path.dirname(current_full_path_to_list)
            # Ensure parent also stays within or is abs_browse_root (should be true due to earlier checks)
            parent_relative_to_base = os.path.relpath(parent_dir_full_path, abs_browse_root).replace('\\', '/')
            if parent_relative_to_base == '.': parent_relative_to_base = ''
            dirs_list.append({"name": ".. (Parent)", "path": parent_relative_to_base, "type": "parent"})

        # List items in the current directory
        for item_name in sorted(os.listdir(current_full_path_to_list)):
            item_full_path_on_server = os.path.join(current_full_path_to_list, item_name)
            # Path for client should be relative to abs_browse_root
            item_relative_to_base = os.path.relpath(item_full_path_on_server, abs_browse_root).replace('\\', '/')

            if os.path.isdir(item_full_path_on_server):
                dirs_list.append({"name": item_name, "path": item_relative_to_base, "type": "dir"})
            elif item_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                files_list.append({"name": item_name, "path": item_relative_to_base, "type": "file"})
        
        return jsonify({
            "current_relative_path": displayed_relative_path,
            "directories": dirs_list, 
            "files": files_list
        })
    except Exception as e:
        print(f"UNHANDLED ERROR in /list_dirs: {e}")
        import traceback; traceback.print_exc()
        return jsonify({"error": f"An unexpected server error occurred while listing directories: {str(e)}"}), 500

@app.route('/load_image', methods=['POST'])
def load_image_api():
    data = request.get_json()
    relative_image_path_req = data.get('image_path') 
    if not relative_image_path_req:
        return jsonify({"error": "Image path not provided"}), 400
    
    abs_base_dir = os.path.abspath(BASE_IMAGE_DIRECTORY)
    safe_relative_path = relative_image_path_req.lstrip('/').lstrip('\\')
    server_image_path = os.path.normpath(os.path.join(abs_base_dir, safe_relative_path))
    
    if not os.path.abspath(server_image_path).startswith(abs_base_dir):
         return jsonify({"error": "Access denied to image path (outside base directory)"}), 403
    if not os.path.isfile(server_image_path):
        return jsonify({"error": f"Image not found on server: '{relative_image_path_req}'"}), 404

    display_url, original_pil, actual_server_path = get_display_path_and_original_pil(server_image_path)
    if not display_url or not original_pil:
        return jsonify({"error": f"Failed to prepare image '{relative_image_path_req}' for display"}), 500

    session['current_image_original_path'] = actual_server_path
    session['current_image_original_width'] = original_pil.width
    session['current_image_original_height'] = original_pil.height
    session['is_folder_mode'] = False 
    session.pop('uploaded_from_client', None)
    return jsonify({
        "image_url": display_url, "original_width": original_pil.width, "original_height": original_pil.height,
        "message": f"Loaded server image: {os.path.basename(server_image_path)}"
    })

@app.route('/upload_single_image', methods=['POST'])
def upload_single_image_api():
    # ... (This route remains the same as your last provided version) ...
    if 'image_file' not in request.files: return jsonify({"error": "No image file part"}), 400
    file = request.files['image_file']
    if file.filename == '': return jsonify({"error": "No image selected"}), 400
    if file:
        try:
            original_client_filename = secure_filename(file.filename)
            unique_suffix = uuid.uuid4().hex
            extension = os.path.splitext(original_client_filename)[1].lower()
            allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
            if extension not in allowed_extensions: return jsonify({"error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"}), 400
            temp_filename_on_server = f"uploaded_{unique_suffix}{extension}"
            uploaded_image_server_path = os.path.join(TEMP_UPLOAD_DIR_ABSPATH, temp_filename_on_server)
            file.save(uploaded_image_server_path)
            display_url, original_pil, _ = get_display_path_and_original_pil(uploaded_image_server_path)
            if not display_url or not original_pil:
                if os.path.exists(uploaded_image_server_path): os.remove(uploaded_image_server_path)
                return jsonify({"error": "Failed to prepare uploaded image for display"}), 500
            session['current_image_original_path'] = uploaded_image_server_path
            session['current_image_original_width'] = original_pil.width
            session['current_image_original_height'] = original_pil.height
            session['is_folder_mode'] = False
            session['uploaded_from_client'] = True
            session['original_client_filename'] = original_client_filename 
            return jsonify({
                "message": f"Uploaded '{original_client_filename}'. Define region.",
                "image_url": display_url, "original_width": original_pil.width, "original_height": original_pil.height
            })
        except Exception as e:
            print(f"Error uploading/processing single image: {e}"); import traceback; traceback.print_exc()
            return jsonify({"error": f"Server error during image upload: {str(e)}"}), 500
    return jsonify({"error": "File upload error"}), 400


@app.route('/set_folder_and_load_sample', methods=['POST'])
def set_folder_and_load_sample_api():
    # ... (This route remains the same as your last provided version) ...
    data = request.get_json()
    relative_folder_path_req = data.get('folder_path')
    if relative_folder_path_req is None: return jsonify({"error": "Folder path not provided"}), 400
    abs_base_dir = os.path.abspath(BASE_IMAGE_DIRECTORY)
    safe_relative_path = relative_folder_path_req.lstrip('/').lstrip('\\')
    server_folder_path = os.path.normpath(os.path.join(abs_base_dir, safe_relative_path))
    if not os.path.abspath(server_folder_path).startswith(abs_base_dir): return jsonify({"error": "Access denied to folder path"}), 403
    if not os.path.isdir(server_folder_path): return jsonify({"error": f"Folder not found on server: '{relative_folder_path_req}'"}), 404
    session['input_folder_path'] = server_folder_path 
    session['is_folder_mode'] = True
    session.pop('original_selection_coords', None); session.pop('uploaded_from_client', None)
    image_files = sorted([f for f in os.listdir(server_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))])
    if not image_files:
        session.pop('current_image_original_path', None)
        return jsonify({ "message": f"Folder '{relative_folder_path_req}' selected. No images found for sample.", "is_folder_mode": True, "image_url": None })
    sample_image_name = image_files[0]
    sample_image_path = os.path.join(server_folder_path, sample_image_name)
    display_url, original_pil, actual_server_path = get_display_path_and_original_pil(sample_image_path)
    if not display_url or not original_pil: return jsonify({"error": f"Failed to prepare sample image '{sample_image_name}'"}), 500
    session['current_image_original_path'] = actual_server_path
    session['current_image_original_width'] = original_pil.width
    session['current_image_original_height'] = original_pil.height
    return jsonify({
        "image_url": display_url, "original_width": original_pil.width, "original_height": original_pil.height,
        "message": f"Folder '{relative_folder_path_req}' selected. Sample: {sample_image_name}. Define region.", "is_folder_mode": True
    })

@app.route('/process_selection', methods=['POST'])
def process_selection_api():
    data = request.get_json()
    selection = data.get('selection') # This is the 's' I mistakenly used
    shape = data.get('shape')
    color = data.get('color')
    line_width = data.get('lineWidth', 2)
    display_width = data.get('displayWidth')
    display_height = data.get('displayHeight') 

    current_image_original_path = session.get('current_image_original_path')
    original_image_width = session.get('current_image_original_width')
    original_image_height = session.get('current_image_original_height')
    is_folder_mode = session.get('is_folder_mode', False)
    was_uploaded = session.get('uploaded_from_client', False)

    if not all([current_image_original_path, original_image_width is not None, original_image_height is not None, 
                selection, shape, color, display_width is not None, display_height is not None]):
        return jsonify({"error": "Missing critical data for processing."}), 400

    try:
        scale_x = original_image_width / display_width if display_width > 0 else 1 # This is s_x
        scale_y = original_image_height / display_height if display_height > 0 else 1 # This is s_y
        
        # CORRECTED LINE:
        final_original_coords = (
            min(int(selection['x1'] * scale_x), int(selection['x2'] * scale_x)),
            min(int(selection['y1'] * scale_y), int(selection['y2'] * scale_y)),
            max(int(selection['x1'] * scale_x), int(selection['x2'] * scale_x)),
            max(int(selection['y1'] * scale_y), int(selection['y2'] * scale_y))
        )
        
        session['original_selection_coords'] = final_original_coords
        session['selection_shape'] = shape
        session['selection_color'] = color
        session['selection_line_width'] = line_width

        if is_folder_mode and not was_uploaded:
            folder_name = os.path.basename(session.get('input_folder_path', 'unknown_folder'))
            job_output_path = os.path.join(OUTPUT_BASE_DIR, secure_filename(folder_name) + "_batch")
            base_name_for_output_files = os.path.basename(current_image_original_path)
        else: 
            name_only, _ = os.path.splitext(secure_filename(session.get('original_client_filename', 'image') if was_uploaded else os.path.basename(current_image_original_path)))
            job_output_path = os.path.join(OUTPUT_BASE_DIR, name_only + "_single")
            base_name_for_output_files = os.path.basename(current_image_original_path)
        
        os.makedirs(job_output_path, exist_ok=True)

        pil_image_to_process = Image.open(current_image_original_path).convert("RGB")
        
        annotated_path, cropped_path, message = process_image_data(
            pil_image_to_process, 
            final_original_coords, 
            shape, 
            color, 
            line_width, 
            base_name_for_output_files, 
            job_output_path
        )

        if not annotated_path: 
            return jsonify({"error": f"Image processing failed: {message}"}), 500

        params_for_json = {
            "source_image_origin": "uploaded_by_client" if was_uploaded else "server_path",
            "original_source_path_or_filename": session.get('original_client_filename') if was_uploaded else current_image_original_path,
            "server_filename_processed": os.path.basename(current_image_original_path),
            "selection_shape": shape,
            "selection_color": color,
            "selection_line_width": line_width,
            "original_image_size_at_source": (original_image_width, original_image_height),
            "selection_coords_on_original_image": final_original_coords,
            "display_image_size_at_selection_time": (display_width, display_height),
            "selection_coords_on_display_image": selection, # Save the client-side selection coords
            "scale_factors_applied": (scale_x, scale_y),
            "output_job_folder": os.path.basename(job_output_path)
        }
        params_file_path = os.path.join(job_output_path, PARAMS_FILE)
        with open(params_file_path, 'w') as f: 
            json.dump(params_for_json, f, indent=4)

        response_message = f"Image '{os.path.basename(current_image_original_path)}' processed. Parameters saved. "
        if is_folder_mode and not was_uploaded: 
            response_message += "Ready for 'Apply to Folder'."
        
        if was_uploaded and os.path.exists(current_image_original_path):
            try: 
                os.remove(current_image_original_path)
                print(f"Cleaned up transient uploaded file: {current_image_original_path}")
            except OSError as e: 
                print(f"Error cleaning transient file {current_image_original_path}: {e}")
        if was_uploaded: 
            session.pop('uploaded_from_client', None)
            session.pop('original_client_filename', None) # Also pop this

        rel_ann_url = os.path.join(os.path.basename(job_output_path), DRAW_SUBDIR, os.path.basename(annotated_path)).replace('\\','/')
        rel_cut_url = os.path.join(os.path.basename(job_output_path), CUT_SUBDIR, os.path.basename(cropped_path)).replace('\\','/')
        
        return jsonify({
            "message": response_message, 
            "is_folder_mode": is_folder_mode and not was_uploaded, 
            "annotated_image_url": rel_ann_url, 
            "cropped_image_url": rel_cut_url, 
            "params_file": PARAMS_FILE
        })
    except Exception as e:
        print(f"Error in process_selection_api: {e}")
        import traceback
        traceback.print_exc()
        # Attempt to clean up temp uploaded file on error too
        if session.get('uploaded_from_client') and session.get('current_image_original_path'):
             if os.path.exists(session.get('current_image_original_path')):
                try: os.remove(session.get('current_image_original_path'))
                except OSError: pass 
        if session.get('uploaded_from_client'): 
            session.pop('uploaded_from_client', None)
            session.pop('original_client_filename', None)
        return jsonify({"error": f"Server error during processing: {str(e)}"}), 500

@app.route('/apply_to_folder', methods=['POST'])
def apply_to_folder_api():
    # ... (This route remains the same, including line_width handling) ...
    input_folder_path = session.get('input_folder_path'); original_selection_coords = session.get('original_selection_coords') 
    selection_shape = session.get('selection_shape'); selection_color = session.get('selection_color'); selection_line_width = session.get('selection_line_width', 2)
    if not all([input_folder_path, original_selection_coords, selection_shape, selection_color]): return jsonify({"error": "Batch params not set."}), 400
    if not os.path.isdir(input_folder_path): return jsonify({"error": f"Input folder invalid: {input_folder_path}"}), 400
    folder_name = os.path.basename(input_folder_path)
    job_output_path = os.path.join(OUTPUT_BASE_DIR, secure_filename(folder_name) + "_batch")
    os.makedirs(job_output_path, exist_ok=True)
    batch_params_path = os.path.join(job_output_path, PARAMS_FILE)
    batch_params_data = { # ... (fill with relevant params, including line_width)
        "selection_line_width_used": selection_line_width,
        # ... other batch params
    }
    with open(batch_params_path, 'w') as f: json.dump(batch_params_data, f, indent=4)
    processed_count, skipped_count = 0, 0
    image_files = sorted([f for f in os.listdir(input_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))])
    if not image_files: return jsonify({"message": "No images in folder."}), 200
    results_log = []
    for filename in image_files:
        image_full_path = os.path.join(input_folder_path, filename)
        try:
            current_pil_image = Image.open(image_full_path).convert("RGB")
            ann_path, cut_path, msg = process_image_data(current_pil_image, original_selection_coords, selection_shape, selection_color, selection_line_width, filename, job_output_path)
            if ann_path: processed_count += 1; results_log.append(f"OK: {filename}")
            else: skipped_count += 1; results_log.append(f"SKIP {filename}: {msg}")
        except Exception as e: skipped_count += 1; results_log.append(f"ERROR {filename}: {str(e)}")
    summary = (f"Batch for '{folder_name}' done. Processed: {processed_count}, Skipped: {skipped_count}.")
    return jsonify({"message": summary, "details": results_log})


@app.route('/output/<path:job_folder_name>/<path:sub_path>')
def serve_output_file(job_folder_name, sub_path):
    # ... (This route remains the same) ...
    safe_job_folder_name = secure_filename(job_folder_name)
    directory_to_serve_from = os.path.join(OUTPUT_BASE_DIR, safe_job_folder_name)
    requested_path = os.path.normpath(os.path.join(directory_to_serve_from, sub_path))
    if not requested_path.startswith(os.path.abspath(directory_to_serve_from)): return "Access denied", 403
    return send_from_directory(directory_to_serve_from, sub_path)


if __name__ == '__main__':
    print(f"--- Flask Image Annotator (Remote Server Version) ---")
    print(f"IMPORTANT: Ensure BASE_IMAGE_DIRECTORY is set to an ABSOLUTE PATH on your server.")
    print(f"Configured BASE_IMAGE_DIRECTORY: {BASE_IMAGE_DIRECTORY}")
    print(f"Annotation output (relative to app): {OUTPUT_BASE_DIR}")
    print(f"---")
    print(f"To run for remote access (e.g. on your SSH'd server):")
    print(f"  python app.py")
    print(f"Then access via http://<YOUR_SERVER_IP>:5000 in your browser.")
    print(f"Ensure port 5000 is open in your server's firewall if accessing externally.")
    print(f"---")
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=False for production