# GUI Code Snippets

Reusable GUI snippets for all 22 requested elements, grouped by category for faster build and reuse.

## Table of Contents

| GUI Element | Short Description |
| --- | --- |
| Point 1 - Dashboard Feature Card With Enable Button | Dashboard feature card with icon and enable button |
| Point 2 - Modern Toggle (Green and Blue) | Reusable animated toggle styles |
| Point 3 - Emoji Selector Widget | Emoji trigger and popup picker flow |
| Point 4 - GUI Page Template Block | Base page shell and header pattern |
| Point 5 - Feature Frame With Header + Toggle | Reusable card frame for sections |
| Point 6 - Feature Frame + Dropdown Logic | Section frame with dropdown behavior |
| Point 7 - Changes Detected Save Bar + Logic + DB Signal | Save/cancel bar and persistence flow |
| Point 8 - Welcome Message Channel Dropdown + Backend | Channel selector and API connection |
| Point 9 - Text/Embed Tabs | Tab switch UI and state logic |
| Point 10 - Message Editor Command Badge Frame | Command tags that insert placeholders |
| Point 11 - Textarea + Character Counter | Message area with limit indicator |
| Point 12 - Font Dropdown (10-15 Fonts) | Font picker dropdown used in cards |
| Point 13 - 10 Color Selector | Color dots with active state |
| Point 14 - Live Welcome Card Preview | Live card preview with placeholder render |
| Point 15 - Role Selector + Create Role + Backend | Role dropdown + role creation flow |
| Point 16 - Selected Role Chips | Selected-role badges with remove button |
| Point 17 - Commands Permission Frame | Command card with toggle and role picker |
| Point 18 - Full Embed Message Builder | Full embed UI with image pickers |
| Point 19 - Time Selector | Time picker component |
| Point 20 - Date Selector Calendar | Calendar selector component |
| Point 21 - Sliders (XP + Overlay Opacity) | Advanced and simple slider styles |
| Point 22 - Modern Checkbox | Modern checkbox row style |

## Dashboard Cards & Frames

## Point 1 - Dashboard Feature Card With Enable Button
Dashboard card with icon, hover lift effect, and enable button.

```html
<style>
  .card {
    background-color: #1e1f22;
    transition: transform 0.2s;
  }

  .card:hover {
    transform: translateY(-2px);
  }
</style>

<div class="card rounded-xl p-6 flex flex-col border border-white/5" data-feature-title="Welcome & Goodbye">
  <div class="flex justify-between items-start mb-4">
    <div class="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center text-blue-500">
      <i data-lucide="hand" class="w-6 h-6"></i>
    </div>
  </div>
  <h3 class="text-white font-bold mb-2">Welcome & Goodbye</h3>
  <p class="text-gray-400 text-xs leading-relaxed mb-6 flex-1">
    Automatically send messages and give roles to your new members and send a message when a
    members lea...
  </p>
  <button class="w-full flex items-center justify-center space-x-2 py-2 rounded-md bg-white/5 text-white text-xs font-bold border border-white/10 hover:bg-white/10">
    <i data-lucide="plus" class="w-4 h-4"></i>
    <span>Enable</span>
  </button>
</div>
```

## Point 2 - Modern Toggle (Green and Blue)
Animated toggle style with both green and blue active variants.

```html
<style>
  .switch {
    position: relative;
    display: inline-block;
    width: 46px;
    height: 26px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #4e5058;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 999px;
    box-shadow: inset 0 0 0 1px #3f4147;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
  }

  .switch.green input:checked + .slider {
    background-color: #22c55e;
  }

  .switch.blue input:checked + .slider {
    background-color: #5865f2;
  }

  .switch input:checked + .slider:before {
    transform: translateX(20px);
  }
</style>

<div style="display:flex; gap:14px; align-items:center;">
  <label class="switch green">
    <input type="checkbox" checked>
    <span class="slider"></span>
  </label>

  <label class="switch blue">
    <input type="checkbox" checked>
    <span class="slider"></span>
  </label>
</div>
```

## Point 3 - Emoji Selector Widget
Emoji trigger button with popup picker behavior.

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/emoji-picker-element@1/index.js"></script>

