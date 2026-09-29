document.addEventListener('DOMContentLoaded', () => {
    const mainImage = document.getElementById('mainImage');
    const selectionCanvas = document.getElementById('selectionCanvas');
    const imageContainer = document.getElementById('imageContainer');
    const statusDiv = document.getElementById('status');
    const directoryBrowserDiv = document.getElementById('directoryBrowser');
    const directoryBrowserTitle = document.getElementById('directoryBrowserTitle');

    const singleImageInputNative = document.getElementById('singleImageInputNative');
    const loadSingleImageBtn = document.getElementById('loadSingleImageBtn');
    const lineWidthInput = document.getElementById('lineWidth'); 

    const confirmSelectionBtn = document.getElementById('confirmSelectionBtn');
    const applyToFolderBtn = document.getElementById('applyToFolderBtn');

    const ctxSelection = selectionCanvas.getContext('2d');

    let isDrawing = false;
    let startX, startY, currentX, currentY;
    let currentSelection = null; 
    let currentDisplayWidth, currentDisplayHeight; 
    let ctrlKeyPressedDuringDraw = false; 

    if (loadSingleImageBtn) {
        loadSingleImageBtn.addEventListener('click', () => singleImageInputNative.click());
    }
    if (singleImageInputNative) {
        singleImageInputNative.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files && files.length > 0) {
                const file = files[0];
                if (file.type.startsWith('image/')) uploadAndLoadSingleImage(file);
                else updateStatus('Error: Please select a valid image file.');
            }
            singleImageInputNative.value = ''; 
        });
    }
    async function uploadAndLoadSingleImage(file) {
        updateStatus(`Uploading ${file.name}...`);
        clearOnNewImageLoad(); 
        const formData = new FormData();
        formData.append('image_file', file);
        try {
            const response = await fetch('/upload_single_image', { method: 'POST', body: formData });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || `HTTP error ${response.status}`);
            if (data.image_url) {
                mainImage.src = data.image_url; 
                mainImage.alt = `Loading ${file.name}...`;
                mainImage.onload = () => {
                    setupCanvases();
                    updateStatus(data.message || `Uploaded ${file.name}. Draw selection.`);
                    confirmSelectionBtn.disabled = true;
                    applyToFolderBtn.classList.add('hidden'); 
                };
                mainImage.onerror = () => { updateStatus(`Error: Could not display uploaded image.`); mainImage.alt = `Error.`;};
            } else { updateStatus(data.message || "Upload failed."); mainImage.alt = "Upload failed.";}
        } catch (error) { updateStatus(`Error uploading: ${error.message}`); console.error('Upload error:', error); mainImage.alt = "Error.";}
    }

    async function fetchAndDisplayDirs(relativePath = '') {
        directoryBrowserDiv.innerHTML = '<p>Loading...</p>';
        updateStatus('Loading directory...');
        try {
            const response = await fetch('/list_dirs', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: relativePath })
            });
            const data = await response.json(); 
            if (!response.ok) {
                const errorMsg = data.error || `HTTP error ${response.status}`;
                directoryBrowserDiv.innerHTML = `<p style="color:red;">Error: ${errorMsg}</p>`;
                directoryBrowserTitle.textContent = `Error: /${relativePath}`;
                updateStatus(`Error fetching dir: ${errorMsg}`); return;
            }
            if (data.error) { 
                 directoryBrowserDiv.innerHTML = `<p style="color:red;">Server Error: ${data.error}</p>`;
                 directoryBrowserTitle.textContent = `Server error: /${relativePath}`;
                 updateStatus(`Server error: ${data.error}`); return;
            }
            directoryBrowserTitle.textContent = `Current: /${data.current_relative_path || ''}`;
            let html = '<ul>';
            if (data.directories.length === 0 && data.files.length === 0 && (data.current_relative_path === '' || !data.directories.some(d => d.type === 'parent'))) {
                 html += '<li><em>(Directory is empty or no accessible items. Check server path and permissions.)</em></li>';
            }
            data.directories.forEach(item => html += `<li data-path="${item.path}" data-type="${item.type}" class="${item.type}-item" title="Go to ${item.path || 'root directory'}">${item.name}</li>`);
            data.files.forEach(item => html += `<li data-path="${item.path}" data-type="${item.type}" class="${item.type}-item" title="Load ${item.name}">${item.name}</li>`);
            html += '</ul>';
            directoryBrowserDiv.innerHTML = html;
            updateStatus('Directory loaded. Select image or Ctrl+Click file for folder mode.');
        } catch (error) { 
            const errorText = `Client error fetching directories: ${error.message}. Check console.`;
            directoryBrowserDiv.innerHTML = `<p style="color:red;">${errorText}</p>`;
            directoryBrowserTitle.textContent = `Client error: /${relativePath}`;
            updateStatus(errorText); console.error('Dir fetch error:', error);
        }
    }
    directoryBrowserDiv.addEventListener('click', (event) => {
        const targetLi = event.target.closest('li');
        if (!targetLi || typeof targetLi.dataset.path === 'undefined') return;
        const path = targetLi.dataset.path;
        const type = targetLi.dataset.type;
        if (type === 'dir' || type === 'parent') fetchAndDisplayDirs(path);
        else if (type === 'file') {
            if (event.ctrlKey || event.metaKey) { 
                 const lastSlash = path.lastIndexOf('/');
                 const folderPath = (lastSlash > -1) ? path.substring(0, lastSlash) : ''; 
                 selectFolderAndLoadSample(folderPath); 
            } else loadImageFromServer(path);
        }
    });
    async function loadImageFromServer(imageRelativePath) {
        updateStatus(`Loading server image: ${imageRelativePath}...`);
        clearOnNewImageLoad();
        try { 
            const response = await fetch('/load_image', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image_path: imageRelativePath }) });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || `HTTP error ${response.status}`);
            if (data.image_url) {
                mainImage.src = data.image_url; mainImage.alt = `Loading ${imageRelativePath}...`;
                mainImage.onload = () => { setupCanvases(); updateStatus(data.message || 'Server image loaded.'); confirmSelectionBtn.disabled = true; applyToFolderBtn.classList.add('hidden'); };
                mainImage.onerror = () => { updateStatus(`Error displaying server image.`); mainImage.alt = `Error.`;};
            } else { updateStatus(data.message || "Image URL not provided."); mainImage.alt = "Load failed.";}
        } catch (error) { updateStatus(`Error loading server image: ${error.message}`); console.error('Server image load error:', error); mainImage.alt = "Error.";}
    }
    async function selectFolderAndLoadSample(folderRelativePath) {
        updateStatus(`Selecting server folder: ${folderRelativePath || '/'}...`);
        clearOnNewImageLoad();
        try { 
            const response = await fetch('/set_folder_and_load_sample', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_path: folderRelativePath }) });
            const data = await response.json();
            if (!response.ok && data.error) throw new Error(data.error || `HTTP error ${response.status}`);
            updateStatus(data.message || 'Folder selected.'); 
            if (data.image_url) { 
                mainImage.src = data.image_url; mainImage.alt = `Loading sample...`;
                mainImage.onload = () => { setupCanvases(); updateStatus(data.message || 'Folder selected. Define on sample.'); confirmSelectionBtn.disabled = true; applyToFolderBtn.classList.add('hidden'); };
                mainImage.onerror = () => { updateStatus(`Error displaying sample image.`); mainImage.alt = `Error.`;};
            } else { mainImage.src = ""; mainImage.alt = "No sample image."; setupCanvases(); updateStatus(data.message || "Folder selected, no sample loaded."); confirmSelectionBtn.disabled = true; applyToFolderBtn.classList.add('hidden');}
        } catch (error) { updateStatus(`Error setting folder: ${error.message}`); console.error('Folder set error:', error); mainImage.alt = "Error.";}
    }

    function clearOnNewImageLoad() {
        mainImage.src = ""; 
        mainImage.alt = "Loading...";
        if (ctxSelection) ctxSelection.clearRect(0, 0, selectionCanvas.width, selectionCanvas.height);
        currentSelection = null;
        confirmSelectionBtn.disabled = true;
        applyToFolderBtn.classList.add('hidden');
        setupCanvases(); 
    }
    
    function setupCanvases() {
        if (!mainImage.complete || mainImage.naturalWidth === 0 || mainImage.src === "" || mainImage.src.includes("alt=")) {
            const containerWidth = imageContainer.clientWidth || 300;
            const containerHeight = imageContainer.clientHeight || 200;
            selectionCanvas.width = containerWidth;
            selectionCanvas.height = containerHeight;
            if (ctxSelection) ctxSelection.clearRect(0, 0, selectionCanvas.width, selectionCanvas.height);
            if (mainImage.alt === "Loading..." && mainImage.src === "") {
                mainImage.alt = "Load an image locally, or browse server images on the left.";
            }
            currentDisplayWidth = 0; currentDisplayHeight = 0;
            return;
        }
        const rect = mainImage.getBoundingClientRect();
        currentDisplayWidth = rect.width;
        currentDisplayHeight = rect.height;
        selectionCanvas.width = currentDisplayWidth;
        selectionCanvas.height = currentDisplayHeight;
        selectionCanvas.style.top = mainImage.offsetTop + 'px';
        selectionCanvas.style.left = mainImage.offsetLeft + 'px';
        clearSelectionDrawing(); 
    }

    function clearSelectionDrawing() {
        if (ctxSelection) ctxSelection.clearRect(0, 0, selectionCanvas.width, selectionCanvas.height);
    }
    
    function getMousePos(canvas, evt) { return { x: evt.clientX - canvas.getBoundingClientRect().left, y: evt.clientY - canvas.getBoundingClientRect().top }; }

    selectionCanvas.addEventListener('mousedown', (e) => {
        if (!mainImage.src || mainImage.src.includes("alt=") || currentDisplayWidth === 0) return; 
        ctrlKeyPressedDuringDraw = e.ctrlKey; 
        const pos = getMousePos(selectionCanvas, e);
        startX = Math.max(0, Math.min(pos.x, currentDisplayWidth)); 
        startY = Math.max(0, Math.min(pos.y, currentDisplayHeight));
        isDrawing = true; currentSelection = null; confirmSelectionBtn.disabled = true;
        clearSelectionDrawing(); 
    });

    selectionCanvas.addEventListener('mousemove', (e) => {
        if (!isDrawing || !mainImage.src || currentDisplayWidth === 0) return;
        const pos = getMousePos(selectionCanvas, e);
        let tempCurrentX = Math.max(0, Math.min(pos.x, currentDisplayWidth));
        let tempCurrentY = Math.max(0, Math.min(pos.y, currentDisplayHeight));
        clearSelectionDrawing();
        if (ctrlKeyPressedDuringDraw) {
            const dx = tempCurrentX - startX; const dy = tempCurrentY - startY;
            const sideLength = Math.max(Math.abs(dx), Math.abs(dy));
            tempCurrentX = startX + (dx > 0 ? sideLength : -sideLength);
            tempCurrentY = startY + (dy > 0 ? sideLength : -sideLength);
            tempCurrentX = Math.max(0, Math.min(tempCurrentX, currentDisplayWidth));
            tempCurrentY = Math.max(0, Math.min(tempCurrentY, currentDisplayHeight));
        }
        currentX = tempCurrentX; currentY = tempCurrentY;
        drawShapeOnCanvas(startX, startY, currentX, currentY, getSelectedShape(), getSelectedColor(), getSelectedLineWidth(), ctxSelection, ctrlKeyPressedDuringDraw);
    });

    selectionCanvas.addEventListener('mouseup', (e) => {
        if (!isDrawing || currentDisplayWidth === 0) return;
        isDrawing = false;
        if (typeof currentX === 'undefined') currentX = startX; if (typeof currentY === 'undefined') currentY = startY;
        const x_1 = Math.min(startX, currentX), y_1 = Math.min(startY, currentY);
        const x_2 = Math.max(startX, currentX), y_2 = Math.max(startY, currentY);
        if ((x_2 - x_1) < 5 || (y_2 - y_1) < 5) { 
            clearSelectionDrawing(); updateStatus("Selection too small.");
            currentSelection = null; confirmSelectionBtn.disabled = true; 
            ctrlKeyPressedDuringDraw = false; return;
        }
        currentSelection = { x1: x_1, y1: y_1, x2: x_2, y2: y_2 };
        clearSelectionDrawing(); 
        drawShapeOnCanvas(currentSelection.x1, currentSelection.y1, currentSelection.x2, currentSelection.y2, 
                  getSelectedShape(), getSelectedColor(), getSelectedLineWidth(), ctxSelection, false); 
        confirmSelectionBtn.disabled = false;
        updateStatus(`Region selected. Coords: (${x_1.toFixed(0)},${y_1.toFixed(0)})-(${x_2.toFixed(0)},${y_2.toFixed(0)})`);
        ctrlKeyPressedDuringDraw = false; 
    });

    function getSelectedShape() { return document.querySelector('input[name="shape"]:checked')?.value || "Rectangle"; }
    function getSelectedColor() { return document.getElementById('shapeColor').value; }
    function getSelectedLineWidth() { 
        const width = parseInt(lineWidthInput.value, 10);
        return (width > 0 && width <= 20) ? width : 2; 
    }

    function drawShapeOnCanvas(x1, y1, x2, y2, shapeType, color, lineWidth, ctx, isConstrained) { 
        if (!ctx) return;
        ctx.strokeStyle = color; ctx.lineWidth = lineWidth; 
        let selX1 = Math.min(x1, x2), selY1 = Math.min(y1, y2);
        let selWidth = Math.abs(x2 - x1), selHeight = Math.abs(y2 - y1);
        if (selWidth < 1 || selHeight < 1) return; 
        if (shapeType === "Rectangle") { ctx.strokeRect(selX1, selY1, selWidth, selHeight); }
        else if (shapeType === "Circle") {
            ctx.beginPath();
            ctx.ellipse(selX1 + selWidth / 2, selY1 + selHeight / 2, selWidth / 2, selHeight / 2, 0, 0, 2 * Math.PI);
            ctx.stroke();
        }
    }
    
    confirmSelectionBtn.addEventListener('click', async () => {
        if (!currentSelection || !mainImage.src || mainImage.src.includes("alt=") || currentDisplayWidth === 0) {
            updateStatus("Error: No image or valid selection."); return;
        }
        updateStatus("Processing selection...");
        confirmSelectionBtn.disabled = true; applyToFolderBtn.disabled = true; 
        const payload = {
            selection: currentSelection, shape: getSelectedShape(), color: getSelectedColor(),
            lineWidth: getSelectedLineWidth(), 
            displayWidth: currentDisplayWidth, displayHeight: currentDisplayHeight, 
        };
        try { 
            const response = await fetch('/process_selection', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || `HTTP error ${response.status}`);
            let fullMessage = result.message || "Processing complete.";
            if (result.annotated_image_url && result.cropped_image_url) {
                fullMessage += `<br/>Access: <a href="/output/${result.annotated_image_url}" target="_blank">Annotated</a> | <a href="/output/${result.cropped_image_url}" target="_blank">Cropped</a>. (Params: ${result.params_file})`;
            }
            updateStatus(fullMessage, true); 
            if (result.is_folder_mode) { applyToFolderBtn.classList.remove('hidden'); applyToFolderBtn.disabled = false; }
            else { applyToFolderBtn.classList.add('hidden'); }
        } catch (error) { updateStatus(`Error processing: ${error.message}`); console.error('Processing error:', error);
        } finally {
            if (currentSelection && mainImage.src && !mainImage.src.includes("alt=")) confirmSelectionBtn.disabled = false;
        }
    });

    applyToFolderBtn.addEventListener('click', async () => { 
        updateStatus("Applying to server folder...");
        applyToFolderBtn.disabled = true; confirmSelectionBtn.disabled = true;
        try {
            const response = await fetch('/apply_to_folder', { method: 'POST' });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || `HTTP error ${response.status}`);
            let fullMessage = result.message || "Folder processing complete.";
            if (result.details && result.details.length > 0) {
                fullMessage += "<br/>Log:<br/><small>" + result.details.join("<br/>") + "</small>";
            }
            updateStatus(fullMessage, true); 
        } catch (error) { updateStatus(`Error applying to folder: ${error.message}`); console.error('Folder apply error:', error);
        } finally {
            applyToFolderBtn.disabled = false; 
            if (currentSelection && mainImage.src && !mainImage.src.includes("alt=")) confirmSelectionBtn.disabled = false;
        }
    });
    function updateStatus(message, allowHtml = false) { 
        if (allowHtml) statusDiv.innerHTML = message; else statusDiv.textContent = message;
        console.log("Status:", message);
    }

    window.addEventListener('resize', setupCanvases); 
    fetchAndDisplayDirs(); 
    setupCanvases(); 
    mainImage.alt = "Load an image locally, or browse server images on the left."; 
});