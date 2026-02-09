# AutoClaudeBot – File Structure & Development Guide

This document explains the **complete structure**, **startup flow**, and **development workflow** of **AutoClaudeBot**.  
It is intended for contributors who want to understand how the GUI, backend, and core logic connect, and how to correctly add or modify features.

---

## Top-Level Files

Inside the `AutoClaude` folder you will find:

- `Start.py` � Launches the app.
- `Backend.py` � FastAPI backend and API routes.
- `Database.py` � Stores last state of the GUI (toggles, dropdowns, text inputs). Stores in data.db
- `Message_Database.py` � Stores message history and manages Messages_database.py
- `GUI.html` � Main web UI entry point.
- `Core/` � Contain all the python files for Bakcend
- `GUI/` � Contains all the html and javascritps

## 2. Startup Flow

When you start the application:

1. You run `Start.py`
2. `Start.py` starts:
   - `Backend.py`
   - `GUI.html`
3. `GUI.html` opens in the browser and acts as the main interface
4. User interactions in `GUI.html` load specific pages from the `GUI/` folder
5. Those pages communicate with `Backend.py`
6. `Backend.py` executes logic from the `Core/` scripts and returns responses


## GUI Architecture

`GUI.html` contains the main dashboard and navigation. When a button is clicked, it loads the corresponding page from `GUI/`.

### GUI Folders

- `GUI/Level/`
- `GUI/Reaction_Roles/`
- `GUI/Scheduled_Announcement/`
- `GUI/Welcome_Goodbye/`

### GUI Files

- `Commands.html`
- `Leaderboard.html`
- `Level.html`
- `Reaction_Roles.html`
- `Scheduled_Announcement.html`
- `Setting.html`
- `TEMPLATE.html`
- `Welcome_Goodbye.html`

Each of these HTML files is loaded by `GUI.html`. If a page needs extra JavaScript, the script lives in a matching folder under `GUI/`.

## Core Structure

`Core/` contains the Discord logic classes used by `Backend.py`:

- `Commands.py`
- `Leaderboard_Command.py`
- `Level.py`
- `Reaction_Roles.py`
- `scheduled_announcements.py`
- `Setting.py`
- `Welcome_Goodbye.py`

`Backend.py` imports these classes and runs them as needed.

---

### How to Create or Edit Any Script in AutoClaudeBot

This section explains the **correct workflow** for adding or modifying features.

---

### Step 1: Creating or Editing a GUI Page

1. Open the `GUI/` folder
2. Copy `TEMPLATE.html`
3. Rename it (example: `MyFeature.html`)
4. Edit the HTML and UI elements
5. If needed:
   - Create a folder like `GUI/MyFeature/`
   - Add JavaScript files inside it
6. Connect the new page inside `GUI.html` so it can be opened

---

### Step 2: Making the GUI Remember State

To remember state when:
- Refreshing the app
- Closing and reopening
- Switching pages

Examples:
- Text input values
- Toggle ON/OFF
- Dropdown selections
- Last selected server

Steps:
1. Add storage logic in `Database.py`
2. Create API routes in `Backend.py`
3. Save values whenever the UI changes
4. Restore values when the page loads

---

### Step 3: Adding Backend Logic

If your feature needs to work with Discord data (channels, roles, servers, etc.):

1. Create a new class inside `Backend.py` (temporary)
2. Use the Discord token to:
   - Fetch channel lists
   - Fetch role lists
   - Fetch server data
3. Expose the data using API routes
4. Connect the API routes to the GUI using JavaScript

---

### Step 4: Connecting Databases

Your backend logic can:
- Read/write UI state using `Database.py`
- Store or read message data using `Message_Database.py`
- Access other databases or scripts if needed

---

### Step 5: Testing

Before finalizing:
- Test every button
- Test every API route
- Verify UI state restoration
- Ensure no errors occur in backend logs

---

### Step 6: Final Cleanup (IMPORTANT)

Once everything works correctly:

1. Create a new Python file inside `Core/`
2. Name it **exactly the same as the HTML file**
   - Example:
     - `Level.html` → `Core/Level.py`
3. Move all feature-related classes from `Backend.py` into this Core file
4. Import the Core class back into `Backend.py`
5. Keep `Backend.py` clean and minimal

---

##  Architecture Summary

Start.py
↓
GUI.html
↓
GUI/.html + JavaScript
↓
Backend.py (API & Controller)
↓
Core/.py (Discord Feature Logic)
↓
Database.py / Message_Database.py

---



# Prompt/Steps to Create a Command in AutoClaudeBot

Developer guide: add a new slash command with a web-controllable toggle and role-based permissions.

## 1. Database Layer (`AutoClaude/Database.py`)

Add a new key in the default settings dictionary:

```python
"commands_new_feature": {
    "enabled": False,
    "role_ids": []
}
```

## 2. Core Logic Layer (`AutoClaude/Core/Commands.py`)

Add the command inside `IntegratedCommandBot.setup_hook`:

```python
@self.tree.command(name="mycommand", description="Does something cool")
async def mycommand(interaction: discord.Interaction):
    cfg = self.db.get_settings().get("commands_new_feature", {})
    if not self._check_perms(interaction, cfg):
        return

    await interaction.response.send_message("Success!")
```

## 3. Backend API Layer (`AutoClaude/Backend.py`)

Add GET and POST endpoints:

```python
@app.post("/api/settings/commands-new-feature")
async def save_new_settings(payload: Dict = Body(...)):
    db_manager.save_settings({"commands_new_feature": payload})
    if command_bot_instance:
        asyncio.create_task(command_bot_instance.refresh_permissions())
    return {"success": True}
```

## 4. GUI Layer (`AutoClaude/GUI/Commands.html`)

Add a new command card and initialize a `CommandManager`:

```javascript
const newFeatureManager = new CommandManager('uniquePrefix', '/api/settings/commands-new-feature');
newFeatureManager.loadSettings();
```

---

## Summary Workflow

1. Add persistent state in `Database.py`.
2. Implement the slash command in `Core/Commands.py`.
3. Add API routes in `Backend.py`.
4. Add the GUI card and JS wiring in `Commands.html`.