<style>
  .emoji-trigger {
    font-size: 24px;
    cursor: pointer;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    background: #2b2d31;
    flex-shrink: 0;
    border: 1px solid #3f4147;
  }

  .emoji-trigger:hover {
    background: #35373c;
  }

  #emoji_picker_popup {
    position: fixed;
    z-index: 1000;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    display: none;
    max-width: 360px;
    max-height: 380px;
    overflow: hidden;
    border-radius: 12px;
  }

  #emoji_picker_popup emoji-picker {
    max-height: 380px;
    height: 380px;
  }
</style>

<div id="hiEmojiBtn" class="emoji-trigger" title="Pick emoji">&#128075;</div>
<div id="emoji_picker_popup">
  <emoji-picker class="dark"></emoji-picker>
</div>

<script>
  const hiEmojiBtn = document.getElementById('hiEmojiBtn');

  function openEmojiPicker(event) {
    event.stopPropagation();
    const picker = document.getElementById('emoji_picker_popup');
    const rect = hiEmojiBtn.getBoundingClientRect();
    picker.style.display = 'block';

    const pickerHeight = 380;
    const pickerWidth = 360;
    const viewportH = window.innerHeight;
    const viewportW = window.innerWidth;

    let top = rect.bottom + 10;
    if (top + pickerHeight > viewportH - 10) {
      top = rect.top - pickerHeight - 10;
    }
    if (top < 10) top = 10;

    let left = rect.left;
    if (left + pickerWidth > viewportW - 10) {
      left = viewportW - pickerWidth - 10;
    }
    if (left < 10) left = 10;

    picker.style.top = top + 'px';
    picker.style.left = left + 'px';
  }

  document.addEventListener('click', (e) => {
    const picker = document.getElementById('emoji_picker_popup');
    if (picker && !picker.contains(e.target) && e.target !== hiEmojiBtn) {
      picker.style.display = 'none';
    }
  });

  const pickerElement = document.querySelector('emoji-picker');
  if (pickerElement) {
    pickerElement.addEventListener('emoji-click', event => {
      const emoji = event.detail.unicode;
      hiEmojiBtn.textContent = emoji;
      document.getElementById('emoji_picker_popup').style.display = 'none';
    });
  }

  hiEmojiBtn.addEventListener('click', openEmojiPicker);
</script>
```

## Point 4 - GUI Page Template Block
Base GUI page shell and shared styling tokens.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leaderboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script type="module" src="https://cdn.jsdelivr.net/npm/emoji-picker-element@1/index.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&display=swap');

        :root {
            --bg-color: #1a1b1e;
            --card-bg: #2a2c31;
            --card-hover: #313339;
            --text-main: #ffffff;
            --text-sub: #b5bac1;
            --accent-blue: #5865f2;
            --toggle-off: #4e5058;
            --scrollbar-thumb: #111214;
            --editor-bg: #1e1f22;
            --preview-bg: #000000;
            --border: #3f4147;
        }

        body {
            font-family: 'Golos Text', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px 24px;
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            overflow-y: overlay;
            font-size: 15px;
        }

        ::-webkit-scrollbar {
            width: 12px;
        }

        ::-webkit-scrollbar-track {
            background-color: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background-color: var(--scrollbar-thumb);
            border: 3px solid var(--bg-color);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: #6d6f78;
        }

        .container {
            width: 100%;
            max-width: 900px;
            padding-bottom: 100px;
            overflow: visible;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding: 0;
        }

        .header-title-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header h1 {
            font-size: 30px;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .close-btn {
            color: var(--text-sub);
            cursor: pointer;
            transition: 0.2s;
        }

        .close-btn:hover {
            color: #fff;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div class="header-title-group">
                <i data-lucide="chevron-left" class="close-btn" onclick="window.parent.closeComponent()"></i>
                <div class="w-2 h-2 rounded-full bg-accent-blue"></div>
                <h1>Leaderboard</h1>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>

</html>
```

## Point 5 - Feature Frame With Header + Toggle
Reusable frame used for join/leave/role/private-message feature cards.

