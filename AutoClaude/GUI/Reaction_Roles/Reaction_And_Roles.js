window.REACTION_ROLES_CONTENT_HTML = `
<style>
    .rr-tab-btn {
        padding: 8px 24px;
        font-size: 14px;
        font-weight: 600;
        color: #949ba4;
        border-bottom: 2px solid transparent;
        cursor: pointer;
        transition: all 0.2s;
    }
    .rr-tab-btn.active {
        color: #fff;
        background-color: #35373c;
        border-radius: 4px;
    }
    .rr-frame {
        background-color: #1e1f22;
        border: 1px solid #2b2d31;
        border-radius: 8px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: border-color 0.2s;
        min-height: 60px;
    }
    .rr-frame:hover {
        border-color: #3f4147;
    }
    .emoji-trigger {
        font-size: 28px;
        cursor: pointer;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        background: #2b2d31;
        flex-shrink: 0;
    }
    .emoji-trigger:hover {
        background: #35373c;
    }
    .role-select-btn {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #2b2d31;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #949ba4;
        border: 1px solid #3f4147;
    }
    .role-select-btn:hover {
        background: #35373c;
        color: #fff;
    }
    .role-label {
        flex: 1;
        font-size: 16px;
        color: #dbdee1;
        padding: 6px 12px;
        border: 1px solid #3f4147;
        border-radius: 6px;
        min-height: 38px;
        display: flex;
        align-items: center;
    }
    .option-input {
        flex: 1;
        font-size: 16px;
        color: #dbdee1;
        padding: 6px 12px;
        border: 1px solid #3f4147;
        border-radius: 6px;
        background: transparent;
        outline: none;
        width: 100%;
    }
    .option-input:focus {
        border-color: #5865f2;
    }
    .rr-trash {
        color: #ed4245;
        cursor: pointer;
        opacity: 0.6;
        transition: opacity 0.2s;
        flex-shrink: 0;
    }
    .rr-trash:hover {
        opacity: 1;
    }
    .add-btn {
        border: 1px dashed #4e5058;
        border-radius: 8px;
        padding: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        color: #b5bac1;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
    }
    .add-btn:hover {
        background: rgba(255,255,255,0.02);
        border-color: #b5bac1;
    }
    
    #emoji_picker_popup {
        position: fixed;
        z-index: 1000;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        display: none;
    }
    
    /* Shared Global Role Selector Styling */
    .role-selector-panel {
        position: absolute;
        top: 100%;
        left: 0;
        width: 260px;
        background: #111214;
        border: 1px solid #2b2d31;
        border-radius: 8px;
        z-index: 500;
        display: none;
        padding: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .role-search-input {
        width: 100%;
        background: #1e1f22;
        border: 1px solid #3f4147;
        border-radius: 4px;
        padding: 6px 10px;
        color: #fff;
        font-size: 13px;
        margin-bottom: 8px;
        outline: none;
    }
    .role-list-container {
        max-height: 180px;
        overflow-y: auto;
    }
    .role-item {
        padding: 8px 10px;
        font-size: 13px;
        cursor: pointer;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #dbdee1;
    }
    .role-item:hover {
        background: #35373c;
        color: #fff;
    }
    .create-role-trigger {
        padding: 8px 10px;
        font-size: 13px;
        cursor: pointer;
        color: #5865f2;
        border-top: 1px solid #2b2d31;
        margin-top: 4px;
    }
</style>

<div class="config-content space-y-6">
    <!-- Tabs -->
    <div class="flex gap-2 p-1 bg-[#111214] rounded-lg w-fit">
        <div id="rr_tab_emoji" class="rr-tab-btn active" onclick="switchRrTab('emoji')">Emoji</div>
        <div id="rr_tab_dropdown" class="rr-tab-btn" onclick="switchRrTab('dropdown')">Dropdown</div>
    </div>

    <!-- Toggle -->
    <div class="flex items-center gap-3">
        <label class="switch">
            <input type="checkbox" id="rr_multiple_toggle" checked>
            <span class="slider"></span>
        </label>
        <span class="text-sm text-gray-300">Allow members to pick up roles from multiple reactions</span>
    </div>

    <!-- Emoji Content -->
    <div id="rr_content_emoji" class="space-y-3">
        <div id="emoji_rows_container" class="space-y-2"></div>
        <div class="add-btn" onclick="addEmojiRow()">
            <div class="w-6 h-6 rounded-full bg-[#2b2d31] flex items-center justify-center">
                <i data-lucide="plus" class="w-4 h-4"></i>
            </div>
            <span>Add new reaction</span>
        </div>
    </div>

    <!-- Dropdown Content -->
    <div id="rr_content_dropdown" class="hidden space-y-4">
        <div>
            <label class="config-label">Dropdown placeholder</label>
            <input type="text" class="option-input w-full mt-1" value="" placeholder="Your option" id="rr_dropdown_placeholder">
        </div>
        
        <div id="dropdown_rows_container" class="space-y-2"></div>
        
        <div class="add-btn" onclick="addDropdownRow()">
            <div class="w-6 h-6 rounded-full bg-[#2b2d31] flex items-center justify-center">
                <i data-lucide="plus" class="w-4 h-4"></i>
            </div>
            <span>Add new option</span>
        </div>
    </div>
</div>

<!-- Emoji Picker Popup -->
<div id="emoji_picker_popup">
    <emoji-picker class="dark"></emoji-picker>
</div>
`;

