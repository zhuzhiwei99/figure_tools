from flask import Flask, render_template, request, jsonify, send_file
import os
import io
import zipfile
from urllib.parse import unquote

app = Flask(__name__)

# --- CONFIGURATION ---
ALLOWED_BASE_DIR = "/work/Users/zhuzhiwei/project/3dRecon/compress/"  # Base directory for image scanning
# 【MODIFIED】Define all supported image file extensions
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')


@app.route("/api/list_dirs")
def list_dirs():
    """
    Scans the allowed base directory recursively and builds a nested
    dictionary to represent the directory tree structure for the frontend.
    """
    tree = {}
    start_path = os.path.abspath(ALLOWED_BASE_DIR)
    
    for dirpath, dirnames, _ in os.walk(start_path):
        rel_path = os.path.relpath(dirpath, start_path)
        
        parent = tree
        if rel_path != ".":
            parts = rel_path.split(os.sep)
            for part in parts:
                parent = parent.setdefault(part, {}).setdefault("_subdirs", {})
        
        for d in sorted(dirnames):
            parent[d] = {"_subdirs": {}}
            
    return jsonify(tree)

@app.route("/api/scan_images", methods=["POST"])
def scan_images():
    """
    【MODIFIED】Scans for various image types within a selected directory.
    The path is relative to the ALLOWED_BASE_DIR.
    """
    selected_path = request.json.get("root_dir", "")
    abs_root = os.path.abspath(os.path.join(ALLOWED_BASE_DIR, selected_path))
    
    image_dict = {}
    # Security check: Ensure the path is within the allowed directory
    if abs_root.startswith(ALLOWED_BASE_DIR) and os.path.isdir(abs_root):
    # if os.path.isdir(abs_root):
        for dirpath, _, filenames in os.walk(abs_root):
            for filename in sorted(filenames):
                # Check if the file has one of the supported extensions
                if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    abs_path = os.path.join(dirpath, filename)
                    rel_path_from_base = os.path.relpath(abs_path, ALLOWED_BASE_DIR)
                    
                    if filename not in image_dict:
                        image_dict[filename] = []
                    # Use forward slashes for cross-platform compatibility
                    image_dict[filename].append(rel_path_from_base.replace("\\", "/"))
                    
    return jsonify(image_dict)

@app.route("/download")
def download():
    """
    Provides a download endpoint for a single file.
    """
    path = request.args.get("path", "")
    abs_path = os.path.abspath(os.path.join(ALLOWED_BASE_DIR, path))
    
    # Security check: Ensure the file is within the allowed directory
    if abs_path.startswith(ALLOWED_BASE_DIR) and os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)
        
    return "Invalid file path", 400

@app.route('/api/zip_download')
def zip_download():
    """
    Packages multiple files into a single zip archive for download.
    """
    raw_paths = request.args.get('paths', '')
    if not raw_paths:
        return "No paths provided", 400

    relative_paths = [unquote(p) for p in raw_paths.split(',')]
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for rel_path in relative_paths:
            abs_path = os.path.abspath(os.path.join(ALLOWED_BASE_DIR, rel_path))

            if not abs_path.startswith(ALLOWED_BASE_DIR) or not os.path.isfile(abs_path):
                continue 

            zipf.write(abs_path, arcname=rel_path)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='gsc_gallery_archive.zip'
    )

@app.route("/")
def index():
    """
    Renders the main gallery page.
    """
    return render_template("gallery.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)