```html
<style>
  .feature-card-container {
    background-color: #2a2c31;
    border-radius: 12px;
    overflow: hidden;
    transition: background-color 0.3s;
  }

  .feature-card-container.allow-overflow {
    overflow: visible;
  }

  .feature-card-header {
    padding: 22px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }

  .feature-card-header:hover {
    background-color: #313339;
  }

  .feature-title {
    font-size: 17px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ffffff;
  }

  .switch {
    position: relative;
    display: inline-block;
    width: 44px;
    height: 24px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #4e5058;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 20px;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
  }

  input:checked + .slider {
    background-color: #5865f2;
  }

  input:checked + .slider:before {
    transform: translateX(20px);
  }
</style>

<div class="feature-card-container">
  <div class="feature-card-header" onclick="toggleSection(this)">
    <div class="feature-title">Send a message when a user joins the server</div>
    <label class="switch">
      <input type="checkbox" id="toggle_join" onchange="handleToggle(this)">
      <span class="slider"></span>
    </label>
  </div>
  <div id="join-server-container"></div>
</div>
```

## Point 6 - Feature Frame + Dropdown Logic
Feature frame plus dropdown open/close logic.

```html
<div class="expandable-section active" id="section_join">
  <div class="config-content">
    <div>
      <label class="config-label">Welcome Message Channel <span class="text-red-500">*</span></label>
      <div class="relative">
        <div class="dropdown-box" onclick="toggleJoinDropdown('join_channel_dropdown')">
          <span id="join_current_channel" class="flex items-center gap-2 text-gray-400">
            <i data-lucide="hash" class="w-4 h-4"></i> Select a channel
          </span>
          <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
        </div>
        <div id="join_channel_dropdown" class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto">
          <div class="p-2 text-sm text-gray-500">Loading channels...</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

```js
window.toggleJoinDropdown = async function(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('hidden');
  if (!el.classList.contains('hidden') && el.innerHTML.includes('Loading')) {
    await loadDiscordData();
  }
};
```

## Point 7 - Changes Detected Save Bar + Logic + DB Signal
Save/cancel bar UI, change-detection logic, and backend/database signal flow.

```html
<style>
  .save-bar {
    position: fixed;
    bottom: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 60px);
    max-width: 800px;
    background-color: #111214;
    padding: 15px 25px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: bottom 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 -10px 25px rgba(0, 0, 0, 0.5);
    z-index: 1000;
  }

  .save-bar.active {
    bottom: 25px;
  }

  .save-info {
    color: white;
    font-size: 14px;
    font-weight: 500;
  }

  .save-actions {
    display: flex;
    gap: 12px;
  }

  .btn {
    padding: 8px 24px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
    border: none;
  }

  .btn-cancel {
    background-color: #4f545c;
    color: white;
  }

  .btn-cancel:hover {
    background-color: #5d6269;
  }

  .btn-save {
    background-color: #5865f2;
    color: white;
  }

  .btn-save:hover {
    background-color: #4752c4;
  }
</style>

<div id="saveBar" class="save-bar">
  <div class="save-info">Changes detected! Please save or cancel.</div>
  <div class="save-actions">
    <button class="btn btn-cancel" onclick="cancelChanges()">Cancel</button>
    <button class="btn btn-save" onclick="saveChanges()">Save</button>
  </div>
</div>
```

```js
function checkForChanges() {
  const isChanged = JSON.stringify(state) !== JSON.stringify(initialState);
  const bar = document.getElementById('saveBar');
  if (isChanged) bar.classList.add('active');
  else bar.classList.remove('active');
}

function cancelChanges() {
  state = JSON.parse(JSON.stringify(initialState));
  location.reload();
}

async function saveChanges() {
  const urlParams = new URLSearchParams(window.location.search);
  const guildId = urlParams.get('guild_id');
  if (!guildId) return;

  try {
    const jPromise = fetch(`/api/config/join/${guildId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.join)
    });

    const lPromise = fetch(`/api/config/leave/${guildId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.leave)
    });

    const dPromise = fetch(`/api/config/dm/${guildId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.dm)
    });

    const rPromise = fetch(`/api/config/role/${guildId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state.role)
    });

    const results = await Promise.all([jPromise, lPromise, dPromise, rPromise]);

    if (results.every(r => r.ok)) {
      initialState = JSON.parse(JSON.stringify(state));
      checkForChanges();
      alert("Settings saved successfully!");
    } else {
      alert("One or more settings failed to save.");
    }
  } catch (e) {
    console.error("Save failed", e);
    alert("An error occurred while saving.");
  }
}
```

```python
@app.post("/api/config/join/{guild_id}")
async def save_join_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "join", data)
    return {"success": True}

