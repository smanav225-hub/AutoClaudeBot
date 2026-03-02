window.JOIN_PRIVATE_HTML = `
<!-- Feature 2 (The Detailed One) -->
<div class="expandable-section active" id="section_dm">
    <div class="config-content">
        <div class="text-xs text-gray-500">
            This message is sent to the user directly in DMs when they join the server.
        </div>

        <div class="tabs-container">
            <div id="dm_tab_text" class="tab active" onclick="setDmMessageType('text')">Text
                message</div>
            <div id="dm_tab_embed" class="tab" onclick="setDmMessageType('embed')">Embed message
            </div>
        </div>

        <!-- Text Editor -->
        <div id="dm_text_editor">
            <div class="config-label">Message Editor</div>

            <!-- Commands Frame -->
            <div class="flex flex-wrap gap-2 mb-3 p-3 bg-[#1e1f22] border border-[#333] rounded-lg">
                <span class="command-badge" onclick="insertDmCmd('{user}')">{user}</span>
                <span class="command-badge" onclick="insertDmCmd('{userid}')">{userid}</span>
                <span class="command-badge" onclick="insertDmCmd('{usertag}')">{usertag}</span>
                <span class="command-badge" onclick="insertDmCmd('{mention}')">{mention}</span>
                <span class="command-badge" onclick="insertDmCmd('{avatar}')">{avatar}</span>
                <span class="command-badge" onclick="insertDmCmd('{server}')">{server}</span>
                <span class="command-badge" onclick="insertDmCmd('{serverid}')">{serverid}</span>
                <span class="command-badge"
                    onclick="insertDmCmd('{membercount}')">{membercount}</span>
                <span class="command-badge" onclick="insertDmCmd('{members}')">{members}</span>
                <span class="command-badge" onclick="insertDmCmd('{date}')">{date}</span>
                <span class="command-badge" onclick="insertDmCmd('{time}')">{time}</span>
                <span class="command-badge" onclick="insertDmCmd('{role}')">{role}</span>
            </div>

            <div class="text-editor-container">
                <textarea id="dm_msg_input" class="text-editor"
                    oninput="updateDmValue('text', this.value)">Hey {user}, welcome to **{server}**!</textarea>
                <span id="dm_char_count" class="char-counter">36 / 2000</span>
            </div>

            <!-- Card Toggle -->
            <div class="card-toggle-container">
                <label class="switch">
                    <input type="checkbox" id="dm_card_toggle"
                        onchange="toggleDmCard(this.checked)">
                    <span class="slider"></span>
                </label>
                <span class="card-toggle-label">Send a welcome card in private message</span>
            </div>

            <!-- Card Settings (Nested) -->
            <div id="dm_card_settings" class="hidden mt-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-gray-400">Customize your
                        welcome card</h3>
                </div>

                <div>
                    <label class="config-label">Font</label>
                    <div class="relative">
                        <div class="dropdown-box" onclick="toggleDmDropdown('dm_font_dropdown')">
                            <span id="dm_current_font">Inter</span>
                            <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
                        </div>
                        <div id="dm_font_dropdown"
                            class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto custom-scrollbar">
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Inter]"
                                onclick="setDmCardFont('dm', 'Inter')">Inter</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Roboto]"
                                onclick="setDmCardFont('dm', 'Roboto')">Roboto</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Open Sans']"
                                onclick="setDmCardFont('dm', 'Open Sans')">Open Sans</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Source Sans 3']"
                                onclick="setDmCardFont('dm', 'Source Sans 3')">Source Sans 3</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Lato]"
                                onclick="setDmCardFont('dm', 'Lato')">Lato</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Montserrat]"
                                onclick="setDmCardFont('dm', 'Montserrat')">Montserrat</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Poppins]"
                                onclick="setDmCardFont('dm', 'Poppins')">Poppins</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Raleway]"
                                onclick="setDmCardFont('dm', 'Raleway')">Raleway</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Nunito]"
                                onclick="setDmCardFont('dm', 'Nunito')">Nunito</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Ubuntu]"
                                onclick="setDmCardFont('dm', 'Ubuntu')">Ubuntu</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['DM Sans']"
                                onclick="setDmCardFont('dm', 'DM Sans')">DM Sans</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Merriweather]"
                                onclick="setDmCardFont('dm', 'Merriweather')">Merriweather</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Playfair Display']"
                                onclick="setDmCardFont('dm', 'Playfair Display')">Playfair Display</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Oswald]"
                                onclick="setDmCardFont('dm', 'Oswald')">Oswald</div>
                            <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Bebas Neue']"
                                onclick="setDmCardFont('dm', 'Bebas Neue')">Bebas Neue</div>
                        </div>
                    </div>
                </div>
                <div>
                    <label class="config-label">Text color</label>
                    <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                        <div class="color-dot bg-white active" data-color="#ffffff"
                            onclick="setDmCardColor('dm', 'textColor', '#ffffff')"></div>
                        <div class="color-dot bg-[#f2f3f5]" data-color="#f2f3f5"
                            onclick="setDmCardColor('dm', 'textColor', '#f2f3f5')"></div>
                        <div class="color-dot bg-[#dbdee1]" data-color="#dbdee1"
                            onclick="setDmCardColor('dm', 'textColor', '#dbdee1')"></div>
                        <div class="color-dot bg-[#b5bac1]" data-color="#b5bac1"
                            onclick="setDmCardColor('dm', 'textColor', '#b5bac1')"></div>
                        <div class="color-dot bg-[#949ba4]" data-color="#949ba4"
                            onclick="setDmCardColor('dm', 'textColor', '#949ba4')"></div>
                        <div class="color-dot bg-[#80848e]" data-color="#80848e"
                            onclick="setDmCardColor('dm', 'textColor', '#80848e')"></div>
                        <div class="color-dot bg-[#5865f2]" data-color="#5865f2"
                            onclick="setDmCardColor('dm', 'textColor', '#5865f2')"></div>
                        <div class="color-dot bg-[#57f287]" data-color="#57f287"
                            onclick="setDmCardColor('dm', 'textColor', '#57f287')"></div>
                        <div class="color-dot bg-[#fee75c]" data-color="#fee75c"
                            onclick="setDmCardColor('dm', 'textColor', '#fee75c')"></div>
                        <div class="color-dot bg-[#ed4245]" data-color="#ed4245"
                            onclick="setDmCardColor('dm', 'textColor', '#ed4245')"></div>
                    </div>
                </div>

                <div>
                    <label class="config-label">Background color</label>
                    <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                        <div class="color-dot bg-[#0b0f17] active" data-color="#0b0f17"
                            onclick="setDmCardColor('dm', 'bgColor', '#0b0f17')"></div>
                        <div class="color-dot bg-[#111827]" data-color="#111827"
                            onclick="setDmCardColor('dm', 'bgColor', '#111827')"></div>
                        <div class="color-dot bg-[#1f2937]" data-color="#1f2937"
                            onclick="setDmCardColor('dm', 'bgColor', '#1f2937')"></div>
                        <div class="color-dot bg-[#0f172a]" data-color="#0f172a"
                            onclick="setDmCardColor('dm', 'bgColor', '#0f172a')"></div>
                        <div class="color-dot bg-[#111827]" data-color="#111827"
                            onclick="setDmCardColor('dm', 'bgColor', '#111827')"></div>
                        <div class="color-dot bg-[#1e1b4b]" data-color="#1e1b4b"
                            onclick="setDmCardColor('dm', 'bgColor', '#1e1b4b')"></div>
                        <div class="color-dot bg-[#0f766e]" data-color="#0f766e"
                            onclick="setDmCardColor('dm', 'bgColor', '#0f766e')"></div>
                        <div class="color-dot bg-[#3b0764]" data-color="#3b0764"
                            onclick="setDmCardColor('dm', 'bgColor', '#3b0764')"></div>
                        <div class="color-dot bg-[#0f2a3f]" data-color="#0f2a3f"
                            onclick="setDmCardColor('dm', 'bgColor', '#0f2a3f')"></div>
                        <div class="color-dot bg-[#1f2937]" data-color="#1f2937"
                            onclick="setDmCardColor('dm', 'bgColor', '#1f2937')"></div>
                    </div>
                </div>
                <div>
                    <label class="config-label">Background image</label>
                    <div class="flex items-center gap-4">
                        <div class="img-upload img-upload-lg" id="dm_card_bg_button">
                            <i data-lucide="image" class="w-5 h-5"></i>
                        </div>
                        <div id="dm_card_bg_label" class="text-xs text-gray-500">No image selected</div>
                        <input type="file" id="dm_card_bg_input" accept="image/*" class="hidden" />
                    </div>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <label class="config-label mb-0">Overlay opacity</label>
                        <span id="dm_opacity_val" class="text-[10px] text-gray-500">50%</span>
                    </div>
                    <input type="range" class="range-slider" min="0" max="100" value="50"
                        oninput="updateDmCardValue('dm', 'opacity', this.value)">
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="config-label">Title</label>
                        <input type="text" class="custom-input"
                            placeholder="{user} just joined the server"
                            value="{user} just joined the server"
                            oninput="updateDmCardValue('dm', 'title', this.value)">
                    </div>
                    <div>
                        <label class="config-label">Subtitle</label>
                        <input type="text" class="custom-input"
                            placeholder="Member # {membercount}"
                            value="Member # {membercount}"
                            oninput="updateDmCardValue('dm', 'subtitle', this.value)">
                    </div>
                </div>
            </div>
        </div>

        <!-- Embed Editor -->
        <div id="dm_embed_editor" class="hidden space-y-6">
            <div class="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase">
                <i data-lucide="eye" class="w-3 h-3"></i> Preview
            </div>
            
            <div class="embed-stripe" id="dm_embed_stripe">
                <div class="space-y-6">
                    <div>
                        <div class="config-label">Stripe color</div>
                        <div class="flex gap-2 items-center">
                            <div class="w-6 h-6 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 cursor-pointer flex items-center justify-center overflow-hidden border border-white/20">
                                <i data-lucide="aperture" class="w-3 h-3 text-white"></i>
                            </div>
                            <div class="color-dot bg-white" onclick="setDmEmbedColor('#ffffff')"></div>
                            <div class="color-dot bg-gray-500 active" onclick="setDmEmbedColor('#6b7280')"></div>
                            <div class="color-dot bg-red-400" onclick="setDmEmbedColor('#f87171')"></div>
                            <div class="color-dot bg-orange-400" onclick="setDmEmbedColor('#fb923c')"></div>
                            <div class="color-dot bg-yellow-400" onclick="setDmEmbedColor('#fbbf24')"></div>
                            <div class="color-dot bg-green-400" onclick="setDmEmbedColor('#4ade80')"></div>
                            <div class="color-dot bg-blue-400" onclick="setDmEmbedColor('#5865f2')"></div>
                        </div>
                    </div>

                    <div class="flex gap-4 items-center">
                        <div class="img-upload" id="dm_embed_image_button">
                            <i data-lucide="image" class="w-5 h-5"></i>
                        </div>
                        <input type="file" id="dm_embed_image_input" accept="image/*" class="hidden" />
                        <div id="dm_embed_image_label" class="text-xs text-gray-500">No image selected</div>
                        <div class="flex-1">
                            <div class="config-label">Author</div>
                            <input type="text" 
                                class="custom-input bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                                placeholder="Author name"
                                id="dm_embed_author"
                                oninput="updateDmEmbedValue('author', this.value)">
                        </div>
                    </div>

                    <div>
                        <div class="config-label">Title text</div>
                        <input type="text" 
                            class="custom-input bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                            placeholder="Title text"
                            id="dm_embed_title"
                            oninput="updateDmEmbedValue('title', this.value)">
                    </div>

                    <div>
                        <div class="config-label">Message template</div>
                        <textarea class="text-editor h-24" placeholder="Description"
                            id="dm_embed_description"
                            oninput="updateDmEmbedValue('description', this.value)">Hey {user}, welcome to **{server}**!</textarea>
                    </div>
                    <div id="dm_embed_image_preview_wrap" class="hidden">
                        <div class="config-label">Image Preview</div>
                        <img id="dm_embed_image_preview" class="w-full max-w-[420px] rounded-lg border border-[#2b2d31]" alt="Embed preview">
                    </div>

                    <div>
                        <div class="config-label">Footer</div>
                        <input type="text" 
                            class="bg-[#1e1f22] border border-[#3f4147] rounded-md p-2 w-full text-sm outline-none focus:border-[#5865f2]"
                            placeholder="Footer text"
                            id="dm_embed_footer"
                            oninput="updateDmEmbedValue('footer', this.value)">
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="dm_preview_section" class="space-y-4 mt-6 hidden">
        <div class="config-label">Live Preview</div>
        <div class="unified-preview">
            <div class="welcome-card-preview w-full max-w-[520px] mx-auto" id="dm_card_preview_wrap">
                <div class="card-overlay" id="dm_card_overlay"></div>
                <div class="card-content">
                    <div class="card-avatar" id="dm_card_avatar_border">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lucky" alt="Avatar">
                    </div>
                    <div class="card-title" id="dm_card_title_text">User#0000 just joined the server</div>
                    <div class="card-subtitle" id="dm_card_subtitle_text">Member #5</div>
                </div>
            </div>
        </div>
    </div>
</div>
`;

