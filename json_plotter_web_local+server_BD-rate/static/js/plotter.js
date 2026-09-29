// plotter.js

document.addEventListener('DOMContentLoaded', () => {
    // DOM Element Getters
    const folderPathInput = document.getElementById('folderPath');
    const filenameRegexInput = document.getElementById('filenameRegex');
    const loadKeysBtn = document.getElementById('loadKeysBtn');
    const keySelectionArea = document.getElementById('keySelectionArea');
    const xKeySelect = document.getElementById('xKey');
    const yKeySelect = document.getElementById('yKey');
    const plotBtn = document.getElementById('plotBtn');
    const plotDiv = document.getElementById('plotDiv');
    const statusDiv = document.getElementById('status');

    const currentEffectiveBaseDisplay = document.getElementById('currentEffectiveBaseDisplay');
    const browseBaseFoldersBtn = document.getElementById('browseBaseFoldersBtn');
    const serverDirectoryBrowserContainer = document.getElementById('serverDirectoryBrowserContainer');
    const currentBrowsingPathDisplay = document.getElementById('currentBrowsingPathDisplay');
    const serverDirBrowser = document.getElementById('serverDirBrowser');
    const setThisFolderAsBaseBtn = document.getElementById('setThisFolderAsBaseBtn');
    
    const localJsonFileInput = document.getElementById('localJsonFileInput');
    const localJsonFolderInput = document.getElementById('localJsonFolderInput');
    const localFilesStatus = document.getElementById('localFilesStatus');

    const methodSelectionContainer = document.getElementById('methodSelectionContainer');
    const methodCheckboxListUl = document.getElementById('methodCheckboxList');
    const selectAllMethodsBtn = document.getElementById('selectAllMethodsBtn');
    const deselectAllMethodsBtn = document.getElementById('deselectAllMethodsBtn');

    const dataTableContainer = document.getElementById('dataTableContainer');
    const dataTableHeaderRow = document.getElementById('dataTableHeaderRow');
    const dataTableBody = document.getElementById('dataTableBody');
    
    // Global State
    let currentAvailableKeys = new Set(); 
    let serverMethodsForSelectionStore = []; 
    let pathCurrentlyBeingBrowsedForBase = ''; 

    // --- Base Folder Browsing Logic ---
    browseBaseFoldersBtn.addEventListener('click', () => {
        serverDirectoryBrowserContainer.classList.toggle('hidden');
        if (!serverDirectoryBrowserContainer.classList.contains('hidden')) {
            fetchServerDirsForBase(''); 
        }
    });

    async function fetchServerDirsForBase(relativePathWithinBrowsableRoot = '') {
        serverDirBrowser.innerHTML = '<p>Loading server directories...</p>';
        setThisFolderAsBaseBtn.disabled = true; 
        try {
            const response = await fetch('/browse_server_dirs_for_base', { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify({ path: relativePathWithinBrowsableRoot }) 
            });
            const data = await response.json();
            if (!response.ok || data.error) throw new Error(data.error || `HTTP error ${response.status}`);
            
            pathCurrentlyBeingBrowsedForBase = data.current_browsing_path_rel; 
            currentBrowsingPathDisplay.textContent = `Server Browsing at: /${pathCurrentlyBeingBrowsedForBase || '(Configured Browsable Root)'}`;
            let html = '<ul>';
            if (!data.directories || data.directories.length === 0) {
                html += '<li><em>(No further subdirectories here.)</em></li>';
            } else {
                data.directories.forEach(item => {
                    html += `<li data-path="${item.path}" data-type="${item.type}" class="${item.type}" title="Navigate to or select '${item.name}'">${item.name}</li>`;
                });
            }
            html += '</ul>'; 
            serverDirBrowser.innerHTML = html;
            setThisFolderAsBaseBtn.disabled = false; 
        } catch (error) {
            serverDirBrowser.innerHTML = `<p style="color:red;">Error listing server directories: ${error.message}</p>`;
            currentBrowsingPathDisplay.textContent = "Error loading directories.";
            console.error("Error in fetchServerDirsForBase JS:", error);
        }
    }

    serverDirBrowser.addEventListener('click', (event) => {
        const targetLi = event.target.closest('li');
        if (targetLi && targetLi.dataset.path !== undefined && targetLi.dataset.type) {
            fetchServerDirsForBase(targetLi.dataset.path); 
        }
    });

    setThisFolderAsBaseBtn.addEventListener('click', async () => {
        const pathToSendToServerRel = pathCurrentlyBeingBrowsedForBase;
        updateStatus(`Setting base folder to: .../${pathToSendToServerRel || '(Allowed Root)'}...`);
        try {
            const response = await fetch('/set_base_json_folder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ selected_path_rel: pathToSendToServerRel })
            });
            const data = await response.json();
            if (!response.ok || data.error) throw new Error(data.error || `HTTP error ${response.status}`);
            updateStatus(data.message);
            currentEffectiveBaseDisplay.textContent = `.../${data.selected_base_json_folder_rel_for_display || '(Top Browsable Area)'}`;
            serverDirectoryBrowserContainer.classList.add('hidden'); 
            resetUIDueToBaseChange();
        } catch (error) {
            updateStatus(`Error setting base folder: ${error.message}`);
            console.error("Set Base Error in JS:", error);
        }
    });

    function resetUIDueToBaseChange(){
        keySelectionArea.classList.add('hidden'); 
        methodSelectionContainer.classList.add('hidden'); 
        dataTableContainer.classList.add('hidden');
        xKeySelect.innerHTML = ''; yKeySelect.innerHTML = ''; methodCheckboxListUl.innerHTML = '';
        currentAvailableKeys.clear(); 
        serverMethodsForSelectionStore = []; 
        updateMethodAndKeySelectorsUI(); 
        plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Base folder changed. Please "Scan All Data" again.</p>';
        checkPlotButtonState();
    }

    localJsonFileInput.addEventListener('change', (e) => { uploadLocalFilesToServer(e.target.files, false); });
    localJsonFolderInput.addEventListener('change', (e) => { uploadLocalFilesToServer(e.target.files, true); });

    async function uploadLocalFilesToServer(files, isFolderUpload) {
        if (!files || files.length === 0) return;
        localFilesStatus.textContent = `Uploading ${files.length} local item(s) to server...`;
        loadKeysBtn.disabled = true; 
        plotBtn.disabled = true; 

        const formData = new FormData();
        let jsonFileCountInUpload = 0;
        for (const file of files) {
            if (file.name.toLowerCase().endsWith('.json')) {
                const formKey = (isFolderUpload && file.webkitRelativePath) ? file.webkitRelativePath : file.name;
                formData.append(formKey, file, file.name);
                jsonFileCountInUpload++;
            } else {
                console.warn(`Skipping non-JSON local file during upload prep: ${file.name}`);
            }
        }

        if (jsonFileCountInUpload === 0) {
            localFilesStatus.textContent = "No JSON files found in local selection to upload.";
            loadKeysBtn.disabled = false;
            return;
        }

        try {
            const response = await fetch('/upload_local_jsons', {
                method: 'POST',
                body: formData 
            });
            const data = await response.json();
            if (!response.ok || data.error) {
                throw new Error(data.error || `Upload HTTP error ${response.status}`);
            }
            let msg = data.message || `${data.uploaded_count || 0} files processed by server.`;
            if(data.errors && data.errors.length > 0) msg += ` Some errors occurred: ${data.errors.join(', ')}`;
            localFilesStatus.textContent = msg;
            updateStatus("Local files uploaded. 'Scan All Data' to include them in analysis.");
            methodSelectionContainer.classList.add('hidden'); 
            keySelectionArea.classList.add('hidden');
            plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Local files uploaded. Click "Scan All Data" to update available series and keys.</p>';
        } catch (error) {
            localFilesStatus.textContent = `Error uploading local files: ${error.message}`;
            console.error("Local Upload JS Error:", error);
        } finally {
            localJsonFileInput.value = ''; 
            localJsonFolderInput.value = '';
            loadKeysBtn.disabled = false; 
            checkPlotButtonState();
        }
    }
    
    loadKeysBtn.addEventListener('click', async () => {
        const subFolder = folderPathInput.value.trim(); 
        const regexStr = filenameRegexInput.value.trim() || filenameRegexInput.placeholder || '.*rp_summary\\.json$';
        
        updateStatus("Scanning all data sources (server & session uploads)..."); 
        loadKeysBtn.disabled = true;
        keySelectionArea.classList.add('hidden'); 
        methodSelectionContainer.classList.add('hidden');
        dataTableContainer.classList.add('hidden');
        plotDiv.innerHTML = '<p style="color:#777;text-align:center;">Scanning all data sources on server...</p>';
        xKeySelect.innerHTML='<option value="">Scanning...</option>'; 
        yKeySelect.innerHTML='<option value="">Scanning...</option>';
        methodCheckboxListUl.innerHTML = '';
        currentAvailableKeys.clear();
        serverMethodsForSelectionStore = [];

        try {
            const resp = await fetch('/list_json_keys', { 
                method: 'POST', headers:{'Content-Type':'application/json'}, 
                body:JSON.stringify({ folder_path: subFolder, filename_regex: regexStr }) 
            });
            const data = await resp.json();
            if (!resp.ok || data.error) {
                if (data.error && resp.status === 404) {
                     updateStatus(data.error); 
                } else {
                    throw new Error(data.error || `Server error during scan: ${resp.status}`);
                }
            } else { 
                updateStatus(data.message || "Server scan complete.");
            }
            
            (data.available_keys || []).forEach(k => currentAvailableKeys.add(k));
            serverMethodsForSelectionStore = data.methods_for_selection || [];
            
            updateMethodAndKeySelectorsUI(data.default_x_key, data.default_y_key);

        } catch (err) { 
            updateStatus(`Error scanning data: ${err.message}`); 
            console.error("Scan Error in JS:", err);
            xKeySelect.innerHTML='<option value="">Error</option>'; 
            yKeySelect.innerHTML='<option value="">Error</option>';
            methodCheckboxListUl.innerHTML = '<li>Error loading series.</li>';
            plotDiv.innerHTML = `<p style="color:red;text-align:center;">Failed to scan data: ${err.message}</p>`;
        } finally { 
            loadKeysBtn.disabled = false; 
            checkPlotButtonState(); 
        }
    });

    function updateMethodAndKeySelectorsUI(defaultX = null, defaultY = null) {
        const allMethodsUI = [...serverMethodsForSelectionStore]; 
        allMethodsUI.sort((a, b) => a.name.localeCompare(b.name));
        
        populateMethodCheckboxes(allMethodsUI);
        if (allMethodsUI.length > 0) {
            methodSelectionContainer.classList.remove('hidden');
        } else {
            methodSelectionContainer.classList.add('hidden');
        }
        
        const sortedKeys = Array.from(currentAvailableKeys).sort();
        populateKeySelectors(sortedKeys, defaultX, defaultY); 
        checkPlotButtonState();
    }

    function populateMethodCheckboxes(methods) {
        methodCheckboxListUl.innerHTML = ''; 
        if (!methods || methods.length === 0) { 
            methodCheckboxListUl.innerHTML = '<li>No data series identified.</li>'; 
            checkPlotButtonState();
            return; 
        }
        methods.forEach(method => {
            const li = document.createElement('li'); 
            const cb = document.createElement('input'); 
            cb.type = 'checkbox';
            const safeIdPart = method.id.replace(/\W/g, '_'); 
            cb.id = `method_cb_${safeIdPart}_${Math.random().toString(16).slice(2)}`; 
            cb.value = method.id; 
            cb.checked = true; 
            cb.addEventListener('change', checkPlotButtonState); 
            
            const lbl = document.createElement('label'); 
            lbl.htmlFor = cb.id; 
            lbl.textContent = method.name; 
            
            li.appendChild(cb); 
            li.appendChild(lbl); 
            methodCheckboxListUl.appendChild(li);
        });
        checkPlotButtonState();
    }

    selectAllMethodsBtn.addEventListener('click', () => {
        methodCheckboxListUl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
        checkPlotButtonState();
    });
    deselectAllMethodsBtn.addEventListener('click', () => {
        methodCheckboxListUl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        checkPlotButtonState();
    });
    
    function populateKeySelectors(keys, defaultX = null, defaultY = null) { 
        xKeySelect.innerHTML = '<option value="">-- Select X Metric --</option>';
        yKeySelect.innerHTML = '<option value="">-- Select Y Metric --</option>';
        
        xKeySelect.removeEventListener('change', checkPlotButtonState);
        yKeySelect.removeEventListener('change', checkPlotButtonState);

        if (!keys || keys.length === 0) {
            checkPlotButtonState();
            return;
        }

        keys.forEach(key => {
            const optX = document.createElement('option'); optX.value = key; optX.textContent = key; 
            xKeySelect.appendChild(optX);
            const optY = document.createElement('option'); optY.value = key; optY.textContent = key; 
            yKeySelect.appendChild(optY);
        });

        if (defaultX && keys.includes(defaultX)) xKeySelect.value = defaultX;
        else if (keys.includes("filesize(MB)")) xKeySelect.value = "filesize(MB)";
        else if (keys.includes("size")) xKeySelect.value = "size";
        
        if (defaultY && keys.includes(defaultY)) yKeySelect.value = defaultY;
        else if (keys.includes("psnr")) yKeySelect.value = "psnr";

        xKeySelect.addEventListener('change', checkPlotButtonState);
        yKeySelect.addEventListener('change', checkPlotButtonState);
        checkPlotButtonState();
    }

    function checkPlotButtonState() {
        const xKeySelected = xKeySelect.value && xKeySelect.selectedIndex > 0;
        const yKeySelected = yKeySelect.value && yKeySelect.selectedIndex > 0;
        const methodsSelectedCount = methodCheckboxListUl.querySelectorAll('input[type="checkbox"]:checked').length;
        const hasMethodsToList = methodCheckboxListUl.querySelectorAll('input[type="checkbox"]').length > 0;
        const hasKeysToList = xKeySelect.options.length > 1; 

        if (hasMethodsToList && hasKeysToList) {
            keySelectionArea.classList.remove('hidden');
        } else {
            keySelectionArea.classList.add('hidden');
        }

        plotBtn.disabled = !(xKeySelected && yKeySelected && methodsSelectedCount > 0);
    }

    // --- Plotting Logic ---
    plotBtn.addEventListener('click', async () => {
        const subFolder = folderPathInput.value.trim(); 
        const regex = filenameRegexInput.value.trim() || filenameRegexInput.placeholder || '.*rp_summary\\.json$';
        const xK = xKeySelect.value; const yK = yKeySelect.value;
        const selMethodIds = Array.from(methodCheckboxListUl.querySelectorAll('input:checked')).map(cb => cb.value);

        if (!xK || xKeySelect.selectedIndex === 0 ) { updateStatus("Error: Select an X-Axis metric."); return; }
        if (!yK || yKeySelect.selectedIndex === 0 ) { updateStatus("Error: Select a Y-Axis metric."); return; }
        if (selMethodIds.length === 0) { updateStatus("Error: No data series selected."); return; }
        
        updateStatus("Fetching & processing data for output..."); 
        dataTableContainer.classList.add('hidden'); dataTableBody.innerHTML = ''; dataTableHeaderRow.innerHTML = '';
        plotDiv.innerHTML = '<p style="color:#777;text-align:center;">Generating table & plot...</p>';
        plotBtn.disabled = true;
        
        try {
            const response = await fetch('/get_plot_data', { 
                method: 'POST', headers:{'Content-Type':'application/json'}, 
                body:JSON.stringify({ 
                    folder_path:subFolder, filename_regex:regex, 
                    x_key:xK, y_key:yK, 
                    selected_methods:selMethodIds 
                }) 
            });
            const plotDataResp = await response.json(); 
            if (!response.ok || plotDataResp.error) throw new Error(plotDataResp.error || `HTTP error ${response.status}`);
            
            // console.log("Data from server for plot/table:", plotDataResp); // Good for debugging

            if (plotDataResp.tabular_data && plotDataResp.tabular_data.length > 0) {
                renderDataTable(plotDataResp.tabular_data, xK, yK); 
                dataTableContainer.classList.remove('hidden');
            } else {
                 dataTableContainer.classList.add('hidden');
                 console.log("No tabular data returned or it was empty.");
            }

            if (plotDataResp.plot_traces && Object.keys(plotDataResp.plot_traces).length > 0) {
                renderPlot(plotDataResp); // Pass the whole response
                let tp=0; Object.values(plotDataResp.plot_traces).forEach(t=>tp+=(t.x?t.x.length:0)); 
                updateStatus(`Output generated. Displaying ${tp} points across ${Object.keys(plotDataResp.plot_traces).length} series.`);
            } else { 
                updateStatus("No data points to plot for the current selection.");
                plotDiv.innerHTML='<p style="color:#777;text-align:center;">No data available to plot.</p>'; 
            }
        } catch (err) { 
            updateStatus(`Error during output generation: ${err.message}`); console.error("OutputGenErr:",err);
            dataTableContainer.classList.add('hidden'); 
            plotDiv.innerHTML = `<p style="color:red;text-align:center;">Error generating output: ${err.message}</p>`;
        } finally {
            checkPlotButtonState();
        }
    });
    
    // **** IMPLEMENTED renderDataTable ****
    function renderDataTable(tabularData, xKey, yKey) {
        dataTableHeaderRow.innerHTML = ''; // Clear previous headers
        dataTableBody.innerHTML = '';    // Clear previous body

        if (!tabularData || tabularData.length === 0) {
            const row = dataTableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 5; // Adjust if you change the number of columns
            cell.textContent = "No data available for table.";
            dataTableContainer.classList.remove('hidden'); // Show container even if empty
            return;
        }

        // Define headers dynamically or statically based on your data structure
        // Your Python backend sends these keys: "Method", "File", "Rate Point", xKey, yKey
        const headers = ["Method", "File", "Rate Point", xKey, yKey];
        headers.forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.textContent = headerText;
            dataTableHeaderRow.appendChild(headerCell);
        });

        tabularData.forEach(item => {
            const row = dataTableBody.insertRow();
            headers.forEach(header => { // Iterate using the defined headers to ensure order and all columns
                const cell = row.insertCell();
                let value = item[header]; // Access data using the header string as key
                
                // Basic formatting for numbers
                if (typeof value === 'number') {
                    // You might want more sophisticated formatting, e.g., to specific decimal places
                    cell.textContent = Number.isInteger(value) ? value : value.toFixed(4); // Example: 4 decimal places for floats
                } else {
                    cell.textContent = value !== undefined && value !== null ? value : 'N/A'; // Handle undefined or null
                }
            });
        });
        dataTableContainer.classList.remove('hidden'); // Make sure it's visible
    }

    // **** IMPLEMENTED renderPlot ****
    function renderPlot(plotDataResponse) {
        const traces = [];
        const plotTracesDict = plotDataResponse.plot_traces; // This is {"Method1": {x:[], y:[]}, "Method2": {x:[], y:[]}, ...}
        const xAxisLabel = plotDataResponse.x_axis_label;
        const yAxisLabel = plotDataResponse.y_axis_label;

        for (const methodName in plotTracesDict) {
            if (plotTracesDict.hasOwnProperty(methodName)) {
                const traceData = plotTracesDict[methodName]; // {x: [...], y: [...], hovertext: [...]}
                if (traceData.x && traceData.y && traceData.x.length > 0) { // Check if there's actual data
                    traces.push({
                        x: traceData.x,
                        y: traceData.y,
                        text: traceData.hovertext, // hovertext array from server
                        hoverinfo: 'text',    // Show only the content of 'text' on hover
                        mode: 'lines+markers',
                        type: 'scatter', // Use 'scattergl' for very large datasets
                        name: methodName  // This will be the legend entry
                    });
                }
            }
        }

        if (traces.length === 0) {
            plotDiv.innerHTML = '<p style="text-align:center;color:#777;">No plottable data points found for the selected series and keys.</p>';
            return;
        }

        const layout = {
            title: `${yAxisLabel} vs. ${xAxisLabel}`,
            xaxis: {
                title: xAxisLabel,
                // autotypenumbers: 'strict' // May help if numbers are sent as strings
            },
            yaxis: {
                title: yAxisLabel,
                // autotypenumbers: 'strict'
            },
            legend: {
                x: 0.99, 
                y: 0.01,
                xanchor: 'right',
                yanchor: 'bottom',
                bgcolor: 'rgba(255,255,255,0.7)',
                bordercolor: '#000', 
                borderwidth: 1
            },
            margin: { l: 60, r: 30, b: 50, t: 50, pad: 4 } // Adjust margins for better look
        };
        
        Plotly.newPlot(plotDiv, traces, layout);
    }
    
    function updateStatus(message) { statusDiv.textContent = message; console.log("STATUS:", message); }
    
    function initializeBaseFolderDisplay() { 
        // This should ideally fetch the initial default base path from server,
        // or server could render it into a hidden field or a JS var.
        // For now, keeping as is, relies on user interaction or default behavior.
        currentEffectiveBaseDisplay.textContent = "Default Server Path (see config)"; 
    }
    
    initializeBaseFolderDisplay();
    checkPlotButtonState(); // Initial check
});