@app.post("/api/config/leave/{guild_id}")
async def save_leave_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "leave", data)
    return {"success": True}

@app.post("/api/config/dm/{guild_id}")
async def save_dm_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "dm", data)
    return {"success": True}

@app.post("/api/config/role/{guild_id}")
async def save_role_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "role", data)
    return {"success": True}

class Database:
    def get_config(self, server_id: str, feature: str) -> Optional[Dict]:
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f:
                    self.data = json.load(f)
        except Exception:
            pass
        return self.data.get("servers", {}).get(server_id, {}).get(feature)

    def save_config(self, server_id: str, feature: str, config: Dict):
        if server_id not in self.data["servers"]:
            self.data["servers"][server_id] = {}
        if feature in ("join", "dm") and isinstance(config, dict):
            card_enabled = bool(config.get("card", {}).get("enabled"))
            msg_type = config.get("type") or "text"
            if card_enabled:
                config["mode"] = "card"
            elif msg_type == "embed":
                config["mode"] = "embed"
            else:
                config["mode"] = "text"
        self.data["servers"][server_id][feature] = config
        self.save_db()
```

## Point 8 - Welcome Message Channel Dropdown + Backend Connection
Channel dropdown UI and backend endpoint wiring for Discord channel fetch.

```html
<label class="config-label">Welcome Message Channel <span class="text-red-500">*</span></label>
<div class="relative">
  <div class="dropdown-box" onclick="toggleJoinDropdown('join_channel_dropdown')">
    <span id="join_current_channel" class="flex items-center gap-2 text-gray-400">
      <i data-lucide="hash" class="w-4 h-4"></i> Select a channel
    </span>
    <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
  </div>
  <div id="join_channel_dropdown" class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto">
    <div class="p-2 text-sm text-gray-500">Loading channels...</div>
  </div>
</div>
```

```python
@app.get("/api/guilds/{guild_id}/channels")
async def get_channels(guild_id: str):
    if active_context["guild_id"] == guild_id and active_context["data"]:
        return {"success": True, "channels": active_context["data"]["channels"]}
    channels = await db_manager.get_channels(guild_id)
    return {"success": True, "channels": channels}
```

## Point 9 - Tabs (Text Message and Embed Message)
Tabs that switch between text editor and embed editor states.

```html
<div class="tabs-container">
  <div id="join_tab_text" class="tab active" onclick="setJoinMessageType('text')">Text message</div>
  <div id="join_tab_embed" class="tab" onclick="setJoinMessageType('embed')">Embed message</div>
</div>

<div id="join_text_editor"></div>
<div id="join_embed_editor" class="hidden"></div>

<script>
window.setJoinMessageType = function(type, preserveCard = false) {
  const cardOn = !!state.join?.card?.enabled || state.join?.mode === 'card';
  if (!preserveCard && !cardOn) {
    setJoinMode(type === 'embed' ? 'embed' : 'text');
  } else {
    state.join.type = type;
  }

  const textEd = document.getElementById('join_text_editor');
  const embedEd = document.getElementById('join_embed_editor');
  const tabT = document.getElementById('join_tab_text');
  const tabE = document.getElementById('join_tab_embed');

  if (type === 'text') {
    if (textEd) textEd.classList.remove('hidden');
    if (embedEd) embedEd.classList.add('hidden');
    if (tabT) tabT.classList.add('active');
    if (tabE) tabE.classList.remove('active');
  } else {
    if (textEd) textEd.classList.add('hidden');
    if (embedEd) embedEd.classList.remove('hidden');
    if (tabT) tabT.classList.remove('active');
    if (tabE) tabE.classList.add('active');
  }
  checkForChanges();
};
</script>
```

## Point 10 - Message Editor Command Badge Frame
Message editor command badge frame with click-to-insert tokens.

```html
<div class="config-label">Message Editor</div>