window.initializeJoinPrivateMessage = function() {
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
        title: '{user} just joined the server',
        subtitle: 'Member # {membercount}',
        titleSize: 56,
        subtitleSize: 36
    };
    const defaultEmbedState = {
        author: '',
        title: '',
        description: 'Hey {user}, welcome to **{server}**!',
        footer: '',
        color: '#6b7280'
    };
    let dmDataLoadPromise = null;
    let dmDataLoaded = false;
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

    function ensureDmState() {
        if (!state.dm) state.dm = {};
        state.dm = mergeDeep(state.dm, {});
        if (!state.dm.type) state.dm.type = 'text';
        if (state.dm.text == null) state.dm.text = '';
        if (!state.dm.card) state.dm.card = {};
        state.dm.card = { ...defaultCardState, ...state.dm.card };
        if (!state.dm.embed) state.dm.embed = {};
        state.dm.embed = { ...defaultEmbedState, ...state.dm.embed };
        if (!state.dm.mode) state.dm.mode = 'text';
    }

    function renderPlaceholders(text) {
        const now = new Date();
        const pad = (n) => String(n).padStart(2, '0');
        const replacements = {
            '{user}': 'User#0000',
            '{userid}': '123456789012345678',
            '{usertag}': 'User#0000',
            '{mention}': '@User',
            '{avatar}': 'https://cdn.discordapp.com/embed/avatars/0.png',
            '{server}': 'My Server',
            '{serverid}': '123456789012345678',
            '{membercount}': '5',
            '{members}': '5',
            '{role}': 'Member',
            '{date}': `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`,
            '{time}': `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
        };
        let out = text || '';
        Object.keys(replacements).forEach((key) => {
            out = out.split(key).join(replacements[key]);
        });
        return out;
    }

    function getDmCardMaxWidth() {
        const wrap = document.getElementById('dm_card_preview_wrap');
        if (!wrap || !wrap.clientWidth) return 420;
        return Math.max(200, wrap.clientWidth - 140);
    }

    function fitDmCardText(el, baseSize, minSize) {
        if (!el) return;
        const maxWidth = getDmCardMaxWidth();
        let size = Math.max(minSize, Number(baseSize) || minSize);
        el.style.fontSize = `${size}px`;
        let safety = 0;
        while (el.scrollWidth > maxWidth && size > minSize && safety < 40) {
            size -= 2;
            el.style.fontSize = `${size}px`;
            safety += 1;
        }
    }

    function applyDmCardFontSizes() {
        const card = state.dm.card || defaultCardState;
        const titleEl = document.getElementById('dm_card_title_text');
        const subtitleEl = document.getElementById('dm_card_subtitle_text');
        const titleSize = Number(card.titleSize || defaultCardState.titleSize || 56);
        const subtitleSize = Number(card.subtitleSize || defaultCardState.subtitleSize || 36);
        fitDmCardText(titleEl, titleSize, 24);
        fitDmCardText(subtitleEl, subtitleSize, 18);
    }

    function applyDmCardUIFromState() {
        const card = state.dm.card || defaultCardState;
        const preview = document.getElementById('dm_preview_section');
        const currentFontEl = document.getElementById('dm_current_font');
        if (currentFontEl) currentFontEl.innerText = card.font || defaultCardState.font;
        toggleDmCard(!!card.enabled);
        setDmCardColor('dm', 'textColor', card.textColor || defaultCardState.textColor);
        setDmCardColor('dm', 'bgColor', card.bgColor || defaultCardState.bgColor);
        applyDmCardBackground(card.bgImage || '');
        if (preview) preview.classList.toggle('hidden', !card.enabled);
        if (card.bgImage) {
            const parts = card.bgImage.split('/');
            setDmCardBgLabel(parts[parts.length - 1] || 'Image selected');
        } else {
            setDmCardBgLabel('No image selected');
        }
        const opacityEl = document.getElementById('dm_opacity_val');
        if (opacityEl) opacityEl.innerText = `${card.opacity ?? defaultCardState.opacity}%`;
        const opacityInput = document.querySelector('#dm_card_settings input[type="range"]');
        if (opacityInput) opacityInput.value = card.opacity ?? defaultCardState.opacity;
        const titleInput = document.querySelector('#dm_card_settings input[placeholder*="just joined"]');
        if (titleInput) titleInput.value = card.title || defaultCardState.title;
        const subtitleInput = document.querySelector('#dm_card_settings input[placeholder*="Member #"]');
        if (subtitleInput) subtitleInput.value = card.subtitle || defaultCardState.subtitle;
        const titlePreview = document.getElementById('dm_card_title_text');
        if (titlePreview) titlePreview.innerText = renderPlaceholders(card.title || defaultCardState.title);
        const subtitlePreview = document.getElementById('dm_card_subtitle_text');
        if (subtitlePreview) subtitlePreview.innerText = renderPlaceholders(card.subtitle || defaultCardState.subtitle);
        applyDmCardFontSizes();
    }

    function applyDmEmbedUIFromState() {
        const embed = state.dm.embed || defaultEmbedState;
        const embedAuthor = document.getElementById('dm_embed_author');
        if (embedAuthor) embedAuthor.value = embed.author || '';
        const embedTitle = document.getElementById('dm_embed_title');
        if (embedTitle) embedTitle.value = embed.title || '';
        const embedDesc = document.getElementById('dm_embed_description');
        if (embedDesc) embedDesc.value = embed.description || defaultEmbedState.description;
        const embedFooter = document.getElementById('dm_embed_footer');
        if (embedFooter) embedFooter.value = embed.footer || '';
        setDmEmbedImageLabel(embed.image);
        setDmEmbedImagePreview(embed.image);
        if (embed.color) setDmEmbedColor(embed.color, true);
    }

    window.setDmMessageType = function(type, preserveCard = false) {
        const cardOn = !!state.dm?.card?.enabled || state.dm?.mode === 'card';
        if (!preserveCard && !cardOn) {
            setDmMode(type === 'embed' ? 'embed' : 'text');
        } else {
            state.dm.type = type;
        }
        const textEd = document.getElementById('dm_text_editor');
        const embedEd = document.getElementById('dm_embed_editor');
        const tabT = document.getElementById('dm_tab_text');
        const tabE = document.getElementById('dm_tab_embed');

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

    window.toggleDmDropdown = function(id) {
        const el = document.getElementById(id);
        if (!el) return;
        el.classList.toggle('hidden');
    };

    window.updateDmValue = function(key, val) {
        ensureDmState();
        const safeVal = (val == null) ? '' : val;
        state.dm[key] = safeVal;
        if (key === 'text') {
            const charCount = document.getElementById('dm_char_count');
            if(charCount) charCount.innerText = `${safeVal.length} / 2000`;
        }
        checkForChanges();
    };

    window.insertDmCmd = function(cmd) {
        const textarea = document.getElementById('dm_msg_input');
        if(!textarea) return;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;
        textarea.value = text.substring(0, start) + cmd + text.substring(end);
        textarea.focus();
        textarea.selectionStart = textarea.selectionEnd = start + cmd.length;
        updateDmValue('text', textarea.value);
    };

    // Card/Embed helpers (simplified wrappers)
    window.toggleDmCard = function(enabled) {
        const feature = 'dm';
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card.enabled = enabled;
        const settings = document.getElementById(`${feature}_card_settings`);
        const textarea = document.getElementById(`${feature}_msg_input`);
        const preview = document.getElementById('dm_preview_section');
        if (enabled) {
            setDmMode('card');
            if (settings) settings.classList.remove('hidden');
            if (preview) preview.classList.remove('hidden');
            if (textarea) {
                textarea.disabled = true;
                textarea.classList.add('opacity-50', 'cursor-not-allowed');
            }
        } else {
            setDmMode(state.dm.type === 'embed' ? 'embed' : 'text');
            if (settings) settings.classList.add('hidden');
            if (preview) preview.classList.add('hidden');
            if (textarea) {
                textarea.disabled = false;
                textarea.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }
        if (enabled) applyDmCardFontSizes();
        checkForChanges();
    };
    
    window.setDmCardFont = function(feature, font) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card.font = font;
        const currentFontEl = document.getElementById(`${feature}_current_font`);
        if (currentFontEl) currentFontEl.innerText = font;
        const dropdown = document.getElementById(`${feature}_font_dropdown`);
        if(dropdown) dropdown.classList.add('hidden');
        checkForChanges();
    };

    window.setDmCardColor = function(feature, key, color) {
        if (!state[feature]) state[feature] = {};
        if (!state[feature].card) state[feature].card = { ...defaultCardState };
        state[feature].card[key] = color;
        if (key === 'textColor') {
            const title = document.getElementById(`${feature}_card_title_text`);
            const border = document.getElementById(`${feature}_card_avatar_border`);
            if (title) title.style.color = color;
            if (border) border.style.borderColor = color;
        } else {
            applyDmCardBackground(state[feature].card.bgImage || '');
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
    
    window.updateDmCardValue = function(feature, key, val) {
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
            const text = renderPlaceholders(val || '');
            const el = document.getElementById(`${feature}_card_title_text`);
            if (el) el.innerText = text;
            applyDmCardFontSizes();
        }
        if (key === 'subtitle') {
            const text = renderPlaceholders(val || '');
            const el = document.getElementById(`${feature}_card_subtitle_text`);
            if (el) el.innerText = text;
            applyDmCardFontSizes();
        }
        checkForChanges();
    };

    window.setDmEmbedColor = function(color, suppressMode = false) {
        ensureDmState();
        if (!suppressMode) setDmMode('embed');
        state.dm.embed.color = color;
        const stripe = document.getElementById('dm_embed_stripe');
        if (stripe) stripe.style.borderLeftColor = color;
        
        // Update dots active state
        const container = document.querySelector('#dm_embed_editor .flex.gap-2.items-center');
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

    window.updateDmEmbedValue = function(key, val) {
        ensureDmState();
        setDmMode('embed');
        state.dm.embed[key] = val;
        checkForChanges();
    };

    function applyDmCardBackground(url) {
        const wrap = document.getElementById('dm_card_preview_wrap');
        if (!wrap) return;
        if (url) {
            wrap.style.backgroundImage = `url('${url}')`;
            wrap.style.backgroundSize = 'cover';
            wrap.style.backgroundPosition = 'center';
        } else {
            wrap.style.backgroundImage = 'none';
            wrap.style.backgroundColor = state.dm.card?.bgColor || defaultCardState.bgColor;
        }
    }

    function setDmCardBgLabel(text) {
        const label = document.getElementById('dm_card_bg_label');
        if (label) label.innerText = text;
    }

    function handleDmCardBgFile(file) {
        if (!file) return;
        pendingCardBgFile = file;
        if (pendingCardBgObjectUrl) URL.revokeObjectURL(pendingCardBgObjectUrl);
        pendingCardBgObjectUrl = URL.createObjectURL(file);
        state.dm.card.bgImage = pendingCardBgObjectUrl;
        applyDmCardBackground(pendingCardBgObjectUrl);
        setDmCardBgLabel(file.name);
        checkForChanges();
    }

    async function uploadDmCardImageIfNeeded() {
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
                state.dm.card.bgImage = data.url;
                applyDmCardBackground(data.url);
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

    function setDmEmbedImageLabel(urlOrName) {
        const label = document.getElementById('dm_embed_image_label');
        if (!label) return;
        if (!urlOrName) {
            label.innerText = 'No image selected';
            return;
        }
        const parts = String(urlOrName).split('/');
        label.innerText = parts[parts.length - 1] || 'Image selected';
    }

    function setDmEmbedImagePreview(url) {
        const wrap = document.getElementById('dm_embed_image_preview_wrap');
        const img = document.getElementById('dm_embed_image_preview');
        if (!wrap || !img) return;
        if (!url) {
            wrap.classList.add('hidden');
            img.removeAttribute('src');
            return;
        }
        wrap.classList.remove('hidden');
        img.src = url;
    }

    function handleDmEmbedImageFile(file) {
        if (!file) return;
        pendingEmbedImageFile = file;
        if (pendingEmbedImageObjectUrl) URL.revokeObjectURL(pendingEmbedImageObjectUrl);
        pendingEmbedImageObjectUrl = URL.createObjectURL(file);
        state.dm.embed.image = pendingEmbedImageObjectUrl;
        setDmEmbedImageLabel(file.name);
        setDmEmbedImagePreview(pendingEmbedImageObjectUrl);
        checkForChanges();
    }

    async function uploadDmEmbedImageIfNeeded() {
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
                state.dm.embed.image = data.url;
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

    function setDmMode(mode) {
        ensureDmState();
        state.dm.mode = mode;
        if (mode === 'card') {
            if (state.dm.card) state.dm.card.enabled = true;
        } else {
            state.dm.type = mode === 'embed' ? 'embed' : 'text';
        }
    }

    if (!window.__dmSaveWrapped) {
        const originalSave = window.saveChanges;
        if (typeof originalSave === 'function') {
            window.saveChanges = async function() {
                await uploadDmCardImageIfNeeded();
                await uploadDmEmbedImageIfNeeded();
                return originalSave();
            };
        } else {
            window.saveDmChanges = async function() {
                if (!guildId) return;
                await uploadDmCardImageIfNeeded();
                await uploadDmEmbedImageIfNeeded();
                try {
                    const response = await fetch(`/api/config/dm/${guildId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(state.dm)
                    });
                    if (response.ok) {
                        initialState.dm = JSON.parse(JSON.stringify(state.dm));
                        checkForChanges();
                    }
                } catch (e) { console.error("Save failed", e); }
            };
            window.saveChanges = window.saveDmChanges;
        }
        window.__dmSaveWrapped = true;
    }

    async function loadDmData() {
        if (!guildId) return;
        if (dmDataLoaded) return;
        if (dmDataLoadPromise) return dmDataLoadPromise;
        dmDataLoadPromise = (async () => {

            // Fetch Config
            try {
                const confResp = await fetch(`/api/config/dm/${guildId}`);
                const confData = await confResp.json();
                if (confData.success && confData.config) {
                    const toggleEl = document.getElementById('toggle_dm');
                    const preserveEnabled = toggleEl ? toggleEl.checked : state.dm?.enabled;
                    const mergedDm = mergeDeep(state.dm || {}, confData.config || {});
                    if (preserveEnabled !== undefined) mergedDm.enabled = preserveEnabled;
                    state.dm = mergedDm;
                    ensureDmState();
                    if (!window.__userToggledDm) {
                        initialState.dm = JSON.parse(JSON.stringify(state.dm));
                    }

                    const msgInput = document.getElementById('dm_msg_input');
                    if (msgInput) msgInput.value = state.dm.text || '';
                    const charCount = document.getElementById('dm_char_count');
                    if (charCount) charCount.innerText = `${(state.dm.text || '').length} / 2000`;
                    
                    const toggle = document.getElementById('toggle_dm');
                    if (toggle) toggle.checked = !!state.dm.enabled;
                    const section = document.getElementById('section_dm');
                    if (section) section.classList.toggle('active', !!state.dm.enabled);
                    
                    // Restore Card settings
                    if (state.dm.card) {
                        const cardToggle = document.getElementById('dm_card_toggle');
                        if (cardToggle) cardToggle.checked = !!state.dm.card.enabled;
                        applyDmCardUIFromState();
                    }

                    // Restore Embed settings
                    if (state.dm.embed) applyDmEmbedUIFromState();

                    // Correct Load Logic from Report 5
                    if (state.dm.mode === 'card' || state.dm.card?.enabled) {
                        const cardToggle = document.getElementById('dm_card_toggle');
                        if (cardToggle) cardToggle.checked = true;
                        toggleDmCard(true);
                    }
                    
                    if (state.dm.type) {
                        setDmMessageType(state.dm.type, true);
                    }
                    checkForChanges();
                }
            } catch (e) { console.error("Failed to load dm config", e); }
            dmDataLoaded = true;
        })();
        return dmDataLoadPromise;
    }

    const bgButton = document.getElementById('dm_card_bg_button');
    const bgInput = document.getElementById('dm_card_bg_input');
    if (bgButton && bgInput) {
        bgButton.addEventListener('click', () => bgInput.click());
        bgInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            handleDmCardBgFile(file);
        });
    }
    const embedImageButton = document.getElementById('dm_embed_image_button');
    const embedImageInput = document.getElementById('dm_embed_image_input');
    if (embedImageButton && embedImageInput) {
        embedImageButton.addEventListener('click', () => embedImageInput.click());
        embedImageInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            handleDmEmbedImageFile(file);
        });
    }

    ensureDmState();
    if (!window.__dmCardResizeBound) {
        window.addEventListener('resize', () => {
            if (state.dm && state.dm.card && state.dm.card.enabled) {
                applyDmCardFontSizes();
            }
        });
        window.__dmCardResizeBound = true;
    }
    loadDmData();
    if (window.lucide) window.lucide.createIcons();
};

