window.REACTION_MESSAGE_HTML = `
<style>
    .embed-input {
        border: 1px solid #3f4147;
        border-radius: 4px;
        padding: 4px 8px;
        transition: border-color 0.2s;
    }
    .embed-input:focus {
        border-color: #5865f2;
    }
    .color-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        cursor: pointer;
        border: 2px solid transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }
    .color-dot.active {
        border-color: white;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
    }
    .color-dot.active::after {
        content: '';
        width: 6px;
        height: 10px;
        border: solid white;
        border-width: 0 2px 2px 0;
        transform: rotate(45deg);
        margin-bottom: 2px;
    }
</style>

<div class="config-content space-y-6">
    <div>
        <h2 class="text-white font-bold text-lg">Embed message builder</h2>
        <p class="text-gray-400 text-xs mt-1">Create your embed with optional message the way you want it</p>
    </div>

    <!-- Main Message Input -->
    <div class="space-y-2">
        <div class="bg-[#111214] border border-[#2b2d31] rounded-lg p-2">
            <textarea id="reaction_msg_main" 
                class="w-full bg-transparent border-none outline-none text-sm text-white resize-none placeholder-gray-600 h-10"
                placeholder="React to this message to get your roles!">React to this message to get your roles!</textarea>
        </div>
    </div>

    <!-- Color Picker -->
    <div class="flex items-center gap-3">
        <div class="flex flex-wrap gap-2" id="color_picker_list">
            <!-- 10 bright colors -->
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

    <!-- Embed Preview Frame -->
    <div class="relative bg-[#1e1f22] rounded-md border-l-4 border-white p-4 max-w-2xl" id="embed_preview_frame">
        <div class="flex flex-col gap-3">
            <!-- Header Section -->
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31]" 
                     onclick="document.getElementById('header_img_input').click()">
                    <img id="header_img_preview" src="" class="hidden w-full h-full object-cover">
                    <i data-lucide="image" class="w-5 h-5 text-gray-500" id="header_img_icon"></i>
                </div>
                <input type="text" class="bg-transparent outline-none text-sm text-gray-400 w-full embed-input" placeholder="Header" id="embed_header_text">
                <input type="file" id="header_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'header_img_preview', 'header_img_icon')">
            </div>

            <!-- Content Row (Title/Desc + Thumbnail) -->
            <div class="flex justify-between gap-4">
                <div class="flex-1 space-y-2">
                    <input type="text" class="bg-transparent outline-none text-base font-bold text-white w-full embed-input" placeholder="Title" id="embed_title_text">
                    <textarea class="w-full bg-transparent outline-none text-sm text-gray-300 resize-none h-10 embed-input" 
                              placeholder="React to this message to get your roles!" id="embed_desc_text">React to this message to get your roles!</textarea>
                    
                    <div class="space-y-1">
                        <input type="text" class="bg-transparent outline-none text-xs font-bold text-white w-full embed-input" placeholder="Field name" id="embed_field_name">
                        <input type="text" class="bg-transparent outline-none text-xs text-gray-300 w-full embed-input" placeholder="Field value" id="embed_field_value">
                    </div>
                </div>

                <!-- Thumbnail -->
                <div class="w-24 h-24 rounded-lg border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31] shrink-0"
                     onclick="document.getElementById('thumb_img_input').click()">
                    <img id="thumb_img_preview" src="" class="hidden w-full h-full object-cover">
                    <i data-lucide="image" class="w-12 h-12 text-gray-500" id="thumb_img_icon"></i>
                    <input type="file" id="thumb_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'thumb_img_preview', 'thumb_img_icon')">
                </div>
            </div>

            <!-- Big Main Image -->
            <div class="w-full h-28 rounded-lg border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31] mt-2"
                 onclick="document.getElementById('main_img_input').click()">
                <img id="main_img_preview" src="" class="hidden w-full h-full object-cover">
                <i data-lucide="image" class="w-10 h-10 text-gray-500" id="main_img_icon"></i>
                <input type="file" id="main_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'main_img_preview', 'main_img_icon')">
            </div>

            <!-- Footer Section -->
            <div class="flex items-center gap-2 mt-2 opacity-60">
                <div class="w-6 h-6 rounded-full border border-dashed border-gray-600 flex items-center justify-center cursor-pointer overflow-hidden bg-[#2b2d31]"
                     onclick="document.getElementById('footer_img_input').click()">
                    <img id="footer_img_preview" src="" class="hidden w-full h-full object-cover">
                    <i data-lucide="image" class="w-4 h-4 text-gray-500" id="footer_img_icon"></i>
                </div>
                <input type="text" class="bg-transparent outline-none text-xs text-gray-400 w-full embed-input" placeholder="Footer" id="embed_footer_text">
                <input type="file" id="footer_img_input" class="hidden" accept="image/*" onchange="previewEmbedImage(this, 'footer_img_preview', 'footer_img_icon')">
            </div>
        </div>
    </div>
</div>
`;

