window.SCHEDULED_MESSAGE_HTML = `
<style>
    .sa-container {
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 18px;
        overflow: visible !important;
        min-height: 450px;
    }
    .sa-container.picker-active {
        min-height: 600px;
    }
    .sa-input-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .sa-entry-row {
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
    }
    .sa-square-btn {
        width: 44px;
        height: 44px;
        background-color: #2b2d31;
        border: 1px solid #3f4147;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #b5bac1;
        transition: all 0.2s;
        flex-shrink: 0;
    }
    .sa-square-btn:hover {
        background-color: #35373c;
        border-color: #5865f2;
        color: #fff;
    }
    .sa-input {
        flex: 1;
        background-color: #1e1f22;
        border: 1px solid #3f4147;
        border-radius: 8px;
        padding: 12px 16px;
        color: #fff;
        font-size: 14px;
        outline: none;
        transition: border-color 0.2s;
    }
    .sa-input:focus {
        border-color: #5865f2;
    }
    .sa-countdown-label {
        font-size: 14px;
        font-weight: 600;
        color: #b5bac1;
        padding: 0;
        margin-top: -4px;
    }
    .sa-countdown-highlight {
        color: #5865f2;
        font-family: 'Golos Text', sans-serif;
        font-weight: 700;
    }
    .sa-picker-popup {
        position: absolute;
        top: 50px;
        left: 0;
        background: #111214;
        border: 1px solid #3f4147;
        border-radius: 8px;
        z-index: 1000;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        padding: 12px;
        display: none;
        width: 280px;
    }
    .time-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        text-align: center;
    }
    .time-col label { font-size: 10px; color: #949ba4; text-transform: uppercase; }
    .time-col input {
        width: 100%; background: #1e1f22; border: 1px solid #333;
        color: #fff; border-radius: 4px; padding: 8px; text-align: center;
    }
    .cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
    .cal-day-name { font-size: 10px; color: #555; text-align: center; padding: 4px 0; }
    .cal-cell {
        font-size: 12px; text-align: center; padding: 8px 0; cursor: pointer; border-radius: 4px; color: #dbdee1;
    }
    .cal-cell:hover:not(.disabled) { background: #35373c; }
    .cal-cell.active { background: #5865f2; color: #fff; }
    .cal-cell.disabled { color: #444; cursor: not-allowed; }

    .tabs-container {
        display: flex;
        gap: 8px;
        background: #111214;
        border: 1px solid #2b2d31;
        border-radius: 10px;
        padding: 6px;
        width: fit-content;
    }
    .tab-btn {
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 700;
        color: #949ba4;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s;
        user-select: none;
    }
    .tab-btn.active {
        color: #fff;
        background: #35373c;
    }

    .config-label {
        font-size: 11px;
        font-weight: 700;
        color: #949ba4;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 6px;
    }
    .command-badge {
        padding: 4px 8px;
        border-radius: 6px;
        background: #2b2d31;
        border: 1px solid #3f4147;
        font-size: 11px;
        color: #b5bac1;
        cursor: pointer;
    }
    .text-editor-container { position: relative; }
    .text-editor {
        width: 100%;
        min-height: 140px;
        background: #1e1f22;
        border: 1px solid #333;
        border-radius: 10px;
        color: #fff;
        padding: 12px 14px 26px;
        resize: vertical;
        outline: none;
    }
    .char-counter {
        position: absolute;
        right: 12px;
        bottom: 8px;
        font-size: 11px;
        color: #6b7280;
    }
    .custom-input {
        background: #1e1f22;
        border: 1px solid #3f4147;
        border-radius: 8px;
        padding: 10px 12px;
        color: #fff;
        font-size: 13px;
        width: 100%;
        outline: none;
    }
    .range-slider { width: 100%; accent-color: #5865f2; }
    .img-upload {
        width: 42px;
        height: 42px;
        border-radius: 8px;
        border: 1px dashed #3f4147;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #1e1f22;
        cursor: pointer;
        color: #949ba4;
    }
    .img-upload-lg { width: 54px; height: 54px; }

    .welcome-card-preview {
        width: 100%;
        border-radius: 8px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        background-color: #000;
        background-size: cover;
        background-position: center;
        transition: all 0.3s;
    }
    .card-overlay {
        position: absolute;
        inset: 0;
        background-color: rgba(0, 0, 0, 0.5);
        transition: background-color 0.2s;
    }
    .card-content {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        text-align: center;
    }
    .card-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid #fff;
        overflow: hidden;
    }
    .card-title { font-size: 20px; font-weight: 700; color: #fff; }
    .card-subtitle { font-size: 14px; font-weight: 600; color: #aaa; }

    .embed-input {
        border: 1px solid #3f4147;
        border-radius: 4px;
        padding: 4px 8px;
        transition: border-color 0.2s;
    }
    .embed-input:focus { border-color: #5865f2; }
    .color-dot {
        width: 24px; height: 24px; border-radius: 50%; cursor: pointer;
        border: 2px solid transparent; display: flex; align-items: center; justify-content: center;
        transition: all 0.2s;
    }
    .color-dot.active { border-color: white; box-shadow: 0 0 8px rgba(255, 255, 255, 0.4); }
    .color-dot.active::after {
        content: ''; width: 6px; height: 10px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); margin-bottom: 2px;
    }
</style>

<div class="sa-container">
    <div class="action-btns justify-end">
        <span id="sa_editing_label" class="text-sm font-semibold text-gray-300 mr-auto hidden">Editing</span>
        <button class="btn btn-discard" onclick="discardConfig()">Discard</button>
        <button class="btn btn-save" id="saSaveBtn" onclick="saveConfig(false)">Save</button>
        <button class="btn btn-publish" id="saPostBtn" onclick="saveConfig(true)">Post</button>
    </div>
    <div class="sa-input-group">
        <label class="config-label">Welcome Message Channel *</label>
        <div class="relative">
            <div class="dropdown-box" onclick="toggleSaDropdown('sa_channel_dropdown')">
                <span id="sa_current_channel" class="flex items-center gap-2 text-gray-400">
                    <i data-lucide="hash" class="w-4 h-4"></i> Select a channel
                </span>
                <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
            </div>
            <div id="sa_channel_dropdown" class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-50 p-2 max-h-48 overflow-y-auto custom-scrollbar">
                <div class="p-2 text-sm text-gray-500">Loading channels...</div>
            </div>
        </div>
    </div>

    <div class="sa-input-group">
        <label class="config-label">Scheduled Time (24h)</label>
        <div class="sa-entry-row">
            <div class="sa-square-btn" onclick="toggleSaPicker('sa_time_picker')">
                <i data-lucide="clock" class="w-5 h-5"></i>
            </div>
            <input type="text" id="sa_time_input" class="sa-input" placeholder="00:00:00" readonly onclick="toggleSaPicker('sa_time_picker')">
            <div id="sa_time_picker" class="sa-picker-popup">
                <div class="time-grid">
                    <div class="time-col"><label>Hr</label><input type="number" id="p_hour" min="0" max="23" value="00"></div>
                    <div class="time-col"><label>Min</label><input type="number" id="p_min" min="0" max="59" value="00"></div>
                    <div class="time-col"><label>Sec</label><input type="number" id="p_sec" min="0" max="59" value="00"></div>
                </div>
                <button class="btn btn-publish w-full mt-4 !py-2" onclick="applySaTime()">Set Time</button>
            </div>
        </div>
    </div>

    <div class="sa-input-group">
        <label class="config-label">Scheduled Date</label>
        <div class="sa-entry-row">
            <div class="sa-square-btn" onclick="toggleSaPicker('sa_date_picker')">
                <i data-lucide="calendar" class="w-5 h-5"></i>
            </div>
            <input type="text" id="sa_date_input" class="sa-input" placeholder="MMM DD, YYYY" readonly onclick="toggleSaPicker('sa_date_picker')">
            <div id="sa_date_picker" class="sa-picker-popup">
                <div class="cal-header">
                    <i data-lucide="chevron-left" class="w-4 h-4 cursor-pointer" onclick="changeSaMonth(-1)"></i>
                    <span id="cal_month_year" class="text-sm font-bold text-white"></span>
                    <i data-lucide="chevron-right" class="w-4 h-4 cursor-pointer" onclick="changeSaMonth(1)"></i>
                </div>
                <div class="cal-grid" id="cal_grid"></div>
            </div>
        </div>
    </div>

    <div id="sa_countdown_label" class="sa-countdown-label">
        Message will appear in <span id="sa_timer_val" class="sa-countdown-highlight">00:00:00</span> and in <span id="sa_days_val" class="sa-countdown-highlight">0</span> days left
    </div>

    <div class="tabs-container">
        <div id="sa_tab_text" class="tab-btn active" onclick="saSwitchTab('text')">Text Message</div>
        <div id="sa_tab_card" class="tab-btn" onclick="saSwitchTab('card')">Welcome Card</div>
        <div id="sa_tab_embed" class="tab-btn" onclick="saSwitchTab('embed')">Embeded Message</div>
    </div>

    <div id="sa_tab_content_text">
        <div class="config-label">Message Editor</div>
        <div class="flex flex-wrap gap-2 mb-3 p-3 bg-[#1e1f22] border border-[#333] rounded-lg">
            <span class="command-badge" onclick="insertSaCmd('{user}')">{user}</span>
            <span class="command-badge" onclick="insertSaCmd('{userid}')">{userid}</span>
            <span class="command-badge" onclick="insertSaCmd('{usertag}')">{usertag}</span>
            <span class="command-badge" onclick="insertSaCmd('{mention}')">{mention}</span>
            <span class="command-badge" onclick="insertSaCmd('{avatar}')">{avatar}</span>
            <span class="command-badge" onclick="insertSaCmd('{server}')">{server}</span>
            <span class="command-badge" onclick="insertSaCmd('{serverid}')">{serverid}</span>
            <span class="command-badge" onclick="insertSaCmd('{membercount}')">{membercount}</span>
            <span class="command-badge" onclick="insertSaCmd('{date}')">{date}</span>
            <span class="command-badge" onclick="insertSaCmd('{time}')">{time}</span>
        </div>
        <div class="text-editor-container">
            <textarea id="sa_text_input" class="text-editor" oninput="updateSaText(this.value)">Hey {user}, welcome to **{server}**!</textarea>
            <span id="sa_char_count" class="char-counter">36 / 2000</span>
        </div>
    </div>

    <div id="sa_tab_content_card" class="hidden space-y-6">
        <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-gray-400">Customize your welcome card</h3>
        </div>

        <div>
            <label class="config-label">Font</label>
            <div class="relative">
                <div class="dropdown-box" onclick="toggleSaCardDropdown('sa_font_dropdown')">
                    <span id="sa_current_font">Inter</span>
                    <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
                </div>
                <div id="sa_font_dropdown" class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto custom-scrollbar">
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Inter]" onclick="setSaCardFont('Inter')">Inter</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Roboto]" onclick="setSaCardFont('Roboto')">Roboto</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Open Sans']" onclick="setSaCardFont('Open Sans')">Open Sans</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Source Sans 3']" onclick="setSaCardFont('Source Sans 3')">Source Sans 3</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Lato]" onclick="setSaCardFont('Lato')">Lato</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Montserrat]" onclick="setSaCardFont('Montserrat')">Montserrat</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Poppins]" onclick="setSaCardFont('Poppins')">Poppins</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Raleway]" onclick="setSaCardFont('Raleway')">Raleway</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Nunito]" onclick="setSaCardFont('Nunito')">Nunito</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Ubuntu]" onclick="setSaCardFont('Ubuntu')">Ubuntu</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['DM Sans']" onclick="setSaCardFont('DM Sans')">DM Sans</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Merriweather]" onclick="setSaCardFont('Merriweather')">Merriweather</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Playfair Display']" onclick="setSaCardFont('Playfair Display')">Playfair Display</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Oswald]" onclick="setSaCardFont('Oswald')">Oswald</div>
                    <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Bebas Neue']" onclick="setSaCardFont('Bebas Neue')">Bebas Neue</div>
                </div>
            </div>
        </div>

        <div>
            <label class="config-label">Text color</label>
            <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                <div class="color-dot bg-white active" data-color="#ffffff" onclick="setSaCardColor('textColor', '#ffffff')"></div>
                <div class="color-dot bg-[#f2f3f5]" data-color="#f2f3f5" onclick="setSaCardColor('textColor', '#f2f3f5')"></div>
                <div class="color-dot bg-[#dbdee1]" data-color="#dbdee1" onclick="setSaCardColor('textColor', '#dbdee1')"></div>
                <div class="color-dot bg-[#b5bac1]" data-color="#b5bac1" onclick="setSaCardColor('textColor', '#b5bac1')"></div>
                <div class="color-dot bg-[#949ba4]" data-color="#949ba4" onclick="setSaCardColor('textColor', '#949ba4')"></div>
                <div class="color-dot bg-[#80848e]" data-color="#80848e" onclick="setSaCardColor('textColor', '#80848e')"></div>
                <div class="color-dot bg-[#5865f2]" data-color="#5865f2" onclick="setSaCardColor('textColor', '#5865f2')"></div>
                <div class="color-dot bg-[#57f287]" data-color="#57f287" onclick="setSaCardColor('textColor', '#57f287')"></div>
                <div class="color-dot bg-[#fee75c]" data-color="#fee75c" onclick="setSaCardColor('textColor', '#fee75c')"></div>
                <div class="color-dot bg-[#ed4245]" data-color="#ed4245" onclick="setSaCardColor('textColor', '#ed4245')"></div>
            </div>
        </div>

        <div>
            <label class="config-label">Background color</label>
            <div class="flex flex-wrap gap-2 items-center h-auto min-h-10 color-picker-row">
                <div class="color-dot bg-[#0b0f17] active" data-color="#0b0f17" onclick="setSaCardColor('bgColor', '#0b0f17')"></div>
                <div class="color-dot bg-[#111827]" data-color="#111827" onclick="setSaCardColor('bgColor', '#111827')"></div>
                <div class="color-dot bg-[#1f2937]" data-color="#1f2937" onclick="setSaCardColor('bgColor', '#1f2937')"></div>
                <div class="color-dot bg-[#0f172a]" data-color="#0f172a" onclick="setSaCardColor('bgColor', '#0f172a')"></div>
                <div class="color-dot bg-[#1e1b4b]" data-color="#1e1b4b" onclick="setSaCardColor('bgColor', '#1e1b4b')"></div>
                <div class="color-dot bg-[#0f766e]" data-color="#0f766e" onclick="setSaCardColor('bgColor', '#0f766e')"></div>
                <div class="color-dot bg-[#3b0764]" data-color="#3b0764" onclick="setSaCardColor('bgColor', '#3b0764')"></div>
                <div class="color-dot bg-[#0f2a3f]" data-color="#0f2a3f" onclick="setSaCardColor('bgColor', '#0f2a3f')"></div>
                <div class="color-dot bg-[#1f2937]" data-color="#1f2937" onclick="setSaCardColor('bgColor', '#1f2937')"></div>
            </div>
        </div>

        <div>
            <label class="config-label">Background image</label>
            <div class="flex items-center gap-4">
                <div class="img-upload img-upload-lg" id="sa_card_bg_button">
                    <i data-lucide="image" class="w-5 h-5"></i>
                </div>
                <div id="sa_card_bg_label" class="text-xs text-gray-500">No image selected</div>
                <input type="file" id="sa_card_bg_input" accept="image/*" class="hidden" />
            </div>
        </div>

        <div>
            <div class="flex justify-between items-center mb-1">
                <label class="config-label mb-0">Overlay opacity</label>
                <span id="sa_opacity_val" class="text-[10px] text-gray-500">50%</span>
            </div>
            <input type="range" class="range-slider" min="0" max="100" value="50" oninput="updateSaCardValue('opacity', this.value)">
        </div>

        <div class="space-y-4">
            <div>
                <label class="config-label">Title</label>
                <input type="text" class="custom-input" placeholder="{user} just joined the server" value="{user} just joined the server" oninput="updateSaCardValue('title', this.value)">
            </div>
            <div>
                <label class="config-label">Subtitle</label>
                <input type="text" class="custom-input" placeholder="Member # {membercount}" value="Member # {membercount}" oninput="updateSaCardValue('subtitle', this.value)">
            </div>
        </div>

        <div class="welcome-card-preview w-full max-w-[520px] mx-auto" id="sa_card_preview_wrap">
            <div class="card-overlay" id="sa_card_overlay"></div>
            <div class="card-content">
                <div class="card-avatar" id="sa_card_avatar_border">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lucky" alt="Avatar">
                </div>
                <div class="card-title" id="sa_card_title_text">User#0000 just joined the server</div>
                <div class="card-subtitle" id="sa_card_subtitle_text">Member #5</div>
            </div>
        </div>
    </div>

    <div id="sa_tab_content_embed" class="hidden">
        <div class="config-content space-y-6">
            <div>
                <h2 class="text-white font-bold text-lg">Embed message builder</h2>
                <p class="text-gray-400 text-xs mt-1">Create your embed with optional message the way you want it</p>
            </div>

            <div class="space-y-2">
                <div class="bg-[#111214] border border-[#2b2d31] rounded-lg p-2">
                    <textarea id="reaction_msg_main" class="w-full bg-transparent border-none outline-none text-sm text-white resize-none placeholder-gray-600 h-10" placeholder="React to this message to get your roles!">React to this message to get your roles!</textarea>
                </div>
            </div>

            <div class="flex items-center gap-3">
                <div class="flex flex-wrap gap-2" id="color_picker_list">
                    <div class="color-dot bg-white active" data-color="#ffffff" onclick="setEmbedThemeColor(this, '#ffffff')"></div>
                    <div class="color-dot bg-[#6b7280]" data-color="#6b7280" onclick="setEmbedThemeColor(this, '#6b7280')"></div>
                    <div class="color-dot bg-[#ef4444]" data-color="#ef4444" onclick="setEmbedThemeColor(this, '#ef4444')"></div>
                    <div class="color-dot bg-[#f97316]" data-color="#f97316" onclick="setEmbedThemeColor(this, '#f97316')"></div>
                    <div class="color-dot bg-[#f59e0b]" data-color="#f59e0b" onclick="setEmbedThemeColor(this, '#f59e0b')"></div>
                    <div class="color-dot bg-[#10b981]" data-color="#10b981" onclick="setEmbedThemeColor(this, '#10b981')"></div>
                    <div class="color-dot bg-[#14b8a6]" data-color="#14b8a6" onclick="setEmbedThemeColor(this, '#14b8a6')"></div>
                    <div class="color-dot bg-[#0ea5e9]" data-color="#0ea5e9" onclick="setEmbedThemeColor(this, '#0ea5e9')"></div>
                    <div class="color-dot bg-[#3b82f6]" data-color="#3b82f6" onclick="setEmbedThemeColor(this, '#3b82f6')"></div>
                    <div class="color-dot bg-[#8b5cf6]" data-color="#8b5cf6" onclick="setEmbedThemeColor(this, '#8b5cf6')"></div>
                </div>
            </div>

            <div class="relative bg-[#1e1f22] rounded-md border-l-4 border-white p-4 max-w-2xl" id="embed_preview_frame">
                <div class="flex flex-col gap-3">
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 rounded-full border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31]" onclick="document.getElementById('header_img_input').click()">
                            <img id="header_img_preview" src="" class="hidden w-full h-full object-cover">
                            <i data-lucide="image" class="w-5 h-5 text-gray-500" id="header_img_icon"></i>
                        </div>
                        <input type="text" class="bg-transparent outline-none text-sm text-gray-400 w-full embed-input" placeholder="Header" id="embed_header_text">
                        <input type="file" id="header_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'header_img_preview', 'header_img_icon')">
                    </div>

                    <div class="flex justify-between gap-4">
                        <div class="flex-1 space-y-2">
                            <input type="text" class="bg-transparent outline-none text-base font-bold text-white w-full embed-input" placeholder="Title" id="embed_title_text">
                            <textarea class="w-full bg-transparent outline-none text-sm text-gray-300 resize-none h-10 embed-input" placeholder="React to this message to get your roles!" id="embed_desc_text">React to this message to get your roles!</textarea>
                            <div class="space-y-1">
                                <input type="text" class="bg-transparent outline-none text-xs font-bold text-white w-full embed-input" placeholder="Field name" id="embed_field_name">
                                <input type="text" class="bg-transparent outline-none text-xs text-gray-300 w-full embed-input" placeholder="Field value" id="embed_field_value">
                            </div>
                        </div>

                        <div class="w-24 h-24 rounded-lg border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31] shrink-0" onclick="document.getElementById('thumb_img_input').click()">
                            <img id="thumb_img_preview" src="" class="hidden w-full h-full object-cover">
                            <i data-lucide="image" class="w-12 h-12 text-gray-500" id="thumb_img_icon"></i>
                            <input type="file" id="thumb_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'thumb_img_preview', 'thumb_img_icon')">
                        </div>
                    </div>

                    <div class="w-full h-28 rounded-lg border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31] mt-2" onclick="document.getElementById('main_img_input').click()">
                        <img id="main_img_preview" src="" class="hidden w-full h-full object-cover">
                        <i data-lucide="image" class="w-10 h-10 text-gray-500" id="main_img_icon"></i>
                        <input type="file" id="main_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'main_img_preview', 'main_img_icon')">
                    </div>

                    <div class="flex items-center gap-2 mt-2 opacity-60">
                        <div class="w-6 h-6 rounded-full border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31]" onclick="document.getElementById('footer_img_input').click()">
                            <img id="footer_img_preview" src="" class="hidden w-full h-full object-cover">
                            <i data-lucide="image" class="w-4 h-4 text-gray-500" id="footer_img_icon"></i>
                        </div>
                        <input type="text" class="bg-transparent outline-none text-xs text-gray-400 w-full embed-input" placeholder="Footer" id="embed_footer_text">
                        <input type="file" id="footer_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'footer_img_preview', 'footer_img_icon')">
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
`;

