window.JOIN_ROLE_HTML = `
<div class="expandable-section active allow-overflow" id="section_role">
    <div class="config-content">
        <div class="config-label">Roles to give</div>
        <div id="role_selected_list" class="flex flex-wrap gap-2"></div>

        <div class="relative" id="role_dropdown_container">
            <div class="dropdown-box" id="role_dropdown_box">
                <span id="role_dropdown_label" class="text-gray-400">Select or create role</span>
                <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
            </div>
            <div id="role_dropdown_panel" class="hidden absolute bottom-full mb-2 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-50 p-2">
                <div class="p-2">
                    <input id="role_search_input" type="text" class="custom-input" placeholder="Search roles...">
                </div>

                <div id="role_create_entry" class="p-2 rounded cursor-pointer text-sm hover:bg-[#404249] text-[#c7c9d1]">
                    + Create new role
                </div>

                <div id="role_create_form" class="hidden mt-2 bg-[#1e1f22] border border-[#2b2d31] rounded-lg p-3">
                    <div class="config-label">Create Role</div>
                    <div class="space-y-3">
                        <input id="role_create_name" type="text" class="custom-input" placeholder="Role name">
                        <div>
                            <div class="config-label">Role color</div>
                            <div class="flex flex-wrap gap-2 items-center">
                                <div class="color-dot bg-[#5865f2]" data-color="#5865f2"></div>
                                <div class="color-dot bg-[#57f287]" data-color="#57f287"></div>
                                <div class="color-dot bg-[#fee75c]" data-color="#fee75c"></div>
                                <div class="color-dot bg-[#ed4245]" data-color="#ed4245"></div>
                                <div class="color-dot bg-[#95a5a6]" data-color="#95a5a6"></div>
                                <div class="color-dot bg-[#e67e22]" data-color="#e67e22"></div>
                                <div class="color-dot bg-[#9b59b6]" data-color="#9b59b6"></div>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button id="role_create_cancel" class="btn btn-cancel" type="button">Cancel</button>
                            <button id="role_create_save" class="btn btn-save" type="button">Create</button>
                        </div>
                    </div>
                </div>

                <div id="role_list" class="max-h-48 overflow-y-auto custom-scrollbar mt-2"></div>
            </div>
        </div>
    </div>
</div>
`;