<div class="flex flex-wrap gap-2 mb-3 p-3 bg-[#1e1f22] border border-[#333] rounded-lg">
  <span class="command-badge" onclick="insertJoinCmd('{user}')">{user}</span>
  <span class="command-badge" onclick="insertJoinCmd('{userid}')">{userid}</span>
  <span class="command-badge" onclick="insertJoinCmd('{usertag}')">{usertag}</span>
  <span class="command-badge" onclick="insertJoinCmd('{mention}')">{mention}</span>
  <span class="command-badge" onclick="insertJoinCmd('{avatar}')">{avatar}</span>
  <span class="command-badge" onclick="insertJoinCmd('{server}')">{server}</span>
  <span class="command-badge" onclick="insertJoinCmd('{serverid}')">{serverid}</span>
  <span class="command-badge" onclick="insertJoinCmd('{membercount}')">{membercount}</span>
  <span class="command-badge" onclick="insertJoinCmd('{members}')">{members}</span>
  <span class="command-badge" onclick="insertJoinCmd('{date}')">{date}</span>
  <span class="command-badge" onclick="insertJoinCmd('{time}')">{time}</span>
  <span class="command-badge" onclick="insertJoinCmd('{role}')">{role}</span>
</div>

<script>
window.insertJoinCmd = function(cmd) {
  const textarea = document.getElementById('join_msg_input');
  if (!textarea) return;
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const text = textarea.value;
  textarea.value = text.substring(0, start) + cmd + text.substring(end);
  textarea.focus();
  textarea.selectionStart = textarea.selectionEnd = start + cmd.length;
  updateJoinValue('text', textarea.value);
};
</script>
```

## Point 11 - Text Box / Message + Character Counter
Text area with live character counter and red limit warning over 2000.

```html
<style>
  .char-counter.limit-red {
    color: #ed4245;
    font-weight: 700;
  }
</style>

<div class="text-editor-container">
  <textarea id="join_msg_input" class="text-editor" oninput="updateJoinValue('text', this.value)"></textarea>
  <span id="join_char_count" class="char-counter">0 / 2000</span>
</div>

<script>
window.updateJoinValue = function(key, val) {
  ensureJoinState();
  const safeVal = (val == null) ? '' : val;
  state.join[key] = safeVal;
  if (key === 'text') {
    const charCount = document.getElementById('join_char_count');
    if (charCount) {
      charCount.innerText = `${safeVal.length} / 2000`;
      if (safeVal.length > 2000) charCount.classList.add('limit-red');
      else charCount.classList.remove('limit-red');
    }
  }
  checkForChanges();
};
</script>
```

## Point 12 - Font Dropdown (10-15 Fonts)
Font picker dropdown with 10-15 font options and selection behavior.

```html
<div>
  <label class="config-label">Font</label>
  <div class="relative">
    <div class="dropdown-box" onclick="toggleJoinDropdown('join_font_dropdown')">
      <span id="join_current_font">Inter</span>
      <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
    </div>
    <div id="join_font_dropdown" class="hidden absolute top-12 left-0 w-full bg-[#111214] border border-[#2b2d31] rounded-md shadow-2xl z-20 p-2 max-h-48 overflow-y-auto custom-scrollbar">
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Inter]" onclick="setCardFont('join', 'Inter')">Inter</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Roboto]" onclick="setCardFont('join', 'Roboto')">Roboto</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Open Sans']" onclick="setCardFont('join', 'Open Sans')">Open Sans</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Source Sans 3']" onclick="setCardFont('join', 'Source Sans 3')">Source Sans 3</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Lato]" onclick="setCardFont('join', 'Lato')">Lato</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Montserrat]" onclick="setCardFont('join', 'Montserrat')">Montserrat</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Poppins]" onclick="setCardFont('join', 'Poppins')">Poppins</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Raleway]" onclick="setCardFont('join', 'Raleway')">Raleway</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Nunito]" onclick="setCardFont('join', 'Nunito')">Nunito</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Ubuntu]" onclick="setCardFont('join', 'Ubuntu')">Ubuntu</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['DM Sans']" onclick="setCardFont('join', 'DM Sans')">DM Sans</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Merriweather]" onclick="setCardFont('join', 'Merriweather')">Merriweather</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Playfair Display']" onclick="setCardFont('join', 'Playfair Display')">Playfair Display</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-[Oswald]" onclick="setCardFont('join', 'Oswald')">Oswald</div>
      <div class="hover:bg-[#404249] p-2 rounded cursor-pointer text-sm font-['Bebas Neue']" onclick="setCardFont('join', 'Bebas Neue')">Bebas Neue</div>
    </div>
  </div>
</div>

