window.JOIN_SERVER_HTML = `
<!-- Feature 2 (The Detailed One) -->
<div class="expandable-section active" id="section_join">
    <div class="config-content">
        <div>
            <label class="config-label">Welcome Message Channel <span
                    class="text-red-500">*</span></label>
            <div class="relative">
                <div class="dropdown-box" onclick="toggleJoinDropdown('join_channel_dropdown')">
                    <span id="join_current_channel" class="flex items-center gap-2 text-gray-400">
                        <i data-lucide="hash" class="w-4 h-4"></i> Select a channel
                    </span>
                    <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
                </div>
                <div id="join_channel_dropdown"
                    class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto">
                    <div class="p-2 text-sm text-gray-500">Loading channels...</div>
                </div>
            </div>
        </div>

        <div class="tabs-container">
            <div id="join_tab_text" class="tab active" onclick="setJoinMessageType('text')">Text
                message</div>
            <div id="join_tab_embed" class="tab" onclick="setJoinMessageType('embed')">Embed message
            </div>
        </div>

        <!-- Text Editor -->
        <div id="join_text_editor">
            <div class="config-label">Message Editor</div>

            <!-- Commands Frame -->
            <div class="flex flex-wrap gap-2 mb-3 p-3 bg-[#1e1f22] border border-[#333] rounded-lg">
                <span class="command-badge" onclick="insertJoinCmd('{user}')">{user}</span>
                <span class="command-badge" onclick="insertJoinCmd('{userid}')">{userid}</span>
                <span class="command-badge" onclick="insertJoinCmd('{usertag}')">{usertag}</span>
                <span class="command-badge" onclick="insertJoinCmd('{mention}')">{mention}</span>
                <span class="command-badge" onclick="insertJoinCmd('{avatar}')">{avatar}</span>
                <span class="command-badge" onclick="insertJoinCmd('{server}')">{server}</span>
                <span class="command-badge" onclick="insertJoinCmd('{serverid}')">{serverid}</span>
                <span class="command-badge"
                    onclick="insertJoinCmd('{membercount}')">{membercount}</span>
                <span class="command-badge" onclick="insertJoinCmd('{members}')">{members}</span>
                <span class="command-badge" onclick="insertJoinCmd('{date}')">{date}</span>
                <span class="command-badge" onclick="insertJoinCmd('{time}')">{time}</span>
                <span class="command-badge" onclick="insertJoinCmd('{role}')">{role}</span>
            </div>

            <div class="text-editor-container">
                <textarea id="join_msg_input" class="text-editor"
                    oninput="updateJoinValue('text', this.value)">Hey {user}, welcome to **{server}**!</textarea>
                <span id="join_char_count" class="char-counter">36 / 2000</span>
            </div>

            <!-- Card Toggle -->
            <div class="card-toggle-container">
                <label class="switch">
                    <input type="checkbox" id="join_card_toggle"
                        onchange="toggleCard('join', this.checked)">
                    <span class="slider"></span>
                </label>
                <span class="card-toggle-label">Send a welcome card when a user joins the server</span>
            </div>

            <!-- Card Settings (Nested) -->
            <div id="join_card_settings" class="hidden mt-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-gray-400">Customize your
                        welcome card</h3>
                </div>

                <div>
                    <label class="config-label">Font</label>
                    <div class="relative">
                        <div class="dropdown-box" onclick="toggleJoinDropdown('join_font_dropdown')">
                            <span id="join_current_font">Inter</span>
                            <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
                        </div>
                        <div id="join_font_dropdown"
                            class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto custom-scrollbar">
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Inter]"
                                onclick="setCardFont('join', 'Inter')">Inter</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Roboto]"
                                onclick="setCardFont('join', 'Roboto')">Roboto</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Open Sans']"
                                onclick="setCardFont('join', 'Open Sans')">Open Sans</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Source Sans 3']"
                                onclick="setCardFont('join', 'Source Sans 3')">Source Sans 3</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Lato]"
                                onclick="setCardFont('join', 'Lato')">Lato</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Montserrat]"
                                onclick="setCardFont('join', 'Montserrat')">Montserrat</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Poppins]"
                                onclick="setCardFont('join', 'Poppins')">Poppins</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Raleway]"
                                onclick="setCardFont('join', 'Raleway')">Raleway</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Nunito]"
                                onclick="setCardFont('join', 'Nunito')">Nunito</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Ubuntu]"
                                onclick="setCardFont('join', 'Ubuntu')">Ubuntu</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['DM Sans']"
                                onclick="setCardFont('join', 'DM Sans')">DM Sans</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Merriweather]"
                                onclick="setCardFont('join', 'Merriweather')">Merriweather</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Playfair Display']"
                                onclick="setCardFont('join', 'Playfair Display')">Playfair Display</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Oswald]"
                                onclick="setCardFont('join', 'Oswald')">Oswald</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Bebas Neue']"
                                onclick="setCardFont('join', 'Bebas Neue')">Bebas Neue</div>
                        </div>
                    </div>
                </div>
                <div>
                    <label class="config-label">Text color</label>
                    <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                        <div class="color-dot bg-white active" data-color="#ffffff"
                            onclick="setCardColor('join', 'textColor', '#ffffff')"></div>
                        <div class="color-dot bg-[#f2f3f5]" data-color="#f2f3f5"
                            onclick="setCardColor('join', 'textColor', '#f2f3f5')"></div>
                        <div class="color-dot bg-[#dbdee1]" data-color="#dbdee1"
                            onclick="setCardColor('join', 'textColor', '#dbdee1')"></div>
                        <div class="color-dot bg-[#b5bac1]" data-color="#b5bac1"
                            onclick="setCardColor('join', 'textColor', '#b5bac1')"></div>
                        <div class="color-dot bg-[#949ba4]" data-color="#949ba4"
                            onclick="setCardColor('join', 'textColor', '#949ba4')"></div>
                        <div class="color-dot bg-[#80848e]" data-color="#80848e"
                            onclick="setCardColor('join', 'textColor', '#80848e')"></div>
                        <div class="color-dot bg-[#5865f2]" data-color="#5865f2"
                            onclick="setCardColor('join', 'textColor', '#5865f2')"></div>
                        <div class="color-dot bg-[#57f287]" data-color="#57f287"
                            onclick="setCardColor('join', 'textColor', '#57f287')"></div>
                        <div class="color-dot bg-[#fee75c]" data-color="#fee75c"
                            onclick="setCardColor('join', 'textColor', '#fee75c')"></div>
                        <div class="color-dot bg-[#ed4245]" data-color="#ed4245"
                            onclick="setCardColor('join', 'textColor', '#ed4245')"></div>
                    </div>
                </div>

                <div>
                    <label class="config-label">Background color</label>
                    <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                        <div class="color-dot bg-[#0b0f17] active" data-color="#0b0f17"
                            onclick="setCardColor('join', 'bgColor', '#0b0f17')"></div>
                        <div class="color-dot bg-[#111827]" data-color="#111827"
                            onclick="setCardColor('join', 'bgColor', '#111827')"></div>
                        <div class="color-dot bg-[#1f2937]" data-color="#1f2937"
                            onclick="setCardColor('join', 'bgColor', '#1f2937')"></div>
                        <div class="color-dot bg-[#0f172a]" data-color="#0f172a"
                            onclick="setCardColor('join', 'bgColor', '#0f172a')"></div>
                        <div class="color-dot bg-[#111827]" data-color="#111827"
                            onclick="setCardColor('join', 'bgColor', '#111827')"></div>
                        <div class="color-dot bg-[#1e1b4b]" data-color="#1e1b4b"
                            onclick="setCardColor('join', 'bgColor', '#1e1b4b')"></div>
                        <div class="color-dot bg-[#0f766e]" data-color="#0f766e"
                            onclick="setCardColor('join', 'bgColor', '#0f766e')"></div>
                        <div class="color-dot bg-[#3b0764]" data-color="#3b0764"
                            onclick="setCardColor('join', 'bgColor', '#3b0764')"></div>
                        <div class="color-dot bg-[#0f2a3f]" data-color="#0f2a3f"
                            onclick="setCardColor('join', 'bgColor', '#0f2a3f')"></div>
                        <div class="color-dot bg-[#1f2937]" data-color="#1f2937"
                            onclick="setCardColor('join', 'bgColor', '#1f2937')"></div>
                    </div>
                </div>
                <div>
                    <label class="config-label">Background image</label>
                    <div class="flex items-center gap-4">
                        <div class="img-upload img-upload-lg" id="join_card_bg_button">
                            <i data-lucide="image" class="w-5 h-5"></i>
                        </div>
                        <div id="join_card_bg_label" class="text-xs text-gray-500">No image selected</div>
                        <input type="file" id="join_card_bg_input" accept="image/*" class="hidden" />
                    </div>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <label class="config-label mb-0">Overlay opacity</label>
                        <span id="join_opacity_val" class="text-[10px] text-gray-500">50%</span>
                    </div>
                    <input type="range" class="range-slider" min="0" max="100" value="50"
                        oninput="updateCardValue('join', 'opacity', this.value)">
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="config-label">Title</label>
                        <input type="text" class="custom-input"
                            placeholder="{user.idname} just joined the server"
                            value="{user.idname} just joined the server"
                            oninput="updateCardValue('join', 'title', this.value)">
                    </div>
                    <div>
                        <label class="config-label">Subtitle</label>
                        <input type="text" class="custom-input"
                            placeholder="Member # {server.member_count}"
                            value="Member # {server.member_count}"
                            oninput="updateCardValue('join', 'subtitle', this.value)">
                    </div>
                </div>
            </div>
        </div>

        <!-- Embed Editor -->
        <div id="join_embed_editor" class="hidden space-y-6">
            <div class="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase">
                <i data-lucide="eye" class="w-3 h-3"></i> Preview
            </div>
            
            <div class="embed-stripe" id="join_embed_stripe">
                <div class="space-y-6">
                    <div>
                        <div class="config-label">Stripe color</div>
                        <div class="flex gap-2 items-center">
                            <div class="w-6 h-6 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 cursor-pointer flex items-center justify-center overflow-hidden border border-white/20">
                                <i data-lucide="aperture" class="w-3 h-3 text-white"></i>
                            </div>
                            <div class="color-dot bg-white" onclick="setJoinEmbedColor('#ffffff')"></div>
                            <div class="color-dot bg-gray-500 active" onclick="setJoinEmbedColor('#6b7280')"></div>
                            <div class="color-dot bg-red-400" onclick="setJoinEmbedColor('#f87171')"></div>
                            <div class="color-dot bg-orange-400" onclick="setJoinEmbedColor('#fb923c')"></div>
                            <div class="color-dot bg-yellow-400" onclick="setJoinEmbedColor('#fbbf24')"></div>
                            <div class="color-dot bg-green-400" onclick="setJoinEmbedColor('#4ade80')"></div>
                            <div class="color-dot bg-blue-400" onclick="setJoinEmbedColor('#5865f2')"></div>
                        </div>
                    </div>

                    <div class="flex gap-4 items-center">
                        <div class="img-upload" id="join_embed_image_button">
                            <i data-lucide="image" class="w-5 h-5"></i>
                        </div>
                        <input type="file" id="join_embed_image_input" accept="image/*" class="hidden" />
                        <div id="join_embed_image_label" class="text-xs text-gray-500">No image selected</div>
                        <div class="flex-1">
                            <div class="config-label">Author</div>
                            <input type="text" 
                                class="custom-input bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                                placeholder="Author name"
                                id="join_embed_author"
                                oninput="updateJoinEmbedValue('author', this.value)">
                        </div>
                    </div>

                    <div>
                        <div class="config-label">Title text</div>
                        <input type="text" 
                            class="custom-input bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                            placeholder="Title text"
                            id="join_embed_title"
                            oninput="updateJoinEmbedValue('title', this.value)">
                    </div>

                    <div>
                        <div class="config-label">Message template</div>
                        <textarea class="text-editor h-24" placeholder="Description"
                            id="join_embed_description"
                            oninput="updateJoinEmbedValue('description', this.value)">Hey {user}, welcome to **{server}**!</textarea>
                    </div>
                    <div id="join_embed_image_preview_wrap" class="hidden">
                        <div class="config-label">Image Preview</div>
                        <img id="join_embed_image_preview" class="w-full max-w-[420px] rounded-lg border border-[#2b2d31]" alt="Embed preview">
                    </div>

                    <div>
                        <div class="config-label">Footer</div>
                        <input type="text" 
                            class="bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                            placeholder="Footer text"
                            id="join_embed_footer"
                            oninput="updateJoinEmbedValue('footer', this.value)">
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="join_preview_section" class="space-y-4 mt-6 hidden">
        <div class="config-label">Live Preview</div>
        <div class="unified-preview">
            <div class="welcome-card-preview w-full max-w-[520px] mx-auto" id="join_card_preview_wrap">
                <div class="card-overlay" id="join_card_overlay"></div>
                <div class="card-content">
                    <div class="card-avatar" id="join_card_avatar_border">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lucky" alt="Avatar">
                    </div>
                    <div class="card-title" id="join_card_title_text">manav6516#0 just joined the server</div>
                    <div class="card-subtitle" id="join_card_subtitle_text">Member #5</div>
                </div>
            </div>
        </div>
    </div>
</div>
`;