window.initializeJoinRole = function () {
    const urlParams = new URLSearchParams(window.location.search);
    const guildId = urlParams.get('guild_id');
    let rolesCache = [];
    let selectedRoleIds = new Set();
    let createColor = '#5865f2';

    function mergeDeep(target, source) {
        const out = { ...(target || {}) };
        if (!source) return out;
        for (const [key, val] of Object.entries(source)) {
            if (val && typeof val === 'object' && !Array.isArray(val)) {
                out[key] = mergeDeep(out[key], val);
            } else {
                out[key] = val;
            }
        }
        return out;
    }

    function ensureRoleState() {
        if (!state.role) state.role = { enabled: false, selected_roles: [] };
        if (!Array.isArray(state.role.selected_roles)) state.role.selected_roles = [];
    }

    function renderSelectedRoles() {
        const container = document.getElementById('role_selected_list');
        if (!container) return;
        container.innerHTML = '';

        if (selectedRoleIds.size === 0) {
            const empty = document.createElement('div');
            empty.className = 'text-xs text-gray-500';
            empty.textContent = 'No roles selected yet.';
            container.appendChild(empty);
            return;
        }

        selectedRoleIds.forEach(roleId => {
            const role = rolesCache.find(r => String(r.id) === String(roleId));
            const chip = document.createElement('div');
            chip.className = 'flex items-center gap-2 px-3 py-1 rounded-full bg-[#1e1f22] border border-[#2b2d31] text-sm';

            const dot = document.createElement('span');
            dot.className = 'inline-block w-3 h-3 rounded-full';
            dot.style.backgroundColor = role?.color ? role.color : '#6b7280';

            const name = document.createElement('span');
            name.textContent = role?.name || 'Unknown role';

            const remove = document.createElement('button');
            remove.type = 'button';
            remove.className = 'text-red-400 hover:text-red-300';
            remove.textContent = '×';
            remove.onclick = () => {
                selectedRoleIds.delete(roleId);
                syncSelectedToState();
                renderSelectedRoles();
            };

            chip.appendChild(dot);
            chip.appendChild(name);
            chip.appendChild(remove);
            container.appendChild(chip);
        });
    }

    function syncSelectedToState() {
        ensureRoleState();
        state.role.selected_roles = Array.from(selectedRoleIds);
        checkForChanges();
    }

    function renderRoleList(filter = '') {
        const list = document.getElementById('role_list');
        if (!list) return;
        list.innerHTML = '';

        const q = filter.trim().toLowerCase();
        rolesCache
            .filter(r => r.name.toLowerCase().includes(q))
            .forEach(role => {
                const item = document.createElement('div');
                item.className = 'p-2 rounded cursor-pointer text-sm hover:bg-[#404249] flex items-center gap-2';
                const dot = document.createElement('span');
                dot.className = 'inline-block w-3 h-3 rounded-full';
                dot.style.backgroundColor = role.color || '#6b7280';
                const label = document.createElement('span');
                label.textContent = role.name;
                item.appendChild(dot);
                item.appendChild(label);
                item.onclick = () => {
                    selectedRoleIds.add(role.id);
                    syncSelectedToState();
                    renderSelectedRoles();
                    toggleDropdown(false);
                };
                list.appendChild(item);
            });
    }

    function toggleDropdown(show) {
        const panel = document.getElementById('role_dropdown_panel');
        if (!panel) return;
        const shouldShow = show ?? panel.classList.contains('hidden');
        panel.classList.toggle('hidden', !shouldShow);
    }

    async function loadRoles() {
        if (!guildId) return;
        try {
            const resp = await fetch(`/api/guilds/${guildId}/roles`);
            const data = await resp.json();
            if (data.success && Array.isArray(data.roles)) {
                const rawRoles = data.roles.filter(r => !r.managed && !/mee6|dyno|bot/i.test(r.name || ''));
                rolesCache = rawRoles.map(r => ({
                    id: r.id,
                    name: r.name,
                    color: r.color ? `#${r.color.toString(16).padStart(6, '0')}` : '#6b7280'
                }));
                renderRoleList();
                renderSelectedRoles();
            }
        } catch (e) {
            console.error('Failed to load roles', e);
        }
    }

    async function loadRoleConfig() {
        if (!guildId) return;
        try {
            const resp = await fetch(`/api/config/role/${guildId}`);
            const data = await resp.json();
            if (data.success && data.config) {
                ensureRoleState();
                const prevEnabled = !!state.role.enabled;
                state.role = mergeDeep(state.role, data.config);
                if (window.__userToggledRole) {
                    state.role.enabled = prevEnabled;
                }
                if (!window.__userToggledRole) {
                    initialState.role = JSON.parse(JSON.stringify(state.role));
                }
                selectedRoleIds = new Set(state.role.selected_roles || []);
                renderSelectedRoles();
            }
        } catch (e) {
            console.error('Failed to load role config', e);
        }
    }

    async function createRole() {
        const nameInput = document.getElementById('role_create_name');
        const name = (nameInput?.value || '').trim();
        if (!name || !guildId) return;
        try {
            const resp = await fetch('/api/roles/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ guild_id: guildId, name, color: createColor })
            });
            const data = await resp.json();
            if (data.success && data.role) {
                rolesCache.unshift({
                    id: data.role.id,
                    name: data.role.name,
                    color: data.role.color
                });
                selectedRoleIds.add(data.role.id);
                syncSelectedToState();
                renderRoleList();
                renderSelectedRoles();
                toggleCreateForm(false);
                if (nameInput) nameInput.value = '';
            }
        } catch (e) {
            console.error('Failed to create role', e);
        }
    }

    function toggleCreateForm(show) {
        const form = document.getElementById('role_create_form');
        if (!form) return;
        form.classList.toggle('hidden', !show);
    }

    const dropdownBox = document.getElementById('role_dropdown_box');
    if (dropdownBox) dropdownBox.addEventListener('click', () => toggleDropdown());

    const searchInput = document.getElementById('role_search_input');
    if (searchInput) searchInput.addEventListener('input', (e) => renderRoleList(e.target.value || ''));

    const createEntry = document.getElementById('role_create_entry');
    if (createEntry) createEntry.addEventListener('click', () => toggleCreateForm(true));

    const createCancel = document.getElementById('role_create_cancel');
    if (createCancel) createCancel.addEventListener('click', () => toggleCreateForm(false));

    const createSave = document.getElementById('role_create_save');
    if (createSave) createSave.addEventListener('click', createRole);

    const colorDots = document.querySelectorAll('#role_create_form .color-dot');
    colorDots.forEach(dot => {
        dot.addEventListener('click', () => {
            const color = dot.getAttribute('data-color');
            if (color) createColor = color;
            colorDots.forEach(d => d.classList.remove('active'));
            dot.classList.add('active');
        });
    });

    ensureRoleState();
    loadRoleConfig().then(loadRoles);
    if (window.lucide) window.lucide.createIcons();
};