<script>
window.setCardFont = function(feature, font) {
  if (!state[feature]) state[feature] = {};
  if (!state[feature].card) state[feature].card = { ...defaultCardState };
  state[feature].card.font = font;
  const currentFontEl = document.getElementById(`${feature}_current_font`);
  if (currentFontEl) currentFontEl.innerText = font;
  const dropdown = document.getElementById(`${feature}_font_dropdown`);
  if (dropdown) dropdown.classList.add('hidden');
  checkForChanges();
};
</script>
```

## Point 13 - 10 Color Selector
10-color selector with active state and check mark.

```html
<style>
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
```

## Point 14 - Live Welcome Card Preview
Live welcome card preview with placeholder rendering and text fitting.

```html
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

<script>
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
</script>
```

## Point 15 - Role Selector + Create Role UI + Backend API
Role selector with search/create-role flow, plus backend role endpoints.

```html
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

<script>
async function createRole() {
  const nameInput = document.getElementById('role_create_name');
  const name = (nameInput?.value || '').trim();
  if (!name || !guildId) return;
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
}
</script>
```

```python
@app.get("/api/guilds/{guild_id}/roles")
async def get_roles(guild_id: str):
    if active_context["guild_id"] == guild_id and active_context["data"]:
        return {"success": True, "roles": active_context["data"]["roles"]}
    headers = {"Authorization": f"Bot {db_manager.token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers)
        if resp.status_code == 200:
            return {"success": True, "roles": resp.json()}
    return {"success": False, "error": "Failed to fetch roles"}

@app.post("/api/roles/create")
async def create_role(payload: Dict = Body(...)):
    guild_id = payload.get("guild_id")
    name = payload.get("name")
    color = payload.get("color", "#5865f2")
    if not guild_id or not name:
        return {"success": False, "error": "guild_id and name are required"}

    try:
        color_int = int(str(color).lstrip("#"), 16)
    except:
        color_int = 0x5865F2

    headers = {"Authorization": f"Bot {db_manager.token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://discord.com/api/v10/guilds/{guild_id}/roles",
            headers=headers,
            json={"name": name, "color": color_int}
        )
        if resp.status_code in (200, 201):
            role = resp.json()
            return {
                "success": True,
                "role": {
                    "id": role.get("id"),
                    "name": role.get("name"),
                    "color": f"#{int(role.get('color') or 0):06x}"
                }
            }
        return {"success": False, "error": resp.text}
```

## Point 16 - Selected Role Chips
Selected role chip UI with color dot and remove action.

```js
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
    remove.textContent = 'x';
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
```

## Point 17 - Commands Permission Frame
Single command permission frame using role chips and add-role dropdown patterns.

```html
<style>
  .switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 26px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #3b3f46;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 999px;
    box-shadow: inset 0 0 0 1px #4b5059;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
  }

  input:checked + .slider { background-color: #22c55e; }
  input:checked + .slider:before { transform: translateX(22px); }

  .role-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    min-height: 48px;
    padding: 10px;
    border: 1px solid #3a3d44;
    border-radius: 10px;
    background: #1b1d21;
  }

  .role-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 999px;
    background: #2b2d31;
    border: 1px solid #3f4147;
    font-size: 13px;
    color: #dbdee1;
  }

  .role-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .role-remove {
    color: #ed4245;
    cursor: pointer;
    font-size: 14px;
    line-height: 1;
  }

  .dropdown-box {
    background-color: #1e1f22;
    border: 1px solid #3f4147;
    border-radius: 8px;
    padding: 10px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    width: 320px;
  }

  .dropdown-panel {
    position: absolute;
    top: 48px;
    left: 0;
    right: 0;
    background-color: #111214;
    border: 1px solid #2b2d31;
    border-radius: 8px;
    z-index: 100;
    max-height: 220px;
    overflow-y: auto;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  }

  .dropdown-item {
    padding: 10px 12px;
    font-size: 14px;
    cursor: pointer;
    color: #b5bac1;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dropdown-item:hover {
    background-color: #35373c;
    color: #fff;
  }
</style>