window.initializeJoinServer = function() {
    // === DISCORD API + DATABASE INTEGRATION ===
    const urlParams = new URLSearchParams(window.location.search);
    const guildId = urlParams.get('guild_id');
    const defaultCardState = {
        enabled: false,
        textColor: '#ffffff',
        bgColor: '#000000',
        bgImage: '',
        opacity: 50,
        font: 'Inter',
        title: '{user.idname} just joined the server',
        subtitle: 'Member # {server.member_count}'
    };
    const defaultEmbedState = {
        author: '',
        title: '',
        description: 'Hey {user}, welcome to **{server}**!',
        footer: '',
        color: '#6b7280'
    };
    let joinDataLoadPromise = null;
    let joinDataLoaded = false;
    let pendingCardBgFile = null;
    let pendingCardBgObjectUrl = null;
    let pendingEmbedImageFile = null;
    let pendingEmbedImageObjectUrl = null;

    function mergeDeep(target, source) {
        const out = { ...(target || {}) };
        if (!source) return out;
        Object.keys(source).forEach(key => {
            const val = source[key];
            if (val && typeof val === 'object' && !Array.isArray(val)) {
                out[key] = mergeDeep(out[key], val);
            } else {
                out[key] = val;
            }
        });
        return out;
    }

    function ensureJoinState() {
        if (!state.join) state.join = {};
        state.join = mergeDeep(state.join, {});
        if (!state.join.type) state.join.type = 'text';
        if (state.join.text == null) state.join.text = '';
        if (!state.join.card) state.join.card = {};
        state.join.card = { ...defaultCardState, ...state.join.card };
        if (!state.join.embed) state.join.embed = {};
        state.join.embed = { ...defaultEmbedState, ...state.join.embed };
        if (!state.join.mode) state.join.mode = 'text';
    }

    function applyJoinCardUIFromState() {
        const card = state.join.card || defaultCardState;
        const preview = document.getElementById('join_preview_section');
        const currentFontEl = document.getElementById('join_current_font');
        if (currentFontEl) currentFontEl.innerText = card.font || defaultCardState.font;
        toggleCard('join', !!card.enabled);
        setCardColor('join', 'textColor', card.textColor || defaultCardState.textColor);
        setCardColor('join', 'bgColor', card.bgColor || defaultCardState.bgColor);
        applyJoinCardBackground(card.bgImage || '');
        if (preview) preview.classList.toggle('hidden', !card.enabled);
        if (card.bgImage) {
            const parts = card.bgImage.split('/');
            setJoinCardBgLabel(parts[parts.length - 1] || 'Image selected');
        } else {
            setJoinCardBgLabel('No image selected');
        }
        const opacityEl = document.getElementById('join_opacity_val');
        if (opacityEl) opacityEl.innerText = `${card.opacity ?? defaultCardState.opacity}%`;
        const opacityInput = document.querySelector('#join_card_settings input[type="range"]');
        if (opacityInput) opacityInput.value = card.opacity ?? defaultCardState.opacity;
        const titleInput = document.querySelector('#join_card_settings input[placeholder*="just joined"]');
        if (titleInput) titleInput.value = card.title || defaultCardState.title;
        const subtitleInput = document.querySelector('#join_card_settings input[placeholder*="Member #"]');
        if (subtitleInput) subtitleInput.value = card.subtitle || defaultCardState.subtitle;
    }

    function applyJoinEmbedUIFromState() {
        const embed = state.join.embed || defaultEmbedState;
        const embedAuthor = document.getElementById('join_embed_author');
        if (embedAuthor) embedAuthor.value = embed.author || '';
        const embedTitle = document.getElementById('join_embed_title');
        if (embedTitle) embedTitle.value = embed.title || '';
        const embedDesc = document.getElementById('join_embed_description');
        if (embedDesc) embedDesc.value = embed.description || defaultEmbedState.description;
        const embedFooter = document.getElementById('join_embed_footer');
        if (embedFooter) embedFooter.value = embed.footer || '';
        setJoinEmbedImageLabel(embed.image);
        setJoinEmbedImagePreview(embed.image);
        if (embed.color) setJoinEmbedColor(embed.color, true);
    }

    window.toggleJoinDropdown = async function(id) {
        const el = document.getElementById(id);
        if(!el) return;
        el.classList.toggle('hidden');
        if (!el.classList.contains('hidden') && el.innerHTML.includes('Loading')) {
            await loadDiscordData();
        }
    };

    window.selectJoinChannel = function(name, id) {
        state.join.channel = id || name;
        state.join.channel_name = name;
        const el = document.getElementById('join_current_channel');
        if (el) el.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${name}`;
        const dropdown = document.getElementById('join_channel_dropdown');
        if(dropdown) dropdown.classList.add('hidden');
        checkForChanges();
    };

    window.setJoinMessageType = function(type) {
        setJoinMode(type === 'embed' ? 'embed' : 'text');
        state.join.type = type;
        const textEd = document.getElementById('join_text_editor');
        const embedEd = document.getElementById('join_embed_editor');
        const tabT = document.getElementById('join_tab_text');
        const tabE = document.getElementById('join_tab_embed');

        if (type === 'text') {
            if(textEd) textEd.classList.remove('hidden');
            if(embedEd) embedEd.classList.add('hidden');
            if(tabT) tabT.classList.add('active');
            if(tabE) tabE.classList.remove('active');
        } else {
            if(textEd) textEd.classList.add('hidden');
            if(embedEd) embedEd.classList.remove('hidden');
            if(tabT) tabT.classList.remove('active');
            if(tabE) tabE.classList.add('active');
        }
        checkForChanges();
    };

    window.updateJoinValue = function(key, val) {
        ensureJoinState();
        const safeVal = (val == null) ? '' : val;
        state.join[key] = safeVal;
        if (key === 'text') {
            const charCount = document.getElementById('join_char_count');
            if(charCount) charCount.innerText = `${safeVal.length} / 2000`;
        }
        checkForChanges();
    };

    window.insertJoinCmd = function(cmd) {
        const textarea = document.getElementById('join_msg_input');
        if(!textarea) return;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;
        textarea.value = text.substring(0, start) + cmd + text.substring(end);
        textarea.focus();
        textarea.selectionStart = textarea.selectionEnd = start + cmd.length;
        updateJoinValue('text', textarea.value);
    };

    // Card/Embed helpers (simplified wrappers)
    window.toggleCard = function(feature, enabled) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card.enabled = enabled;
        const settings = document.getElementById(`${feature}_card_settings`);
        const textarea = document.getElementById(`${feature}_msg_input`);
        const preview = document.getElementById('join_preview_section');
        if (enabled) {
            setJoinMode('card');
            if (settings) settings.classList.remove('hidden');
            if (preview) preview.classList.remove('hidden');
            if (textarea) {
                textarea.disabled = true;
                textarea.classList.add('opacity-50', 'cursor-not-allowed');
            }
        } else {
            setJoinMode(state.join.type === 'embed' ? 'embed' : 'text');
            if (settings) settings.classList.add('hidden');
            if (preview) preview.classList.add('hidden');
            if (textarea) {
                textarea.disabled = false;
                textarea.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }
        checkForChanges();
    };
    
    window.setCardFont = function(feature, font) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card.font = font;
        const currentFontEl = document.getElementById(`${feature}_current_font`);
        if (currentFontEl) currentFontEl.innerText = font;
        const dropdown = document.getElementById(`${feature}_font_dropdown`);
        if(dropdown) dropdown.classList.add('hidden');
        checkForChanges();
    };

    window.setCardColor = function(feature, key, color) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card[key] = color;
        if (key === 'textColor') {
            const title = document.getElementById(`${feature}_card_title_text`);
            const border = document.getElementById(`${feature}_card_avatar_border`);
            if (title) title.style.color = color;
            if (border) border.style.borderColor = color;
        } else {
            applyJoinCardBackground(state[feature].card.bgImage || '');
        }
        // Logic to update dots UI...
        const containers = document.querySelectorAll(`#${feature}_card_settings .color-picker-row`);
        const targetContainer = key === 'textColor' ? containers[0] : containers[1];
        if (targetContainer) {
            targetContainer.querySelectorAll('.color-dot').forEach(dot => {
                const dataColor = dot.getAttribute('data-color');
                const rawColor = dataColor || dot.style.backgroundColor || '';
                const dotColor = rawColor.startsWith('rgb') ? rgbToHex(rawColor) : rawColor;
                if (dotColor && dotColor.toLowerCase() === color.toLowerCase()) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
        checkForChanges();
    };
    
    window.updateCardValue = function(feature, key, val) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card[key] = val;
        if (key === 'opacity') {
            const el = document.getElementById(`${feature}_opacity_val`);
            if (el) el.innerText = `${val}%`;
            const over = document.getElementById(`${feature}_card_overlay`);
            if (over) over.style.backgroundColor = `rgba(0,0,0,${val / 100})`;
        }
        if (key === 'title') {
            const text = (val || '').replace('{user.idname}', 'manav6516#0');
            const el = document.getElementById(`${feature}_card_title_text`);
            if (el) el.innerText = text;
        }
        if (key === 'subtitle') {
            const text = (val || '').replace('{server.member_count}', '5');
            const el = document.getElementById(`${feature}_card_subtitle_text`);
            if (el) el.innerText = text;
        }
        checkForChanges();
    };

    window.setJoinEmbedColor = function(color, suppressMode = false) {
        ensureJoinState();
        if (!suppressMode) setJoinMode('embed');
        state.join.embed.color = color;
        const stripe = document.getElementById('join_embed_stripe');
        if (stripe) stripe.style.borderLeftColor = color;
        
        // Update dots active state
        const container = document.querySelector('#join_embed_editor .flex.gap-2.items-center');
        if (container) {
            container.querySelectorAll('.color-dot').forEach(dot => {
                dot.classList.remove('active');
                // Simple heuristic to match colors - ideally we'd use a better way
                // but for this implementation we'll match by the onclick color
                if (dot.getAttribute('onclick').includes(color)) {
                    dot.classList.add('active');
                }
            });
        }
        checkForChanges();
    };

    window.updateJoinEmbedValue = function(key, val) {
        ensureJoinState();
        setJoinMode('embed');
        state.join.embed[key] = val;
        checkForChanges();
    };

    function applyJoinCardBackground(url) {
        const wrap = document.getElementById('join_card_preview_wrap');
        if (!wrap) return;
        if (url) {
            wrap.style.backgroundImage = `url('${url}')`;
            wrap.style.backgroundSize = 'cover';
            wrap.style.backgroundPosition = 'center';
        } else {
            wrap.style.backgroundImage = 'none';
            wrap.style.backgroundColor = state.join.card?.bgColor || defaultCardState.bgColor;
        }
    }

    function setJoinCardBgLabel(text) {
        const label = document.getElementById('join_card_bg_label');
        if (label) label.innerText = text;
    }

    function handleJoinCardBgFile(file) {
        if (!file) return;
        pendingCardBgFile = file;
        if (pendingCardBgObjectUrl) URL.revokeObjectURL(pendingCardBgObjectUrl);
        pendingCardBgObjectUrl = URL.createObjectURL(file);
        state.join.card.bgImage = pendingCardBgObjectUrl;
        applyJoinCardBackground(pendingCardBgObjectUrl);
        setJoinCardBgLabel(file.name);
        checkForChanges();
    }

    async function uploadJoinCardImageIfNeeded() {
        if (!pendingCardBgFile) return;
        const form = new FormData();
        form.append('file', pendingCardBgFile);
        try {
            const resp = await fetch('/api/upload/image', {
                method: 'POST',
                body: form
            });
            const data = await resp.json();
            if (data && data.success && data.url) {
                state.join.card.bgImage = data.url;
                applyJoinCardBackground(data.url);
                pendingCardBgFile = null;
                if (pendingCardBgObjectUrl) {
                    URL.revokeObjectURL(pendingCardBgObjectUrl);
                    pendingCardBgObjectUrl = null;
                }
            } else {
                console.error('Image upload failed', data);
            }
        } catch (e) {
            console.error('Image upload failed', e);
        }
    }

    function setJoinEmbedImageLabel(urlOrName) {
        const label = document.getElementById('join_embed_image_label');
        if (!label) return;
        if (!urlOrName) {
            label.innerText = 'No image selected';
            return;
        }
        const parts = String(urlOrName).split('/');
        label.innerText = parts[parts.length - 1] || 'Image selected';
    }

    function setJoinEmbedImagePreview(url) {
        const wrap = document.getElementById('join_embed_image_preview_wrap');
        const img = document.getElementById('join_embed_image_preview');
        if (!wrap || !img) return;
        if (!url) {
            wrap.classList.add('hidden');
            img.removeAttribute('src');
            return;
        }
        wrap.classList.remove('hidden');
        img.src = url;
    }

    function handleJoinEmbedImageFile(file) {
        if (!file) return;
        pendingEmbedImageFile = file;
        if (pendingEmbedImageObjectUrl) URL.revokeObjectURL(pendingEmbedImageObjectUrl);
        pendingEmbedImageObjectUrl = URL.createObjectURL(file);
        state.join.embed.image = pendingEmbedImageObjectUrl;
        setJoinEmbedImageLabel(file.name);
        setJoinEmbedImagePreview(pendingEmbedImageObjectUrl);
        checkForChanges();
    }

    async function uploadJoinEmbedImageIfNeeded() {
        if (!pendingEmbedImageFile) return;
        const form = new FormData();
        form.append('file', pendingEmbedImageFile);
        try {
            const resp = await fetch('/api/upload/image', {
                method: 'POST',
                body: form
            });
            const data = await resp.json();
            if (data && data.success && data.url) {
                state.join.embed.image = data.url;
                pendingEmbedImageFile = null;
                if (pendingEmbedImageObjectUrl) {
                    URL.revokeObjectURL(pendingEmbedImageObjectUrl);
                    pendingEmbedImageObjectUrl = null;
                }
            } else {
                console.error('Image upload failed', data);
            }
        } catch (e) {
            console.error('Image upload failed', e);
        }
    }

    function setJoinMode(mode) {
        ensureJoinState();
        state.join.mode = mode;
        if (mode === 'card') {
            state.join.type = 'text';
            if (state.join.card) state.join.card.enabled = true;
        } else {
            if (state.join.card) state.join.card.enabled = false;
            state.join.type = mode === 'embed' ? 'embed' : 'text';
        }
    }

    if (!window.__joinSaveWrapped) {
        const originalSave = window.saveChanges;
        if (typeof originalSave === 'function') {
            window.saveChanges = async function() {
                await uploadJoinCardImageIfNeeded();
                await uploadJoinEmbedImageIfNeeded();
                return originalSave();
            };
        } else {
            window.saveJoinChanges = async function() {
                if (!guildId) return;
                await uploadJoinCardImageIfNeeded();
                await uploadJoinEmbedImageIfNeeded();
                try {
                    const response = await fetch(`/api/config/join/${guildId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(state.join)
                    });
                    if (response.ok) {
                        initialState.join = JSON.parse(JSON.stringify(state.join));
                        checkForChanges();
                    }
                } catch (e) { console.error("Save failed", e); }
            };
            window.saveChanges = window.saveJoinChanges;
        }
        window.__joinSaveWrapped = true;
    }

    async function loadDiscordData() {
        if (!guildId) return;
        if (joinDataLoaded) return;
        if (joinDataLoadPromise) return joinDataLoadPromise;
        joinDataLoadPromise = (async () => {

            // Fetch channels
            try {
                const chanResp = await fetch(`/api/guilds/${guildId}/channels`);
                const chanData = await chanResp.json();
                
                if (chanData.success && chanData.channels) {
                    const dropdown = document.getElementById('join_channel_dropdown');
                    if (dropdown) {
                        dropdown.innerHTML = '';
                        chanData.channels.forEach(ch => {
                            const item = document.createElement('div');
                            item.className = 'hover:bg-[#404249] p-2 rounded cursor-pointer text-sm';
                            item.innerText = `# ${ch.name}`;
                            item.onclick = () => selectJoinChannel(ch.name, ch.id);
                            dropdown.appendChild(item);
                        });
                    }
                }
            } catch (e) { console.error("Failed to populate channels", e); }

            // Fetch Config
            try {
                const confResp = await fetch(`/api/config/join/${guildId}`);
                const confData = await confResp.json();
                if (confData.success && confData.config) {
                    const toggleEl = document.getElementById('toggle_join');
                    const preserveEnabled = toggleEl ? toggleEl.checked : state.join?.enabled;
                    const mergedJoin = mergeDeep(state.join || {}, confData.config || {});
                    if (preserveEnabled !== undefined) mergedJoin.enabled = preserveEnabled;
                    state.join = mergedJoin;
                    ensureJoinState();
                    if (!window.__userToggledJoin) {
                        initialState.join = JSON.parse(JSON.stringify(state.join));
                    }

                    // Restore UI
                    const chDisplay = state.join.channel_name || 'Select a channel';
                    const currentChannelEl = document.getElementById('join_current_channel');
                    if (currentChannelEl) currentChannelEl.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${chDisplay}`;

                    const msgInput = document.getElementById('join_msg_input');
                    if (msgInput) msgInput.value = state.join.text || '';
                    const charCount = document.getElementById('join_char_count');
                    if (charCount) charCount.innerText = `${(state.join.text || '').length} / 2000`;
                    
                    const toggle = document.getElementById('toggle_join');
                    if (toggle) toggle.checked = !!state.join.enabled;
                    const section = document.getElementById('section_join');
                    if (section) section.classList.toggle('active', !!state.join.enabled);
                    
                    // Restore Card settings
                    if (state.join.card) {
                        const cardToggle = document.getElementById('join_card_toggle');
                        if (cardToggle) cardToggle.checked = !!state.join.card.enabled;
                        applyJoinCardUIFromState();
                    }

                    // Restore Embed settings
                    if (state.join.embed) applyJoinEmbedUIFromState();
                    if (state.join.type) setJoinMessageType(state.join.type);
                    if (state.join.mode === 'card') {
                        const cardToggle = document.getElementById('join_card_toggle');
                        if (cardToggle) cardToggle.checked = true;
                        toggleCard('join', true);
                    }
                    checkForChanges();
                }
            } catch (e) { console.error("Failed to load join config", e); }
            joinDataLoaded = true;
        })();
        return joinDataLoadPromise;
    }

    const bgButton = document.getElementById('join_card_bg_button');
    const bgInput = document.getElementById('join_card_bg_input');
    if (bgButton && bgInput) {
        bgButton.addEventListener('click', () => bgInput.click());
        bgInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            handleJoinCardBgFile(file);
        });
    }
    const embedImageButton = document.getElementById('join_embed_image_button');
    const embedImageInput = document.getElementById('join_embed_image_input');
    if (embedImageButton && embedImageInput) {
        embedImageButton.addEventListener('click', () => embedImageInput.click());
        embedImageInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            handleJoinEmbedImageFile(file);
        });
    }

    ensureJoinState();
    loadDiscordData();
    if (window.lucide) window.lucide.createIcons();
};

