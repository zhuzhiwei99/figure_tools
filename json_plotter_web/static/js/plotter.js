document.addEventListener('DOMContentLoaded', () => {
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
    
    const methodSelectionContainer = document.getElementById('methodSelectionContainer');
    const methodCheckboxListUl = document.getElementById('methodCheckboxList');
    const selectAllMethodsBtn = document.getElementById('selectAllMethodsBtn');
    const deselectAllMethodsBtn = document.getElementById('deselectAllMethodsBtn');

    const dataTableContainer = document.getElementById('dataTableContainer');
    const dataTableHeaderRow = document.getElementById('dataTableHeaderRow');
    const dataTableBody = document.getElementById('dataTableBody');
    
    let currentAvailableKeys = [];
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
            currentBrowsingPathDisplay.textContent = `Server Browsing at: /${pathCurrentlyBeingBrowsedForBase || '(Allowed Root)'}`;
            let html = '<ul>';
            if (!data.directories || data.directories.length === 0) {
                html += '<li><em>(No further subdirectories here)</em></li>';
            } else {
                data.directories.forEach(item => {
                    html += `<li data-path="${item.path}" data-type="${item.type}" class="${item.type}" title="Navigate or select '${item.name}'">${item.name}</li>`;
                });
            }
            html += '</ul>';
            serverDirBrowser.innerHTML = html;
            setThisFolderAsBaseBtn.disabled = false; 
        } catch (error) {
            serverDirBrowser.innerHTML = `<p style="color:red;">Error listing: ${error.message}</p>`;
            currentBrowsingPathDisplay.textContent = "Error loading directories.";
            console.error("Error in fetchServerDirsForBase:", error);
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
            currentEffectiveBaseDisplay.textContent = `.../${data.selected_base_json_folder_rel_for_display || '(Allowed Root)'}`;
            serverDirectoryBrowserContainer.classList.add('hidden'); 
            keySelectionArea.classList.add('hidden'); methodSelectionContainer.classList.add('hidden');
            dataTableContainer.classList.add('hidden');
            xKeySelect.innerHTML = ''; yKeySelect.innerHTML = ''; methodCheckboxListUl.innerHTML = '';
            plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Base folder changed. Scan Files again.</p>';
        } catch (error) {
            updateStatus(`Error setting base folder: ${error.message}`); console.error("Set base error:", error);
        }
    });

    // --- JSON Keys and Method Selection Logic ---
    loadKeysBtn.addEventListener('click', async () => {
        const subFolderPath = folderPathInput.value.trim(); 
        const filenameRegex = filenameRegexInput.value.trim();
        if (!filenameRegex) { updateStatus("Error: Filename Regex required."); return; }

        updateStatus("Scanning files for methods and metric keys...");
        loadKeysBtn.disabled = true;
        keySelectionArea.classList.add('hidden');
        methodSelectionContainer.classList.add('hidden'); 
        methodCheckboxListUl.innerHTML = '';
        dataTableContainer.classList.add('hidden');
        plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Scanning files on server...</p>';
        xKeySelect.innerHTML = '<option value="">Scanning...</option>';
        yKeySelect.innerHTML = '<option value="">Scanning...</option>';
        currentAvailableKeys = [];

        try {
            const response = await fetch('/list_json_keys', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: subFolderPath, filename_regex: filenameRegex })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || `Server error ${response.status}`);
            if (data.error) throw new Error(data.error); // Application specific error

            updateStatus(data.message || "Scan complete."); 
            currentAvailableKeys = data.available_keys || [];

            if (data.methods_for_selection && data.methods_for_selection.length > 0) {
                populateMethodCheckboxes(data.methods_for_selection);
                methodSelectionContainer.classList.remove('hidden');
            } else {
                methodSelectionContainer.classList.add('hidden');
                updateStatus(data.message + " No distinct methods/series found to select.");
            }
            
            populateKeySelectors(currentAvailableKeys);
            
            if (currentAvailableKeys.length > 0 && data.methods_for_selection && data.methods_for_selection.length > 0) {
                keySelectionArea.classList.remove('hidden');
                plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Select methods & metric keys, then "Generate Table & Plot".</p>';
            } else {
                keySelectionArea.classList.add('hidden');
                let plotMsg = data.message || "Scan complete.";
                if (!(data.methods_for_selection && data.methods_for_selection.length > 0)) plotMsg += " No methods found.";
                if (currentAvailableKeys.length === 0) plotMsg += " No suitable metric keys found.";
                plotDiv.innerHTML = `<p style="text-align:center;color:#777;">${plotMsg}</p>`;
            }
        } catch (error) {
            updateStatus(`Error during key/method scan: ${error.message}`); 
            console.error("Key/Method scan error:", error);
            xKeySelect.innerHTML = '<option value="">Error</option>'; yKeySelect.innerHTML = '<option value="">Error</option>';
            methodSelectionContainer.classList.add('hidden');
            plotDiv.innerHTML = `<p style="text-align:center;color:red;">Failed: ${error.message}</p>`;
        } finally {
            loadKeysBtn.disabled = false;
        }
    });

    function populateMethodCheckboxes(methods) {
        methodCheckboxListUl.innerHTML = ''; 
        if (!methods || methods.length === 0) {
            methodCheckboxListUl.innerHTML = '<li>No methods identified from files.</li>';
            return;
        }
        methods.forEach(method => {
            const li = document.createElement('li');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `method_cb_${method.id.replace(/[^a-zA-Z0-9-_]/g, '')}_${Math.random().toString(36).substr(2, 5)}`;
            checkbox.value = method.id; 
            checkbox.checked = true; 
            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = method.name; 
            li.appendChild(checkbox); li.appendChild(label);
            methodCheckboxListUl.appendChild(li);
        });
    }

    selectAllMethodsBtn.addEventListener('click', () => methodCheckboxListUl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true));
    deselectAllMethodsBtn.addEventListener('click', () => methodCheckboxListUl.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false));
    
    function populateKeySelectors(keys) { 
        xKeySelect.innerHTML = '<option value="">-- Select X Metric --</option>';
        yKeySelect.innerHTML = '<option value="">-- Select Y Metric --</option>';
        if (!keys || keys.length === 0) return;
        keys.forEach(key => {
            const optX = document.createElement('option'); optX.value = key; optX.textContent = key; xKeySelect.appendChild(optX);
            const optY = document.createElement('option'); optY.value = key; optY.textContent = key; yKeySelect.appendChild(optY);
        });
    }

    plotBtn.addEventListener('click', async () => {
        const subFolderPath = folderPathInput.value.trim(); 
        const filenameRegex = filenameRegexInput.value.trim();
        const selectedXKey = xKeySelect.value; const selectedYKey = yKeySelect.value;
        const selectedMethodIds = Array.from(methodCheckboxListUl.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);

        if (!selectedXKey || !selectedYKey) { updateStatus("Error: Select X & Y metric keys."); return; }
        if (selectedMethodIds.length === 0) { updateStatus("Error: No data series (methods) selected."); return; }
        
        updateStatus("Fetching data for table and plot...");
        dataTableContainer.classList.add('hidden'); 
        plotDiv.innerHTML = '<p style="text-align:center;color:#777;">Generating table & plot...</p>';
        try {
            const response = await fetch('/get_plot_data', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    folder_path: subFolderPath, filename_regex: filenameRegex,
                    x_key: selectedXKey, y_key: selectedYKey,
                    selected_methods: selectedMethodIds 
                })
            });
            const plotDataResponse = await response.json(); 
            if (!response.ok || plotDataResponse.error) throw new Error(plotDataResponse.error || `HTTP error ${response.status}`);
            
            if (plotDataResponse.tabular_data && plotDataResponse.tabular_data.length > 0) {
                renderDataTable(plotDataResponse.tabular_data, selectedXKey, selectedYKey);
                dataTableContainer.classList.remove('hidden');
            } else dataTableContainer.classList.add('hidden');

            if (plotDataResponse.plot_traces && Object.keys(plotDataResponse.plot_traces).length > 0) {
                renderPlot(plotDataResponse);
                let totalPoints = 0; Object.values(plotDataResponse.plot_traces).forEach(trace => totalPoints += (trace.x ? trace.x.length : 0) );
                updateStatus(`Table & Plot ready. ${totalPoints} points across ${Object.keys(plotDataResponse.plot_traces).length} methods.`);
            } else {
                updateStatus("No data points found to plot for the selected methods/keys.");
                plotDiv.innerHTML = '<p style="text-align:center;color:#777;">No data to plot.</p>';
            }
        } catch (error) {
            updateStatus(`Error generating output: ${error.message}`); console.error("Output gen error:", error);
            dataTableContainer.classList.add('hidden');
            plotDiv.innerHTML = `<p style="text-align:center;color:red;">Error: ${error.message}</p>`;
        }
    });

    function renderDataTable(tabularData, xKey, yKey) {
        dataTableHeaderRow.innerHTML = ''; dataTableBody.innerHTML = '';
        if (!tabularData || tabularData.length === 0) return;
        const headers = ["Method", "File", "Rate Point", xKey, yKey];
        headers.forEach(headerText => { const th = document.createElement('th'); th.textContent = headerText; dataTableHeaderRow.appendChild(th);});
        tabularData.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => { 
                const td = document.createElement('td'); let value = row[header];
                if ((header === xKey || header === yKey) && typeof value === 'number') value = parseFloat(value.toFixed(4));
                td.textContent = value !== undefined ? value : 'N/A'; tr.appendChild(td);
            });
            dataTableBody.appendChild(tr);
        });
    }

    function renderPlot(plotDataResponse) { 
    const traces = []; 
    const plotTraces = plotDataResponse.plot_traces;

    for (const methodName in plotTraces) {
        if (plotTraces.hasOwnProperty(methodName)) {
            const methodData = plotTraces[methodName];
            if (methodData.x && methodData.x.length > 0) {
                traces.push({ 
                    x: methodData.x, 
                    y: methodData.y, 
                    text: methodData.hovertext, 
                    mode: 'lines+markers', 
                    type: 'scatter', 
                    name: methodName 
                });
            }
        }
    }
    
    if (traces.length === 0) { 
        plotDiv.innerHTML = '<p style="text-align:center;color:#777;">No valid data series to plot after filtering.</p>'; 
        return; 
    }

    const layout = {
        title: `<b>${plotDataResponse.y_axis_label}</b> vs <b>${plotDataResponse.x_axis_label}</b>`,
        xaxis: { 
            title: plotDataResponse.x_axis_label, 
            automargin: true, 
            zeroline: true, 
            zerolinecolor: '#ccc', 
            zerolinewidth: 1 
        },
        yaxis: { 
            title: plotDataResponse.y_axis_label, 
            automargin: true, 
            zeroline: true, 
            zerolinecolor: '#ccc', 
            zerolinewidth: 1 
        },
        hovermode: 'closest', 
        legend: { 
            x: 1,       // Horizontal position: 1 means far right
            xanchor: 'right', // Anchor the legend's right edge to the x position
            y: 0,       // Vertical position: 0 means bottom
            yanchor: 'bottom', // Anchor the legend's bottom edge to the y position
            bgcolor: 'rgba(255,255,255,0.6)', // Optional: background color
            bordercolor: '#000', 
            borderwidth: 1
        }
    };
    
    Plotly.newPlot(plotDiv, traces, layout, {responsive: true});
}

    function updateStatus(message) { statusDiv.textContent = message; console.log("STATUS:", message); }
    
    function initializeBaseFolderDisplay() { currentEffectiveBaseDisplay.textContent = "Default (as per server config)"; }
    initializeBaseFolderDisplay();
});