window.initializeReactionMessage = function () {
    console.log("[SYSTEM] Reaction Message Section Initialized");
    if (window.lucide) window.lucide.createIcons();

    // Sync main textareas if desired (optional behavior)
    const mainInput = document.getElementById('reaction_msg_main');
    const embedDesc = document.getElementById('embed_desc_text');

    if (mainInput && embedDesc) {
        mainInput.addEventListener('input', (e) => {
            embedDesc.value = e.target.value;
        });
        embedDesc.addEventListener('input', (e) => {
            mainInput.value = e.target.value;
        });
    }

    // Restore saved data
    if (window.savedMsgData) {
        const d = window.savedMsgData;

        if (mainInput) mainInput.value = d.content || '';

        if (document.getElementById('embed_title_text')) document.getElementById('embed_title_text').value = d.embed.title || '';
        if (embedDesc) embedDesc.value = d.embed.description || '';

        // Fields (Restore first field only for this UI)
        if (d.embed.fields && d.embed.fields.length > 0) {
            if (document.getElementById('embed_field_name')) document.getElementById('embed_field_name').value = d.embed.fields[0].name || '';
            if (document.getElementById('embed_field_value')) document.getElementById('embed_field_value').value = d.embed.fields[0].value || '';
        }

        // Color
        if (d.embed.color) {
            const dot = document.querySelector(`.color-dot[data-color="${d.embed.color}"]`);
            if (dot) setEmbedThemeColor(dot, d.embed.color);
        }

        // Images Helper
        const setPreview = (imgId, iconId, url) => {
            if (url) {
                const img = document.getElementById(imgId);
                const icon = document.getElementById(iconId);
                if (img && icon) {
                    img.src = url;
                    img.classList.remove('hidden');
                    icon.classList.add('hidden');
                    // Store the saved URL for later use
                    img.setAttribute('data-saved-url', url);
                    img.removeAttribute('data-is-new-upload');
                }
            }
        };

        // Restore Images & Text
        if (d.embed.author) {
            if (document.getElementById('embed_header_text')) document.getElementById('embed_header_text').value = d.embed.author.name || '';
            setPreview('header_img_preview', 'header_img_icon', d.embed.author.icon_url);
        }

        setPreview('thumb_img_preview', 'thumb_img_icon', d.embed.thumbnail);
        setPreview('main_img_preview', 'main_img_icon', d.embed.image);

        if (d.embed.footer) {
            if (document.getElementById('embed_footer_text')) document.getElementById('embed_footer_text').value = d.embed.footer.text || '';
            setPreview('footer_img_preview', 'footer_img_icon', d.embed.footer.icon_url);
        }
    }
};

window.setEmbedThemeColor = function (el, color) {
    // Update dots UI
    const dots = document.querySelectorAll('#color_picker_list .color-dot');
    dots.forEach(dot => dot.classList.remove('active'));
    el.classList.add('active');

    // Update embed frame border
    const frame = document.getElementById('embed_preview_frame');
    if (frame) {
        frame.style.borderLeftColor = color;
    }
};

window.previewEmbedImage = function (input, imgId, iconId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.getElementById(imgId);
            const icon = document.getElementById(iconId);
            if (img && icon) {
                img.src = e.target.result;
                img.classList.remove('hidden');
                icon.classList.add('hidden');
                // Store that this is a new upload (not a saved URL)
                img.setAttribute('data-is-new-upload', 'true');
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
};