window.rrState = {
    mode: 'emoji',
    emojiRows: [
        { id: 'e1', emoji: '🙌', roleId: null, roleName: 'Select a role' },
        { id: 'e2', emoji: '🫡', roleId: null, roleName: 'Select a role' }
    ],
    dropdownRows: [
        { id: 'd1', roleId: null, roleName: 'Select a role', label: '' }
    ]
};

window.initializeReactionRolesContent = async function() {
    console.log("[SYSTEM] Reaction Roles Content Section Initialized");
    if (window.lucide) window.lucide.createIcons();
    
    // Sync local state if window.savedReactionData exists
    if (window.savedReactionData) {
        const d = window.savedReactionData;
        window.rrState.mode = d.type || 'emoji';
        
        if (d.emoji_rows && d.emoji_rows.length > 0) window.rrState.emojiRows = d.emoji_rows;
        if (d.dropdown_rows && d.dropdown_rows.length > 0) window.rrState.dropdownRows = d.dropdown_rows;
        
        // Restore toggle
        const toggle = document.getElementById('rr_multiple_toggle');
        if (toggle) toggle.checked = d.allow_multiple !== false; // Default true

        // Restore placeholder
        const placeholderInput = document.getElementById('rr_dropdown_placeholder');
        if (placeholderInput) placeholderInput.value = d.dropdown_placeholder || '';
        
        // Ensure UI reflects saved mode
        switchRrTab(window.rrState.mode);
    }
    
    await loadRoles(); 
    renderRrContent();
    
    // Global click listener for closing popups
    document.addEventListener('click', (e) => {
        const picker = document.getElementById('emoji_picker_popup');
        if (picker && !picker.contains(e.target) && !e.target.closest('.emoji-trigger')) {
            picker.style.display = 'none';
        }
        
        // Close role selectors
        if (!e.target.closest('.role-select-container')) {
            document.querySelectorAll('.role-selector-panel').forEach(d => d.style.display = 'none');
        }
    });
    
    const pickerElement = document.querySelector('emoji-picker');
    if (pickerElement) {
        pickerElement.addEventListener('emoji-click', event => {
            const emoji = event.detail.unicode;
            if (window.currentRrRowId) {
                const row = window.rrState.emojiRows.find(r => r.id === window.currentRrRowId);
                if (row) {
                    row.emoji = emoji;
                    renderRrContent();
                }
            }
            document.getElementById('emoji_picker_popup').style.display = 'none';
        });
    }
};

window.switchRrTab = function(mode) {
    window.rrState.mode = mode;
    document.getElementById('rr_tab_emoji').classList.toggle('active', mode === 'emoji');
    document.getElementById('rr_tab_dropdown').classList.toggle('active', mode === 'dropdown');
    
    document.getElementById('rr_content_emoji').classList.toggle('hidden', mode !== 'emoji');
    document.getElementById('rr_content_dropdown').classList.toggle('hidden', mode !== 'dropdown');
    
    renderRrContent();
};