window.initializeScheduledMessage = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const guildId = urlParams.get('guild_id');

    if (!window.scheduledState) {
        window.scheduledState = {
            scheduled_datetime: new Date(new Date().getTime() + 10 * 60000),
            channel: null,
            channel_name: null,
            message_type: 'text',
            text: 'Hey {user}, welcome to **{server}**!',
            card: {
                font: 'Inter',
                textColor: '#ffffff',
                bgColor: '#0b0f17',
                bgImage: '',
                opacity: 50,
                title: '{user} just joined the server',
                subtitle: 'Member # {membercount}'
            },
            embed: { color: '#ffffff' },
            calViewDate: new Date()
        };
    }

    const format24h = (dt) => `${String(dt.getHours()).padStart(2, '0')}:${String(dt.getMinutes()).padStart(2, '0')}:${String(dt.getSeconds()).padStart(2, '0')}`;
    const formatDate = (dt) => {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return `${months[dt.getMonth()]} ${String(dt.getDate()).padStart(2, '0')}, ${dt.getFullYear()}`;
    };

    window.toggleSaPicker = function(id) {
        const picker = document.getElementById(id);
        const container = document.querySelector('.sa-container');
        const isHidden = picker.style.display !== 'block';
        document.querySelectorAll('.sa-picker-popup').forEach(p => p.style.display = 'none');
        if (isHidden) {
            picker.style.display = 'block';
            if (container) container.classList.add('picker-active');
            if (id === 'sa_date_picker') renderCalendar();
            if (id === 'sa_time_picker') {
                const dt = window.scheduledState.scheduled_datetime;
                document.getElementById('p_hour').value = dt.getHours();
                document.getElementById('p_min').value = dt.getMinutes();
                document.getElementById('p_sec').value = dt.getSeconds();
            }
        } else if (container) {
            container.classList.remove('picker-active');
        }
    };

    window.applySaTime = function() {
        const h = parseInt(document.getElementById('p_hour').value) || 0;
        const m = parseInt(document.getElementById('p_min').value) || 0;
        const s = parseInt(document.getElementById('p_sec').value) || 0;
        const newDt = new Date(window.scheduledState.scheduled_datetime);
        newDt.setHours(h, m, s);
        if (newDt <= new Date()) {
            window.scheduledState.scheduled_datetime = new Date(new Date().getTime() + 10 * 60000);
        } else {
            window.scheduledState.scheduled_datetime = newDt;
        }
        updateDateTimeDisplay();
        document.getElementById('sa_time_picker').style.display = 'none';
        const container = document.querySelector('.sa-container');
        if (container) container.classList.remove('picker-active');
    };

    window.changeSaMonth = function(dir) {
        window.scheduledState.calViewDate.setMonth(window.scheduledState.calViewDate.getMonth() + dir);
        renderCalendar();
    };

    function renderCalendar() {
        const viewDt = window.scheduledState.calViewDate;
        const month = viewDt.getMonth();
        const year = viewDt.getFullYear();
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        document.getElementById('cal_month_year').innerText = `${months[month]} ${year}`;
        const grid = document.getElementById('cal_grid');
        grid.innerHTML = '';
        ['S','M','T','W','T','F','S'].forEach(d => grid.innerHTML += `<div class="cal-day-name">${d}</div>`);
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();
        today.setHours(0,0,0,0);
        for (let i = 0; i < firstDay; i++) grid.innerHTML += '<div></div>';
        for (let d = 1; d <= daysInMonth; d++) {
            const cellDate = new Date(year, month, d);
            const isDisabled = cellDate < today;
            const isActive = cellDate.toDateString() === window.scheduledState.scheduled_datetime.toDateString();
            const cell = document.createElement('div');
            cell.className = `cal-cell ${isDisabled ? 'disabled' : ''} ${isActive ? 'active' : ''}`;
            cell.innerText = d;
            if (!isDisabled) {
                cell.onclick = () => {
                    const current = window.scheduledState.scheduled_datetime;
                    const newDt = new Date(year, month, d, current.getHours(), current.getMinutes(), current.getSeconds());
                    if (newDt <= new Date()) {
                        window.scheduledState.scheduled_datetime = new Date(new Date().getTime() + 10 * 60000);
                    } else {
                        window.scheduledState.scheduled_datetime = newDt;
                    }
                    updateDateTimeDisplay();
                    document.getElementById('sa_date_picker').style.display = 'none';
                    const container = document.querySelector('.sa-container');
                    if (container) container.classList.remove('picker-active');
                };
            }
            grid.appendChild(cell);
        }
    }

    window.updateDateTimeDisplay = function() {
        document.getElementById('sa_time_input').value = format24h(window.scheduledState.scheduled_datetime);
        document.getElementById('sa_date_input').value = formatDate(window.scheduledState.scheduled_datetime);
        updateCountdown();
    };

    function updateCountdown() {
        const targetDt = window.scheduledState.scheduled_datetime;
        const now = new Date();
        const diff = targetDt - now;
        const label = document.getElementById('sa_countdown_label');
        if (!label) return;
        if (diff <= 0) {
            label.innerHTML = '<span class="text-red-500 font-bold">Scheduled time has already passed!</span>';
            return;
        }
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        const timerStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        label.innerHTML = `Message will appear in <span class="sa-countdown-highlight">${timerStr}</span> and in <span class="sa-countdown-highlight">${days}</span> days left`;
    }

    async function loadChannels() {
        if (!guildId) return;
        try {
            const resp = await fetch(`/api/scheduled-announcements/channels/${guildId}`);
            const data = await resp.json();
            if (data.success && data.channels) {
                const dropdown = document.getElementById('sa_channel_dropdown');
                dropdown.innerHTML = '';
                data.channels.forEach(ch => {
                    const item = document.createElement('div');
                    item.className = 'dropdown-item';
                    item.innerHTML = `# ${ch.name}`;
                    item.onclick = () => {
                        window.scheduledState.channel = ch.id;
                        window.scheduledState.channel_name = ch.name;
                        document.getElementById('sa_current_channel').innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${ch.name}`;
                        document.getElementById('sa_current_channel').classList.remove('text-gray-400');
                        dropdown.classList.add('hidden');
                    };
                    dropdown.appendChild(item);
                });
                if (window.lucide) window.lucide.createIcons();
            }
        } catch (e) { console.error(e); }
    }

    window.toggleSaDropdown = (id) => document.getElementById(id).classList.toggle('hidden');

    window.loadScheduledConfigFromItem = function(item) {
        if (!item) return;
        if (item.scheduled_time) {
            const parsed = new Date(item.scheduled_time);
            if (!isNaN(parsed.getTime())) {
                window.scheduledState.scheduled_datetime = parsed;
            }
        }
        window.scheduledState.channel = item.channel_id || null;
        window.scheduledState.channel_name = item.channel_name || null;
        window.scheduledState.message_type = item.message_type || 'text';

        if (item.message_type === 'card' && item.message && item.message.card) {
            window.scheduledState.card = { ...window.scheduledState.card, ...item.message.card };
        } else if (item.message_type === 'embed' && item.message && item.message.embed) {
            window.scheduledState.embed = { ...window.scheduledState.embed, ...item.message.embed };
        } else if (item.message && item.message.content !== undefined) {
            window.scheduledState.text = item.message.content;
        }

        updateDateTimeDisplay();

        if (window.scheduledState.channel_name) {
            const label = document.getElementById('sa_current_channel');
            if (label) {
                label.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${window.scheduledState.channel_name}`;
                label.classList.remove('text-gray-400');
            }
        }

        const textInput = document.getElementById('sa_text_input');
        if (textInput) textInput.value = window.scheduledState.text || '';
        window.updateSaText(window.scheduledState.text || '');

        const fontLabel = document.getElementById('sa_current_font');
        if (fontLabel) fontLabel.innerText = window.scheduledState.card.font || 'Inter';
        const titleInput = document.querySelector('#sa_tab_content_card input[placeholder*="just joined"]');
        if (titleInput) titleInput.value = window.scheduledState.card.title || '';
        const subtitleInput = document.querySelector('#sa_tab_content_card input[placeholder*="Member #"]');
        if (subtitleInput) subtitleInput.value = window.scheduledState.card.subtitle || '';
        const bgLabel = document.getElementById('sa_card_bg_label');
        if (bgLabel) bgLabel.innerText = window.scheduledState.card.bgImage ? (window.scheduledState.card.bgImage.split('/').pop() || 'Image selected') : 'No image selected';
        applyCardStyles();

        if (item.message_type === 'embed' && item.message && item.message.embed) {
            restoreEmbedUI({
                ...item.message.embed,
                content: item.message.embed.content || item.message.content || ''
            });
        }

        window.saSwitchTab(window.scheduledState.message_type || 'text');
        if (window.lucide) window.lucide.createIcons();
    };

    function setSavedEmbedPreview(imgId, iconId, url) {
        if (!url) return;
        const img = document.getElementById(imgId);
        const icon = document.getElementById(iconId);
        if (img && icon) {
            img.src = url;
            img.classList.remove('hidden');
            icon.classList.add('hidden');
            img.setAttribute('data-saved-url', url);
            img.removeAttribute('data-is-new-upload');
        }
    }

    function restoreEmbedUI(embed) {
        if (!embed) return;
        const mainInput = document.getElementById('reaction_msg_main');
        if (mainInput) mainInput.value = embed.content || mainInput.value || '';
        const title = document.getElementById('embed_title_text');
        if (title) title.value = embed.title || '';
        const desc = document.getElementById('embed_desc_text');
        if (desc) desc.value = embed.description || '';
        const fieldName = document.getElementById('embed_field_name');
        const fieldValue = document.getElementById('embed_field_value');
        if (embed.fields && embed.fields.length > 0) {
            if (fieldName) fieldName.value = embed.fields[0].name || '';
            if (fieldValue) fieldValue.value = embed.fields[0].value || '';
        }

        if (embed.author) {
            const headerText = document.getElementById('embed_header_text');
            if (headerText) headerText.value = embed.author.name || '';
            setSavedEmbedPreview('header_img_preview', 'header_img_icon', embed.author.icon_url);
        }
        if (embed.footer) {
            const footerText = document.getElementById('embed_footer_text');
            if (footerText) footerText.value = embed.footer.text || '';
            setSavedEmbedPreview('footer_img_preview', 'footer_img_icon', embed.footer.icon_url);
        }
        setSavedEmbedPreview('thumb_img_preview', 'thumb_img_icon', embed.thumbnail);
        setSavedEmbedPreview('main_img_preview', 'main_img_icon', embed.image);

        if (embed.color) {
            const dot = document.querySelector(`#color_picker_list .color-dot[data-color="${embed.color}"]`);
            if (dot) window.setEmbedThemeColor(dot, embed.color);
        }
    }

    async function loadSavedConfig() {
        if (!guildId) return;
        try {
            const resp = await fetch(`/api/config/scheduled-announcement/${guildId}`);
            const data = await resp.json();
            if (data.success && data.config) {
                const cfg = data.config;
                if (cfg.scheduled_time) {
                    const parsed = new Date(cfg.scheduled_time);
                    if (!isNaN(parsed.getTime())) {
                        window.scheduledState.scheduled_datetime = parsed;
                    }
                }
                window.scheduledState.channel = cfg.channel_id || null;
                window.scheduledState.channel_name = cfg.channel_name || null;
                window.scheduledState.message_type = cfg.message_type || 'text';

                if (cfg.message_type === 'card' && cfg.message && cfg.message.card) {
                    window.scheduledState.card = { ...window.scheduledState.card, ...cfg.message.card };
                } else if (cfg.message_type === 'embed' && cfg.message && cfg.message.embed) {
                    window.scheduledState.embed = { ...window.scheduledState.embed, ...cfg.message.embed };
                } else if (cfg.message && cfg.message.content !== undefined) {
                    window.scheduledState.text = cfg.message.content;
                }

                updateDateTimeDisplay();

                if (window.scheduledState.channel_name) {
                    const label = document.getElementById('sa_current_channel');
                    if (label) {
                        label.innerHTML = `<i data-lucide="hash" class="w-4 h-4"></i> ${window.scheduledState.channel_name}`;
                        label.classList.remove('text-gray-400');
                    }
                }

                const textInput = document.getElementById('sa_text_input');
                if (textInput) textInput.value = window.scheduledState.text || '';
                window.updateSaText(window.scheduledState.text || '');

                const fontLabel = document.getElementById('sa_current_font');
                if (fontLabel) fontLabel.innerText = window.scheduledState.card.font || 'Inter';
                const titleInput = document.querySelector('#sa_tab_content_card input[placeholder*="just joined"]');
                if (titleInput) titleInput.value = window.scheduledState.card.title || '';
                const subtitleInput = document.querySelector('#sa_tab_content_card input[placeholder*="Member #"]');
                if (subtitleInput) subtitleInput.value = window.scheduledState.card.subtitle || '';
                const bgLabel = document.getElementById('sa_card_bg_label');
                if (bgLabel) bgLabel.innerText = window.scheduledState.card.bgImage ? (window.scheduledState.card.bgImage.split('/').pop() || 'Image selected') : 'No image selected';
                applyCardStyles();

                if (cfg.message_type === 'embed' && cfg.message && cfg.message.embed) {
                    restoreEmbedUI({
                        ...cfg.message.embed,
                        content: cfg.message.embed.content || cfg.message.content || ''
                    });
                }

                window.saSwitchTab(window.scheduledState.message_type || 'text');
                if (window.lucide) window.lucide.createIcons();
            }
        } catch (e) {
            console.error('Failed to load scheduled announcement config', e);
        }
    }

    window.saSwitchTab = function(tab) {
        window.scheduledState.message_type = tab;
        ['text','card','embed'].forEach(t => {
            const btn = document.getElementById(`sa_tab_${t}`);
            const panel = document.getElementById(`sa_tab_content_${t}`);
            if (btn) btn.classList.toggle('active', t === tab);
            if (panel) panel.classList.toggle('hidden', t !== tab);
        });
        if (window.lucide) window.lucide.createIcons();
    };

    window.insertSaCmd = function(token) {
        const input = document.getElementById('sa_text_input');
        if (!input) return;
        const start = input.selectionStart || 0;
        const end = input.selectionEnd || 0;
        input.value = input.value.slice(0, start) + token + input.value.slice(end);
        input.focus();
        input.selectionStart = input.selectionEnd = start + token.length;
        updateSaText(input.value);
    };

    window.updateSaText = function(value) {
        window.scheduledState.text = value;
        const count = document.getElementById('sa_char_count');
        if (count) count.innerText = `${value.length} / 2000`;
    };

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

    const defaultCardState = {
        font: 'Inter',
        textColor: '#ffffff',
        bgColor: '#0b0f17',
        bgImage: '',
        opacity: 50,
        title: '{user} just joined the server',
        subtitle: 'Member # {membercount}'
    };

    let pendingCardBgFile = null;
    let pendingCardBgObjectUrl = null;

    function applyCardStyles() {
        const card = window.scheduledState.card || defaultCardState;
        const wrap = document.getElementById('sa_card_preview_wrap');
        const overlay = document.getElementById('sa_card_overlay');
        const title = document.getElementById('sa_card_title_text');
        const subtitle = document.getElementById('sa_card_subtitle_text');
        if (!wrap || !overlay || !title || !subtitle) return;
        wrap.style.fontFamily = card.font || 'Inter';
        title.style.color = card.textColor || '#ffffff';
        subtitle.style.color = card.textColor || '#ffffff';
        overlay.style.backgroundColor = `rgba(0,0,0,${1 - (Number(card.opacity || 50) / 100)})`;
        if (card.bgImage) {
            wrap.style.backgroundImage = `url('${card.bgImage}')`;
        } else {
            wrap.style.backgroundImage = 'none';
            wrap.style.backgroundColor = card.bgColor || '#0b0f17';
        }
        title.textContent = renderPlaceholders(card.title || defaultCardState.title);
        subtitle.textContent = renderPlaceholders(card.subtitle || defaultCardState.subtitle);
        const opacityVal = document.getElementById('sa_opacity_val');
        if (opacityVal) opacityVal.innerText = `${card.opacity || 50}%`;
    }
    window.applyCardStyles = applyCardStyles;

    window.setSaCardFont = function(font) {
        window.scheduledState.card.font = font;
        const label = document.getElementById('sa_current_font');
        if (label) label.innerText = font;
        document.getElementById('sa_font_dropdown').classList.add('hidden');
        applyCardStyles();
    };

    window.setSaCardColor = function(key, color) {
        window.scheduledState.card[key] = color;
        applyCardStyles();
    };

    window.updateSaCardValue = function(key, value) {
        window.scheduledState.card[key] = key === 'opacity' ? Number(value) : value;
        applyCardStyles();
    };

    window.toggleSaCardDropdown = function(id) {
        document.getElementById(id).classList.toggle('hidden');
    };

    function setSaCardBgLabel(text) {
        const label = document.getElementById('sa_card_bg_label');
        if (label) label.innerText = text || 'No image selected';
    }

    async function uploadCardImage(file) {
        const form = new FormData();
        form.append('file', file);
        const resp = await fetch('/api/upload/image', { method: 'POST', body: form });
        const data = await resp.json();
        if (data && data.success && data.url) {
            window.scheduledState.card.bgImage = data.url;
            applyCardStyles();
        }
    }

    function handleCardBgFile(file) {
        if (!file) return;
        pendingCardBgFile = file;
        if (pendingCardBgObjectUrl) URL.revokeObjectURL(pendingCardBgObjectUrl);
        pendingCardBgObjectUrl = URL.createObjectURL(file);
        window.scheduledState.card.bgImage = pendingCardBgObjectUrl;
        applyCardStyles();
        setSaCardBgLabel(file.name);
        uploadCardImage(file).catch(() => {});
    }

    window.setEmbedThemeColor = function(el, color) {
        const dots = document.querySelectorAll('#color_picker_list .color-dot');
        dots.forEach(dot => dot.classList.remove('active'));
        if (el) el.classList.add('active');
        const frame = document.getElementById('embed_preview_frame');
        if (frame) frame.style.borderLeftColor = color;
        window.scheduledState.embed.color = color;
    };

    window.previewEmbedImage = function(input, imgId, iconId) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.getElementById(imgId);
                const icon = document.getElementById(iconId);
                if (img && icon) {
                    img.src = e.target.result;
                    img.classList.remove('hidden');
                    icon.classList.add('hidden');
                    img.setAttribute('data-is-new-upload', 'true');
                }
            };
            reader.readAsDataURL(input.files[0]);
        }
    };

    const bgButton = document.getElementById('sa_card_bg_button');
    const bgInput = document.getElementById('sa_card_bg_input');
    if (bgButton && bgInput) {
        bgButton.addEventListener('click', () => bgInput.click());
        bgInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            handleCardBgFile(file);
        });
    }

    updateDateTimeDisplay();
    loadChannels();
    const saveBtn = document.getElementById('saSaveBtn');
    if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.removeAttribute('disabled');
    }
    loadSavedConfig();
    setInterval(updateCountdown, 1000);
    updateSaText(window.scheduledState.text || '');
    applyCardStyles();
    window.saSwitchTab(window.scheduledState.message_type || 'text');
    if (window.lucide) window.lucide.createIcons();
};
