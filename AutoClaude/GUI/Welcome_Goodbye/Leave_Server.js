window.LEAVE_SERVER_HTML = `
<!-- Feature 3 (Leave Server) -->
<div class="expandable-section active" id="section_leave">
    <div class="config-content">
        <div>
            <label class="config-label">Leave Message Channel <span
                    class="text-red-500">*</span></label>
            <div class="relative">
                <div class="dropdown-box" onclick="toggleLeaveDropdown('leave_channel_dropdown')">
                    <span id="leave_current_channel" class="flex items-center gap-2 text-gray-400">
                        <i data-lucide="hash" class="w-4 h-4"></i> Select a channel
                    </span>
                    <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
                </div>
                <div id="leave_channel_dropdown"
                    class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto">
                    <div class="p-2 text-sm text-gray-500">Loading channels...</div>
                </div>
            </div>
        </div>

        <div class="tabs-container">
            <div id="leave_tab_text" class="tab active">Text message</div>
        </div>

        <!-- Text Editor -->
        <div id="leave_text_editor">
            <div class="config-label">Message Editor</div>

            <!-- Commands Frame -->
            <div class="flex flex-wrap gap-2 mb-3 p-3 bg-[#1e1f22] border border-[#333] rounded-lg">
                <span class="command-badge" onclick="insertLeaveCmd('{user}')">{user}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{userid}')">{userid}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{usertag}')">{usertag}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{mention}')">{mention}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{avatar}')">{avatar}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{server}')">{server}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{serverid}')">{serverid}</span>
                <span class="command-badge"
                    onclick="insertLeaveCmd('{membercount}')">{membercount}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{members}')">{members}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{date}')">{date}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{time}')">{time}</span>
                <span class="command-badge" onclick="insertLeaveCmd('{role}')">{role}</span>
            </div>

            <div class="text-editor-container">
                <textarea id="leave_msg_input" class="text-editor"
                    oninput="updateLeaveValue('text', this.value)">{user} just left the server.</textarea>
                <span id="leave_char_count" class="char-counter">26 / 2000</span>
            </div>
        </div>
    </div>
</div>
`;

window.initializeLeaveServer = function () {
    // === DISCORD API + DATABASE INTEGRATION ===
    const urlParams = new URLSearchParams(window.location.search);
    const guildId = urlParams.get('guild_id');
    const defaultLeaveState = {
        enabled: false,
        text: '{user} just left the server.'
    };
    let leaveDataLoadPromise = null;
    let leaveDataLoaded = false;

    function ensureLeaveState() {
        if (!state.leave) state.leave = {};
        state.leave = { ...defaultLeaveState, ...state.leave };
        if (state.leave.text == null) state.leave.text = '';
    }

    function applyLeaveUIFromState() {
        const chDisplay = state.leave.channel_name || 'Select a channel';
        const currentChannelEl = document.getElementById('leave_current_channel');
        if (currentChannelEl) currentChannelEl.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${chDisplay}`;
        const msgInput = document.getElementById('leave_msg_input');
        if (msgInput) msgInput.value = state.leave.text || '';
        const charCount = document.getElementById('leave_char_count');
        if (charCount) charCount.innerText = `${(state.leave.text || '').length} / 2000`;
        const toggle = document.getElementById('toggle_leave');
        if (toggle) toggle.checked = !!state.leave.enabled;
        const section = document.getElementById('section_leave');
        if (section) section.classList.toggle('active', !!state.leave.enabled);
    }

    window.toggleLeaveDropdown = async function (id) {
        const el = document.getElementById(id);
        if (!el) return;

        el.classList.toggle('hidden');

        // If opening and empty, try to populate
        if (!el.classList.contains('hidden') && el.innerHTML.includes('Loading')) {
            await loadDiscordData();
        }
    };

    window.selectLeaveChannel = function (name, id) {
        state.leave.channel = id || name;
        state.leave.channel_name = name;
        const el = document.getElementById('leave_current_channel');
        if (el) el.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${name}`;
        const dropdown = document.getElementById('leave_channel_dropdown');
        if (dropdown) dropdown.classList.add('hidden');
        checkForChanges();
    };

    window.updateLeaveValue = function (key, val) {
        ensureLeaveState();
        const safeVal = (val == null) ? '' : val;
        state.leave[key] = safeVal;
        if (key === 'text') {
            const charCount = document.getElementById('leave_char_count');
            if (charCount) charCount.innerText = `${safeVal.length} / 2000`;
        }
        checkForChanges();
    };

    window.insertLeaveCmd = function (cmd) {
        const textarea = document.getElementById('leave_msg_input');
        if (!textarea) return;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;
        textarea.value = text.substring(0, start) + cmd + text.substring(end);
        textarea.focus();
        textarea.selectionStart = textarea.selectionEnd = start + cmd.length;
        updateLeaveValue('text', textarea.value);
    };

    const originalSave = window.saveChanges;
    window.saveLeaveChanges = async function () {
        if (!guildId) return;
        try {
            const response = await fetch(`/api/config/leave/${guildId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state.leave)
            });
            if (response.ok) {
                if (!window.__userToggledLeave) {
                    initialState.leave = JSON.parse(JSON.stringify(state.leave));
                }
                checkForChanges();
            }
        } catch (e) { console.error("Save failed", e); }
    };
    if (typeof originalSave !== 'function') {
        window.saveChanges = window.saveLeaveChanges;
    }

    async function loadDiscordData() {
        if (!guildId) return;
        if (leaveDataLoaded) return;
        if (leaveDataLoadPromise) return leaveDataLoadPromise;
        leaveDataLoadPromise = (async () => {

            // Fetch channels
            try {
                const chanResp = await fetch(`/api/guilds/${guildId}/channels`);
                const chanData = await chanResp.json();

                if (chanData.success && chanData.channels) {
                    const dropdown = document.getElementById('leave_channel_dropdown');
                    if (dropdown) {
                        dropdown.innerHTML = '';
                        chanData.channels.forEach(ch => {
                            const item = document.createElement('div');
                            item.className = 'hover:bg-[#404249] p-2 rounded cursor-pointer text-sm';
                            item.innerText = `# ${ch.name}`;
                            item.onclick = () => selectLeaveChannel(ch.name, ch.id);
                            dropdown.appendChild(item);
                        });
                    }
                }
            } catch (e) { console.error("Failed to populate channels", e); }

            // Fetch saved config and restore UI
            try {
                const confResp = await fetch(`/api/config/leave/${guildId}`);
                const confData = await confResp.json();
                if (confData.success && confData.config) {
                    const toggleEl = document.getElementById('toggle_leave');
                    const preserveEnabled = toggleEl ? toggleEl.checked : state.leave?.enabled;
                    // IMPORTANT: Merge with defaults to prevent null errors
                    state.leave = { ...state.leave, ...confData.config };
                    if (preserveEnabled !== undefined) state.leave.enabled = preserveEnabled;
                    ensureLeaveState();
                    if (!window.__userToggledLeave) {
                        initialState.leave = JSON.parse(JSON.stringify(state.leave));
                    }

                    // Update UI state
                    applyLeaveUIFromState();
                    checkForChanges();
                }
            } catch (e) { console.error("Failed to restore config", e); }
            leaveDataLoaded = true;
        })();
        return leaveDataLoadPromise;
    }

    ensureLeaveState();
    loadDiscordData();
    if (window.lucide) window.lucide.createIcons();
};