window.renderRrContent = function() {
    if (window.rrState.mode === 'emoji') {
        const container = document.getElementById('emoji_rows_container');
        container.innerHTML = window.rrState.emojiRows.map(row => `
            <div class="rr-frame" data-id="${row.id}">
                <div class="emoji-trigger" onclick="openEmojiPicker(event, '${row.id}')">${row.emoji}</div>
                <div class="relative role-select-container flex-1 flex items-center gap-3">
                    <div class="role-select-btn" onclick="toggleRrRoleSelector(event, '${row.id}')">
                        <i data-lucide="plus" class="w-4 h-4"></i>
                    </div>
                    <div class="role-label">${row.roleName}</div>
                    
                    <div id="role_selector_${row.id}" class="role-selector-panel custom-scrollbar">
                        <input type="text" class="role-search-input" placeholder="Search roles..." oninput="filterRrRoles('${row.id}', this.value)">
                        <div class="role-list-container" id="role_list_${row.id}">
                            ${renderRoleListHtml(row.id)}
                        </div>
                        <div class="create-role-trigger" onclick="alert('Role creation form coming soon')">+ Create new role</div>
                    </div>
                </div>
                <i data-lucide="trash-2" class="rr-trash w-5 h-5" onclick="deleteRrRow('${row.id}')"></i>
            </div>
        `).join('');
    } else {
        const container = document.getElementById('dropdown_rows_container');
        container.innerHTML = window.rrState.dropdownRows.map(row => `
            <div class="rr-frame" data-id="${row.id}">
                <div class="relative role-select-container flex-[0.5] flex items-center gap-3">
                    <div class="role-select-btn" onclick="toggleRrRoleSelector(event, '${row.id}')">
                        <i data-lucide="plus" class="w-4 h-4"></i>
                    </div>
                    <div class="role-label">${row.roleName}</div>
                    
                    <div id="role_selector_${row.id}" class="role-selector-panel custom-scrollbar">
                        <input type="text" class="role-search-input" placeholder="Search roles..." oninput="filterRrRoles('${row.id}', this.value)">
                        <div class="role-list-container" id="role_list_${row.id}">
                            ${renderRoleListHtml(row.id)}
                        </div>
                    </div>
                </div>
                <div class="flex-[0.5]">
                    <input type="text" class="option-input" 
                           value="${row.label}" placeholder="Your option" 
                           oninput="updateRrRowLabel('${row.id}', this.value)">
                </div>
                <i data-lucide="trash-2" class="rr-trash w-5 h-5" onclick="deleteRrRow('${row.id}')"></i>
            </div>
        `).join('');
    }
    if (window.lucide) window.lucide.createIcons();
};

function renderRoleListHtml(rowId, filter = '') {
    const q = filter.toLowerCase();
    const filtered = window.rolesCache.filter(r => r.name.toLowerCase().includes(q));
    
    if (filtered.length === 0) return '<div class="p-2 text-xs text-gray-500">No roles found</div>';
    
    return filtered.map(r => `
        <div class="role-item" onclick="selectRrRole('${rowId}', '${r.id}', '${r.name}')">
            <span class="w-3 h-3 rounded-full" style="background-color: #${r.color.toString(16).padStart(6, '0')}"></span>
            ${r.name}
        </div>
    `).join('');
}

window.filterRrRoles = function(rowId, val) {
    const container = document.getElementById(`role_list_${rowId}`);
    if (container) container.innerHTML = renderRoleListHtml(rowId, val);
};

window.openEmojiPicker = function(event, rowId) {
    event.stopPropagation();
    window.currentRrRowId = rowId;
    const picker = document.getElementById('emoji_picker_popup');
    const rect = event.target.getBoundingClientRect();
    
    picker.style.display = 'block';
    picker.style.top = (rect.bottom + 10) + 'px';
    picker.style.left = rect.left + 'px';
};

window.toggleRrRoleSelector = function(event, rowId) {
    event.stopPropagation();
    const panel = document.getElementById(`role_selector_${rowId}`);
    const isOpen = panel.style.display === 'block';
    document.querySelectorAll('.role-selector-panel').forEach(p => p.style.display = 'none');
    panel.style.display = isOpen ? 'none' : 'block';
    
    if (!isOpen) {
        const input = panel.querySelector('input');
        if (input) {
            input.value = '';
            input.focus();
            window.filterRrRoles(rowId, '');
        }
    }
};

window.selectRrRole = function(rowId, roleId, roleName) {
    const list = window.rrState.mode === 'emoji' ? window.rrState.emojiRows : window.rrState.dropdownRows;
    const row = list.find(r => r.id === rowId);
    if (row) {
        row.roleId = roleId;
        row.roleName = roleName;
        renderRrContent();
    }
};

window.deleteRrRow = function(rowId) {
    const list = window.rrState.mode === 'emoji' ? window.rrState.emojiRows : window.rrState.dropdownRows;
    if (list.length <= 1) return;
    
    if (window.rrState.mode === 'emoji') {
        window.rrState.emojiRows = window.rrState.emojiRows.filter(r => r.id !== rowId);
    } else {
        window.rrState.dropdownRows = window.rrState.dropdownRows.filter(r => r.id !== rowId);
    }
    renderRrContent();
};

window.addEmojiRow = function() {
    window.rrState.emojiRows.push({ id: 'e' + Date.now(), emoji: '😀', roleId: null, roleName: 'Select a role' });
    renderRrContent();
};

window.addDropdownRow = function() {
    window.rrState.dropdownRows.push({ id: 'd' + Date.now(), roleId: null, roleName: 'Select a role', label: '' });
    renderRrContent();
};

window.updateRrRowLabel = function(rowId, val) {
    const row = window.rrState.dropdownRows.find(r => r.id === rowId);
    if (row) row.label = val;
};