<div class="command-card">
  <div class="command-head">
    <div class="command-title">
      <span>/Analytics Member</span>
      <div class="info-btn" data-tooltip="Shows roles with member counts for each role.">i</div>
    </div>
    <label class="switch">
      <input id="analyticsToggle" type="checkbox">
      <span class="slider"></span>
    </label>
  </div>

  <div id="roleList" class="role-list">
    <div class="empty-state" id="emptyState">No roles added yet.</div>
  </div>

  <div class="relative">
    <div id="roleDropdownBtn" class="dropdown-box">
      <span class="text-gray-300">Add a role</span>
      <i data-lucide="chevron-down" class="w-4 h-4 text-gray-500"></i>
    </div>
    <div id="roleDropdownPanel" class="dropdown-panel hidden"></div>
  </div>
</div>

<script>
class CommandManager {
  constructor(prefix, apiPath) {
    this.prefix = prefix;
    this.apiPath = apiPath;
    this.roleList = document.getElementById(`${prefix}RoleList`) || document.getElementById('roleList');
    this.emptyState = document.getElementById(`${prefix}EmptyState`) || document.getElementById('emptyState');
    this.roleDropdownBtn = document.getElementById(`${prefix}RoleDropdownBtn`) || document.getElementById('roleDropdownBtn');
    this.roleDropdownPanel = document.getElementById(`${prefix}RoleDropdownPanel`) || document.getElementById('roleDropdownPanel');
    this.toggle = document.getElementById(`${prefix}Toggle`) || document.getElementById('analyticsToggle');
    this.selectedRoles = [];
    this.pendingRoleIds = [];
    this.init();
  }

  init() {
    this.roleDropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleDropdown();
    });

    this.roleList.addEventListener('click', (e) => {
      if (e.target.classList.contains('role-remove')) {
        const id = e.target.getAttribute('data-id');
        this.selectedRoles = this.selectedRoles.filter(r => r.id !== id);
        this.renderRoleList();
        this.saveSettings();
      }
    });

    this.toggle.addEventListener('change', () => this.saveSettings());
  }

  toggleDropdown() {
    this.roleDropdownPanel.classList.toggle('hidden');
    if (!this.roleDropdownPanel.classList.contains('hidden')) {
      this.renderRoleDropdown();
    }
  }
}
</script>
```

## Point 18 - Full Embed Message Builder
Full embed builder snippet with title/fields/footer and image upload previews.

```js
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

    <div class="space-y-2">
        <div class="bg-[#111214] border border-[#2b2d31] rounded-lg p-2">
            <textarea id="reaction_msg_main" 
                class="w-full bg-transparent border-none outline-none text-sm text-white resize-none placeholder-gray-600 h-10"
                placeholder="React to this message to get your roles!">React to this message to get your roles!</textarea>
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
`;

window.initializeReactionMessage = function () {
    if (window.lucide) window.lucide.createIcons();
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
};

window.setEmbedThemeColor = function (el, color) {
    const dots = document.querySelectorAll('#color_picker_list .color-dot');
    dots.forEach(dot => dot.classList.remove('active'));
    el.classList.add('active');

    const frame = document.getElementById('embed_preview_frame');
    if (frame) frame.style.borderLeftColor = color;
};

window.previewEmbedImage = function (input, imgId, iconId) {
    if (!(input.files && input.files[0])) return;
    const file = input.files[0];
    if (!file.type.startsWith('image/')) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const img = document.getElementById(imgId);
        const icon = document.getElementById(iconId);
        if (img && icon) {
            img.src = e.target.result;
            img.classList.remove('hidden');
            icon.classList.add('hidden');
            img.style.objectFit = 'cover';
            img.style.width = '100%';
            img.style.height = '100%';
            img.setAttribute('data-is-new-upload', 'true');
        }
    };
    reader.readAsDataURL(file);
};
```

## Point 19 - Time Selector
Time picker popup with hour/min/sec controls and apply action.

```html
<style>
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
    width: 100%;
    background: #1e1f22;
    border: 1px solid #333;
    color: #fff;
    border-radius: 4px;
    padding: 8px;
    text-align: center;
  }
</style>

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

<script>
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
</script>
```

## Point 20 - Date Selector Calendar
Date calendar popup with month navigation and disabled past dates.

```html
<style>
  .cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
  .cal-day-name { font-size: 10px; color: #555; text-align: center; padding: 4px 0; }
  .cal-cell {
    font-size: 12px;
    text-align: center;
    padding: 8px 0;
    cursor: pointer;
    border-radius: 4px;
    color: #dbdee1;
  }
  .cal-cell:hover:not(.disabled) { background: #35373c; }
  .cal-cell.active { background: #5865f2; color: #fff; }
  .cal-cell.disabled { color: #444; cursor: not-allowed; }
</style>

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

<script>
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
</script>
```

## Point 21 - Sliders (XP + Overlay Opacity)
Two slider styles: XP earning slider and a simpler overlay-opacity slider.

```html
<style>
  .slider-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .range-input {
    width: 60px;
    height: 32px;
    background-color: #1e1f22;
    border: 1px solid #6d6f78;
    border-radius: 6px;
    padding: 6px 8px;
    color: #ffffff;
    font-size: 16px;
    text-align: center;
  }

  .slider {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(to right, #4e5058 0%, #5865f2 50%, #4e5058 100%);
    outline: none;
    -webkit-appearance: none;
    appearance: none;
  }

  .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #5865f2;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .slider::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #5865f2;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .slider-value {
    font-size: 14px;
    font-weight: 600;
    color: #5865f2;
    min-width: 50px;
    text-align: right;
  }
</style>

<label class="form-label">XP Earning Rate</label>
<div class="slider-container">
  <input type="number" class="range-input" id="sliderMin" value="0.5" step="0.1" oninput="updateSliderMin()">
  <input type="range" class="slider" id="xpSlider" min="0.5" max="10" step="0.1" value="1.0" oninput="updateSliderValue()">
  <input type="number" class="range-input" id="sliderMax" value="10" step="0.1" oninput="updateSliderMax()">
  <span class="slider-value" id="sliderValue">1.0x</span>
</div>

<script>
function updateSliderValue() {
  const slider = document.getElementById('xpSlider');
  if (!slider) return;
  const value = parseFloat(slider.value);
  const sliderValue = document.getElementById('sliderValue');
  if (sliderValue) sliderValue.textContent = value.toFixed(1) + 'x';
  const sliderMin = document.getElementById('sliderMin');
  const sliderMax = document.getElementById('sliderMax');
  if (sliderMin) sliderMin.value = parseFloat(slider.min);
  if (sliderMax) sliderMax.value = parseFloat(slider.max);
  handleChange();
}

function updateSliderMin() {
  const slider = document.getElementById('xpSlider');
  if (!slider) return;
  const min = parseFloat(document.getElementById('sliderMin').value);
  slider.min = min;
  if (parseFloat(slider.value) < min) {
    slider.value = min;
    updateSliderValue();
  }
  handleChange();
}

function updateSliderMax() {
  const slider = document.getElementById('xpSlider');
  if (!slider) return;
  const max = parseFloat(document.getElementById('sliderMax').value);
  slider.max = max;
  if (parseFloat(slider.value) > max) {
    slider.value = max;
    updateSliderValue();
  }
  handleChange();
}
</script>
```

```html
<div>
  <div class="flex justify-between items-center mb-1">
    <label class="config-label mb-0">Overlay opacity</label>
    <span id="join_opacity_val" class="text-[10px] text-gray-500">50%</span>
  </div>
  <input type="range" class="range-slider" min="0" max="100" value="50" oninput="updateCardValue('join', 'opacity', this.value)">
</div>
```

## Point 22 - Modern Checkbox
Modern checkbox row pattern used in XP settings.

```html
<style>
  .checkbox-group {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background-color: #1e1f22;
    border-radius: 6px;
    border: 1px solid #3f4147;
    cursor: pointer;
  }

  .checkbox-group input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: #5865f2;
  }

  .checkbox-group label {
    cursor: pointer;
    flex: 1;
    font-size: 14px;
  }
</style>

<div class="checkbox-group">
  <input type="checkbox" id="roleRewardsEnabled" checked onchange="handleChange()">
  <label for="roleRewardsEnabled">Enable role rewards</label>
</div>

<div class="checkbox-group">
  <input type="checkbox" id="removePrevRole" checked onchange="handleChange()">
  <label for="removePrevRole">Remove previous role on level up</label>
</div>

<script>
function wireCheckboxGroups() {
  document.querySelectorAll('.checkbox-group').forEach(group => {
    group.addEventListener('click', (e) => {
      if (e.target && e.target.tagName && e.target.tagName.toLowerCase() === 'input') return;
      const input = group.querySelector('input[type="checkbox"]');
      if (input) {
        input.checked = !input.checked;
        handleChange();
      }
    });
  });
}
</script>
```
