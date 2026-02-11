# How to Vibe Code

---
This app is built so you can ship Discord bot features in minutes, not days.
This file is the direct, technical guide for building, editing, and debugging features in AutoClaude.
The value is the workflow speed and the predictable architecture and the ability to create new features in minutes.

Use this guide to:
- understand the real file map and ownership
- build features with repeatable workflow
- debug bugs across GUI, API, DB, and Core quickly
- use production-ready prompts with placeholders

---

## Starter Prompt (Simple and Safe)

Copy-paste this first when using any AI agent:

```text
You are editing only inside: Github\\AutoClaude
Do not edit outside this folder.

Important:
- Do NOT read all 30+ scripts at the start.
- First read only: ..\\Features.md and ..\\File Structure.md
- Use Features.md to understand what each script does.
- After that, open only the files needed for my task.

Task:
[Write my feature/command/bugfix in one simple sentence]

Rules:
1) Before editing, tell me exactly which files you will edit and why.
2) Reuse existing routes and patterns when possible.
3) If adding new routes, keep names consistent with existing style.
4) Keep Backend.py clean; put runtime logic in Core/*.py.
5) Save settings in Database.py and make UI remember last state.
6) After coding, give: changed files, tests done, and any risks.
```

## Index (Where To Look)

| Section | What to use it for |
| --- | --- |
| `## Steps To Use AutoClaudeBot with high effeciency` | Quick speed workflow rules. |
| `## Mandatory Read Order For Any Agent` | Strict read order before coding. |
| `## Fast Mental Model` | 30-second architecture understanding. |
| `## Real File Ownership` | See which file controls which part. |
| `## Database Contract` | Understand what data is saved and where. |
| `## Golden Workflow 1: Create Or Edit Any Script` | Build full feature workflow. |
| `## Golden Workflow 2: Create Or Edit Any Command` | Build slash command workflow. |
| `## Example Workflows (Beginner Friendly)` | Practical step-by-step workflows. |
| `### Example 1: Get Edited/Deleted Members Messages inside a channel` | Build message edit/delete logs feature. |
| `### Example 2: Edit an Existing WebPage and Add One New Option` | Safely add a new option to old pages. |
| `### Example 3: Create a New Slash Command (Very Simple)` | Add command with GUI permissions. |
| `### Example 4: Fix a Bug (Clear Beginner Order)` | Find bug source and patch safely. |
| `### Example 5: Build AutoMod Keyword Filter` | Build blocked-word moderation feature. |
| `### Example 6: Build Ticket Panel (Support Feature)` | Build support tickets flow. |
| `### Example 7: Add One New Card Design Option (Quick Customization)` | Add one UI customization field. |
| `### Example 8: Build Multiple Features in Parallel (Without Using AutoClaude)` | Build multiple features without conflicts. |
| `# PROMPTS - COPY PASTE READY` | Ready prompts for common tasks. |
| `## Prompt 1: Build New Feature End-To-End` | Full feature from GUI to Core. |
| `## Prompt 2: Edit Existing Feature Safely` | Edit without breaking existing behavior. |
| `## Prompt 3: Create/Edit Slash Command` | Command + role permission workflow. |
| `## Prompt 4: Full Bug Investigation` | Full debugging workflow. |
| `## Prompt 5: Missing Feature Builder` | Build missing feature safely. |
| `## Prompt 6: Multi-Agent Parallel Delivery` | Parallel development workflow. |
| `## Prompt Fill Mini Template` | Short reusable prompt template. |
| `## Quality Gate Checklist` | Final checks before done. |
| `## Deep Validation Matrix` | Layer-by-layer validation checklist. |
| `## Final Notes` | Final reminders. |
| `## How to Create or Edit Any Script in AutoClaudeBot` | Alternate script workflow. |
| `## Prompt/Steps to Create a Command in AutoClaudeBot` | Alternate command workflow. |
| `## Feature Playbooks (Real Modules)` | Module-specific practical playbooks. |
| `## Additional High-Demand Missing Feature Examples (Simple)` | Extra feature ideas and edit order. |
| `### Example A: Voice Activity Tracker` | Build voice activity tracking feature. |
| `### Example B: Invite Tracker` | Build invite tracking feature. |
| `### Example C: Birthday Announcements` | Build birthday announcement feature. |
| `### Example D: Simple Moderation Notes` | Build private mod notes feature. |
| `## Root Cause Locator Matrix` | Quickly classify bug layer. |
| `## Final Delivery Format You Should Demand From AI` | Enforce useful AI output format. |
| `## API Contract Map` | Full backend route list. |

---

## Steps To Use AutoClaudeBot with high effeciency

1. Start from one clear feature goal.
2. Pick the closest workflow in this file.
3. Fill the matching prompt template.
4. Keep folder boundaries strict.
5. Read markdown docs first.
6. Map target files before edits.
7. Keep edits minimal and targeted.
8. Keep Backend.py clean and coordinator-focused.
9. Move final feature runtime logic into Core/.
10. Save and restore GUI state using Database.py.
11. Test GUI, API, and Discord runtime.
12. Return file list, route list, and risk notes.

---

### Use AutoClaude App Built By AndyMik90 to increase workflow by 10x
- [Github Link To AutoClaude](https://github.com/AndyMik90/Auto-Claude)
- You can use Kanban Board to effeciently manage your workflow and testing.
- You can run up to 12 agent terminals inside of Agents Terminal To Ship Upto 12 Features at the same time.
- Protect shared files: Backend.py, Database.py, GUI.html, GUI/Commands.html. Merging Will easily be handled by AutoClaude.
- Use AutoClaude to build your personalized features in a matter of minutes.

---

## Mandatory Read Order For Any Agent

1. Github\\How to Vibe Code.md
2. Github\\README.md
3. Github\\Features.md
4. Github\\File Structure.md


Output expected before editing:
- files to edit
- route changes
- config key changes
- test plan

---

## Fast Mental Model

- Start.py launches backend and opens GUI.
- GUI.html loads server list and opens feature iframes.
- Feature pages call /api routes.
- Backend.py validates and routes data.
- Database.py persists settings and per-guild config in data.db.
- Message_Database.py persists high-volume message analytics in SQLite.
- Core modules execute Discord runtime behavior.

```text
Start.py
  -> Backend.py + browser
GUI.html
  -> select server
  -> open feature page
Feature HTML + JS
  -> GET/POST /api/...
Backend.py
  -> Database.py / Message_Database.py
  -> Core/*.py runtime clients
```

---

## Real File Ownership

### AutoClaude\\Start.py
- Role: Launch orchestration
- Why it matters: Starts backend process, opens browser, handles port cleanup.

### AutoClaude\\Backend.py
- Role: HTTP API + runtime coordinator
- Why it matters: All API routes, client startup, image upload, history jobs.

### AutoClaude\\Database.py
- Role: Config persistence
- Why it matters: Owns data.db, per-guild configs, settings defaults.

### AutoClaude\\Message_Database.py
- Role: Analytics persistence
- Why it matters: Owns Message_Database.db tables and level rebuild pipeline.

### AutoClaude\\GUI.html
- Role: Dashboard shell
- Why it matters: Server selection and feature iframe launch wiring.

### AutoClaude\\Core\\Welcome_Goodbye.py
- Role: Join/leave/DM/autorole runtime
- Why it matters: Handles member events with text/embed/card modes.

### AutoClaude\\Core\\Reaction_Roles.py
- Role: Reaction role runtime
- Why it matters: Emoji and dropdown role assignment logic + publish.

### AutoClaude\\Core\\Level.py
- Role: Level runtime
- Why it matters: XP, cooldowns, rewards, and announcements.

### AutoClaude\\Core\\scheduled_announcements.py
- Role: Scheduler runtime
- Why it matters: Polls and sends scheduled text/embed/card posts.

### AutoClaude\\Core\\Setting.py
- Role: Hi reaction runtime
- Why it matters: Reacts to hi/hello using configurable emoji.

### AutoClaude\\Core\\Commands.py
- Role: Slash command runtime
- Why it matters: analytics, github, level, leaderboard commands + perms.

### AutoClaude\\Core\\Leaderboard_Command.py
- Role: Interactive leaderboard UI
- Why it matters: Query builder controls, filters, and renderers.

### AutoClaude\\GUI\\Welcome_Goodbye.html
- Role: Welcome/Goodbye page
- Why it matters: Container page for join/leave/DM/role modules.

### AutoClaude\\GUI\\Reaction_Roles.html
- Role: Reaction roles page
- Why it matters: Message + reaction config and publish flow.

### AutoClaude\\GUI\\Level.html
- Role: Levels page
- Why it matters: XP settings, rewards, no-xp rules, announce settings.

### AutoClaude\\GUI\\Scheduled_Announcement.html
- Role: Scheduler page
- Why it matters: Schedule creation, list, edit, delete, post controls.

### AutoClaude\\GUI\\Commands.html
- Role: Command settings page
- Why it matters: Enable toggles and role permissions per command.

### AutoClaude\\GUI\\Setting.html
- Role: Global settings page
- Why it matters: Token and hi-emoji settings.

### AutoClaude\\GUI\\Leaderboard.html
- Role: Leaderboard info page
- Why it matters: UI stub while command-driven leaderboard runs in Discord.

---

## Database Contract

### Message_Database.db tables
- messages: raw message analytics and metadata
- user_levels: cumulative XP and level state

### Formula Used For Level Calculation
- 5 * (level ** 2) + (50 * level) + 100

### data.db keys
- token
- settings.hi_emoji
- settings.hi_enabled
- settings.github_token
- settings.commands_analytics.enabled
- settings.commands_analytics.role_ids
- settings.commands_github.enabled
- settings.commands_github.role_ids
- settings.commands_level.enabled
- settings.commands_level.role_ids
- settings.commands_leaderboard.enabled
- settings.commands_leaderboard.role_ids
- last_server
- servers.{guild_id}.join
- servers.{guild_id}.leave
- servers.{guild_id}.dm
- servers.{guild_id}.role
- servers.{guild_id}.levels
- servers.{guild_id}.reaction_roles
- servers.{guild_id}.scheduled_announcement
- servers.{guild_id}.scheduled_announcements

---

## Golden Workflow 1: Create Or Edit Any Script

### Step 1: Scope
1. Define expected behavior in one sentence.
2. Decide if GUI is needed.
3. Decide if runtime listener is needed.
4. Decide config keys and persistence shape.

### Step 2: GUI
1. Copy GUI/TEMPLATE.html when creating a new page.
2. Add JS file in matching GUI subfolder if required.
3. Implement state object, validation, and save UX.

### Step 3: Backend
1. Add GET route to load config.
2. Add POST route to save config.
3. Add publish/test route if runtime action is immediate.

### Step 4: Database
1. Save per-guild config through db_manager.save_config.
2. Keep payload normalized and backwards compatible.

### Step 5: Core
1. Put runtime logic in Core/<Feature>.py.
2. Keep Backend.py as coordinator, not heavy logic host.
3. Wire class in Backend main clients list when needed.

### Step 6: Test
1. Test GET load.
2. Test POST save.
3. Test reload restore state.
4. Test restart restore state.
5. Test Discord runtime behavior.

### Diagram
```text
Feature idea
  -> GUI page + JS
  -> Backend routes
  -> Database save/load
  -> Core runtime
  -> GUI + Discord tests
```

---

## Golden Workflow 2: Create Or Edit Any Command

### Step 1: Add settings key in Database.py
```python
"commands_new_feature": {
    "enabled": False,
    "role_ids": []
}
```

### Step 2: Add Backend GET/POST endpoints
- GET /api/settings/commands-new-feature
- POST /api/settings/commands-new-feature
- Save settings and refresh command permissions.

### Step 3: Add slash command in Core/Commands.py
- Read config from settings key.
- Enforce _check_perms(interaction, cfg).
- Implement command response logic.

### Step 4: Add command card in GUI/Commands.html
- Toggle
- Role multiselect
- CommandManager wiring

### Step 5: Validate
- Disabled command blocked
- Unauthorized role blocked
- Authorized role allowed

### Diagram
```text
Database key
  -> Backend settings API
  -> Core slash command
  -> Commands GUI card
  -> Permission refresh + tests
```

---

## Example Workflows (Beginner Friendly)

This section is written in simple language.
Each example tells you exactly which file to touch first, second, and third.

### Example 1: Get Edited/Deleted Members Messages inside a channel

What you are making:
- A new feature that posts edited or deleted message logs into one selected channel.

Files you will touch:
- `AutoClaude\GUI.html`
- `AutoClaude\GUI\Message_Logs.html` (new)
- `AutoClaude\GUI\Message_Logs\Message_Logs.js` (new)
- `AutoClaude\Backend.py`
- `AutoClaude\Database.py`
- `AutoClaude\Core\Message_Logs.py` (new)

Step-by-step:
1. Edit `AutoClaude\GUI.html`.
2. Add one new card/button called `Message Logs` so the page can be opened.
3. Create `AutoClaude\GUI\Message_Logs.html` from `GUI\TEMPLATE.html`.
4. In that new HTML, add very simple controls:
- on/off toggle
- output channel dropdown
- include channels list
- exclude channels list
- include roles list
- exclude roles list
5. Create `AutoClaude\GUI\Message_Logs\Message_Logs.js`.
6. Add load and save calls in JS:
- load from `GET /api/config/message-logs/{guild_id}`
- save to `POST /api/config/message-logs/{guild_id}`
7. Edit `AutoClaude\Backend.py`.
8. Add those two routes (GET + POST).
9. Edit `AutoClaude\Database.py`.
10. Save this feature under `servers.{guild_id}.message_logs`.
11. Create `AutoClaude\Core\Message_Logs.py`.
12. Add one class (for example `MessageLogsServer`) that listens to message edit/delete and sends logs.
13. Edit `AutoClaude\Backend.py` again.
14. Import your new class and add it to the `clients` list in `main()`.
15. Test by editing and deleting messages in Discord.

Simple workflow:

```text
Create Message Logs page
  -> save/load settings
  -> store settings in Database.py
  -> create MessageLogs runtime class
  -> connect class in Backend.py
  -> test in Discord
```

Done when:
- settings save and load after refresh
- logs send only when toggle is ON
- logs go to the selected channel

---

### Example 2: Edit an Existing WebPage and Add One New Option

What you are making:
- Add one more option in an existing feature page.

Files you will touch:
- target HTML page in `AutoClaude\GUI\...`
- matching JS file in `AutoClaude\GUI\<Feature>\...js`
- `AutoClaude\Backend.py`
- `AutoClaude\Database.py`
- matching file in `AutoClaude\Core\...py`

Step-by-step:
1. Edit the HTML file and add your new input/toggle/dropdown.
2. Edit the JS file and add that value to the page state.
3. In JS load function, map that value from API response to the UI.
4. In JS save function, include that value in POST body.
5. In `Backend.py`, make sure the route accepts and returns this value.
6. In `Database.py`, make sure this value gets saved inside feature config.
7. In Core file, use this value in runtime behavior.
8. Test old options to make sure nothing broke.

Simple workflow:

```text
Edit HTML control
  -> connect in JS state
  -> send value to Backend.py
  -> save in Database.py
  -> use value in Core logic
  -> test old + new behavior
```

Done when:
- new option stays after refresh/restart
- existing options still work
- runtime behavior changes only when expected

---

### Example 3: Create a New Slash Command (Very Simple)

What you are making:
- A new command like `/reminder` with enable toggle and allowed roles.

Files you will touch:
- `AutoClaude\Database.py`
- `AutoClaude\Backend.py`
- `AutoClaude\Core\Commands.py`
- `AutoClaude\GUI\Commands.html`

Step-by-step:
1. Open `Database.py` and add a new settings key:
- `commands_reminder` with `enabled` and `role_ids`.
2. Open `Backend.py` and add:
- `GET /api/settings/commands-reminder`
- `POST /api/settings/commands-reminder`
3. Open `Core\Commands.py` and create command `/reminder`.
4. Before command logic, check permissions with your settings key.
5. Open `GUI\Commands.html` and add one command card.
6. Connect that card to your new API endpoint.
7. Save from GUI and test in Discord.

Simple workflow:

```text
Add key in Database.py
  -> add routes in Backend.py
  -> add /command in Core/Commands.py
  -> add card in Commands.html
  -> test role permission
```

Done when:
- command can be enabled/disabled from GUI
- only selected roles can use it
- save works without restart

---

### Example 4: Fix a Bug (Clear Beginner Order)

What you are doing:
- Find exactly where the bug is and patch only that part.

Files you may touch:
- feature HTML + JS
- `Backend.py`
- `Database.py`
- matching `Core` file

Step-by-step:
1. Reproduce bug and write exact steps.
2. Check JS first:
- is click/change event firing?
- is fetch URL correct?
- is payload correct?
3. Check `Backend.py` route:
- is the same route path present?
- is payload read correctly?
4. Check `Database.py` save/load:
- are values really saved?
- are values returned correctly?
5. Check Core file:
- is Core reading the same key names?
6. Fix smallest possible part.
7. Test bug path and nearby features.

Simple workflow:

```text
Reproduce bug
  -> check JS event/payload
  -> check Backend route
  -> check Database save/load
  -> check Core key usage
  -> fix smallest part
  -> retest
```

Done when:
- bug is gone
- no new errors appear
- related feature still works

---

### Example 5: Build AutoMod Keyword Filter

What you are making:
- A feature that deletes blocked words and optionally warns user.

Files you will touch:
- `AutoClaude\GUI\AutoMod.html` (new)
- `AutoClaude\GUI\AutoMod\AutoMod.js` (new)
- `AutoClaude\Backend.py`
- `AutoClaude\Database.py`
- `AutoClaude\Core\AutoMod.py` (new)

Step-by-step:
1. Add `AutoMod` card in `GUI.html`.
2. Create `GUI\AutoMod.html` page with controls:
- toggle
- blocked words list
- bypass roles
- bypass channels
- warning message toggle
3. Create `GUI\AutoMod\AutoMod.js` for load/save.
4. Add routes in `Backend.py`:
- GET/POST `/api/config/automod/{guild_id}`
5. Save config in `Database.py` under `automod`.
6. Create class in `Core\AutoMod.py` to check messages and apply rules.
7. Connect class in `Backend.py` clients list.
8. Test with blocked and allowed messages.

Simple workflow:

```text
Build AutoMod page
  -> save config routes
  -> store in Database.py
  -> create AutoMod class in Core
  -> connect in Backend.py
  -> test in server
```

Done when:
- blocked words are deleted
- bypass rules work
- warning works if enabled

---

### Example 6: Build Ticket Panel (Support Feature)

What you are making:
- Admin publishes a support panel, user clicks, ticket channel is created.

Files you will touch:
- `AutoClaude\GUI\Tickets.html` (new)
- `AutoClaude\GUI\Tickets\Tickets.js` (new)
- `AutoClaude\Backend.py`
- `AutoClaude\Database.py`
- `AutoClaude\Core\Tickets.py` (new)

Step-by-step:
1. Add `Tickets` open button in `GUI.html`.
2. Create tickets page with controls:
- ticket panel text
- target category
- support roles
- open/close button text
3. Create tickets JS load/save.
4. Add GET/POST routes in `Backend.py` for ticket config.
5. Save to `Database.py` under `tickets`.
6. Create class in `Core\Tickets.py` for button interactions.
7. Add publish route if panel send is manual.
8. Connect class in backend clients list and test full flow.

Simple workflow:

```text
Create Tickets page
  -> add config routes
  -> save ticket settings
  -> create Ticket runtime class
  -> publish panel
  -> user opens ticket
```

Done when:
- panel posts correctly
- ticket channel/thread is created
- permissions are correct

---

### Example 7: Add One New Card Design Option (Quick Customization)

What you are making:
- One new visual option in welcome card (example: border color).

Files you will touch:
- `AutoClaude\GUI\Welcome_Goodbye\Join_Server.js`
- `AutoClaude\GUI\Welcome_Goodbye.html`
- `AutoClaude\Backend.py`
- `AutoClaude\Database.py`
- `AutoClaude\Core\Welcome_Goodbye.py`

Step-by-step:
1. Add border color input in welcome card UI.
2. Add border color key to JS state.
3. Save and load this key in join config route.
4. Save this key in Database feature config.
5. In Core welcome card drawing logic, apply border color.
6. Test with color set and unset.

Simple workflow:

```text
Add UI input
  -> add JS state key
  -> save/load in Backend
  -> store in Database
  -> apply in Core image draw
  -> test
```

Done when:
- border color stays saved
- card image reflects selected color
- old card settings still work

---

### Example 8: Build Multiple Features in Parallel (Without Using AutoClaude)

What you are doing:
- Build many features faster without file conflicts.

Step-by-step:
1. Split work into small independent tasks.
2. Give one task to one AI terminal.
3. Do not let two terminals edit `Backend.py` at the same time.
4. Do not let two terminals edit `Database.py` at the same time.
5. Finish each feature branch first.
6. Merge shared-file changes at the end in one terminal.
7. Run full check:
- all pages open
- all routes work
- all saves restore
- no command conflicts

Simple workflow:

```text
Split tasks
  -> one terminal per task
  -> protect shared files
  -> merge carefully
  -> run full app checks
```

Done when:
- all features run
- no broken routes
- no missing imports
- old features still work

---

# PROMPTS - COPY PASTE READY

These prompts follow the same theme as script/command workflows and are production-ready.

## Prompt 1: Build New Feature End-To-End

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
New GUI + API + Core + persistence.

Fill these placeholders:
- [feature_name]
- [gui_page]
- [js_file]
- [route_prefix]
- [config_key]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Include server switch, restart persistence, and Discord runtime tests.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

## Prompt 2: Edit Existing Feature Safely

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
Add new controls without breaking old behavior.

Fill these placeholders:
- [target_feature]
- [new_controls]
- [payload_changes]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Require backward compatibility and regression checks.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

## Prompt 3: Create/Edit Slash Command

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
Add command with GUI permission card.

Fill these placeholders:
- [command_name]
- [description]
- [settings_key]
- [endpoint_path]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Require _check_perms and role-based validation tests.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

## Prompt 4: Full Bug Investigation

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
Find root cause across GUI/API/DB/Core.

Fill these placeholders:
- [bug_report]
- [expected]
- [actual]
- [reproduce_steps]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Require minimal safe fix and regression summary.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

## Prompt 5: Missing Feature Builder

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
Implement message edit/delete logging module.

Fill these placeholders:
- [message_logs config]
- [filters]
- [output channel]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Require dedicated Core module and explicit API contract.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

## Prompt 6: Multi-Agent Parallel Delivery

```text
You are editing only inside this folder:
AutoClaudeBot\\AutoClaude
Do not edit outside this folder.

Read first, in order:
1) ..\\README.md
2) ..\\Features.md
3) ..\\File Structure.md
4) Database.py
5) Backend.py
6) Message_Database.py
7) Core\\*.py relevant to task
8) GUI.html
9) GUI\\*.html and GUI\\**\\*.js relevant to task

Task goal:
Ship multiple features with controlled merges.

Fill these placeholders:
- [feature_list]
- [shared_files]
- [integration_checks]

Mandatory implementation workflow:
1) Output impacted files before editing.
2) Implement GUI/API/DB/Core changes with minimal diff.
3) Keep Backend.py lean and coordinator-focused.
4) Persist and restore state correctly.
5) Validate routes, payloads, and runtime behavior.
6) Retest adjacent flows for regressions.

Special requirement:
Require collision checks for routes, settings keys, and imports.

Output required:
- files changed and why
- routes changed
- config keys changed
- tests executed and results
- unresolved risks
```

---

## Prompt Fill Mini Template

```text
You are editing only inside AutoClaudeBot\\AutoClaude. Do not edit outside this folder.
Read docs first: ..\\README.md, ..\\Features.md, ..\\File Structure.md.
Task: [YOUR_TASK]
Files likely involved: [FILES]
Must return: files changed, routes changed, config changes, tests, risks.
```

---

## Quality Gate Checklist
1. Feature opens from GUI.html correctly.
2. Server switching still works.
3. GET config returns expected shape.
4. POST config saves expected shape.
5. Values restore after refresh.
6. Values restore after restart.
7. Core runtime uses latest config values.
8. No backend tracebacks.
9. No browser console exceptions.
10. No route path collisions.
11. No settings-key collisions.
12. No import-cycle or duplicate-class issues.
13. Commands sync if command code changed.
14. Permission checks still enforced.
15. Existing features still work.

---

## Deep Validation Matrix

### GUI
- [ ] Input validation present
- [ ] Error handling present
- [ ] State persistence validated
- [ ] Restore-on-load validated
- [ ] Permission behavior validated
- [ ] Empty value behavior validated
- [ ] Invalid value behavior validated
- [ ] Backwards compatibility validated
- [ ] Logging clarity validated
- [ ] Regression check completed

### Backend
- [ ] Input validation present
- [ ] Error handling present
- [ ] State persistence validated
- [ ] Restore-on-load validated
- [ ] Permission behavior validated
- [ ] Empty value behavior validated
- [ ] Invalid value behavior validated
- [ ] Backwards compatibility validated
- [ ] Logging clarity validated
- [ ] Regression check completed

### Database
- [ ] Input validation present
- [ ] Error handling present
- [ ] State persistence validated
- [ ] Restore-on-load validated
- [ ] Permission behavior validated
- [ ] Empty value behavior validated
- [ ] Invalid value behavior validated
- [ ] Backwards compatibility validated
- [ ] Logging clarity validated
- [ ] Regression check completed

### Core Runtime
- [ ] Input validation present
- [ ] Error handling present
- [ ] State persistence validated
- [ ] Restore-on-load validated
- [ ] Permission behavior validated
- [ ] Empty value behavior validated
- [ ] Invalid value behavior validated
- [ ] Backwards compatibility validated
- [ ] Logging clarity validated
- [ ] Regression check completed

### Discord API
- [ ] Input validation present
- [ ] Error handling present
- [ ] State persistence validated
- [ ] Restore-on-load validated
- [ ] Permission behavior validated
- [ ] Empty value behavior validated
- [ ] Invalid value behavior validated
- [ ] Backwards compatibility validated
- [ ] Logging clarity validated
- [ ] Regression check completed

---

## Final Notes
This project is designed for fast extension with strong structure.
Do not skip read order, persistence wiring, runtime wiring, and tests.
Follow this guide and one prompt can drive full implementation reliably.
Use parallel agents carefully and protect shared files.
This is the practical path from basic bot to custom server platform.

---

## How to Create or Edit Any Script in AutoClaudeBot

This is the fixed, production version of the original workflow and keeps the same design pattern.

### Step 1: Create or Edit GUI

1. Open `GUI/`.
2. Copy `TEMPLATE.html` if creating a new page.
3. Rename to target feature name.
4. Add/adjust controls, toggles, dropdowns, and save UX.
5. If needed, create `GUI/<Feature>/` and add JS files.
6. Connect page launch path from `GUI.html` modal routing.

### Step 2: Make GUI Remember State

1. Add state keys in page JS.
2. Load state through feature GET endpoint.
3. Save state through feature POST endpoint.
4. Restore all controls on load:
- text input
- dropdown selections
- toggle state
- mode tab selection
- color/image/font selections

### Step 3: Add Backend Logic

1. Add feature routes in `Backend.py`.
2. Validate `guild_id` and payload shape.
3. Save through `db_manager.save_config`.
4. Return stable JSON responses.

### Step 4: Connect Databases

1. Use `Database.py` for settings and feature configs.
2. Use `Message_Database.py` only when analytics or message history is required.
3. Keep payload keys consistent between GUI, backend, and core runtime.

### Step 5: Add Runtime Feature Logic

1. Build or edit runtime class in `Core/`.
2. Ensure runtime class reads the same config keys GUI writes.
3. Add guard checks for disabled mode, missing channel/role, missing permissions.
4. Wire class instance in `Backend.py` `clients` list if needed.

### Step 6: Test and Cleanup

1. Manual test from GUI.
2. Manual Discord behavior test.
3. Restart app and confirm persistence.
4. Keep `Backend.py` minimal and move heavy runtime logic into `Core/`.

### Architecture Summary

```text
Start.py
  -> Backend.py
  -> GUI.html
GUI/*.html + JS
  -> Backend API routes
Backend.py
  -> Core/*.py runtime logic
  -> Database.py / Message_Database.py persistence
```

---

## Prompt/Steps to Create a Command in AutoClaudeBot

This keeps the same design as your command workflow but with production hardening.

### 1. Database Layer (`AutoClaude/Database.py`)

Add default settings key:

```python
"commands_new_feature": {
    "enabled": False,
    "role_ids": []
}
```

### 2. Core Logic Layer (`AutoClaude/Core/Commands.py`)

Add slash command in `setup_hook` and enforce permissions:

```python
@self.tree.command(name="mycommand", description="Does something useful")
async def mycommand(interaction: discord.Interaction):
    cfg = self.db.get_settings().get("commands_new_feature", {})
    if not self._check_perms(interaction, cfg):
        return

    await interaction.response.send_message("Success")
```

### 3. Backend API Layer (`AutoClaude/Backend.py`)

Add GET and POST settings routes and refresh permissions on save:

```python
@app.post("/api/settings/commands-new-feature")
async def save_new_feature_settings(payload: Dict = Body(...)):
    enabled = bool((payload or {}).get("enabled", False))
    role_ids = (payload or {}).get("role_ids", [])
    if not isinstance(role_ids, list):
        role_ids = []
    db_manager.save_settings({"commands_new_feature": {"enabled": enabled, "role_ids": role_ids}})
    if command_bot_instance:
        asyncio.create_task(command_bot_instance.refresh_permissions())
    return {"success": True}
```

### 4. GUI Layer (`AutoClaude/GUI/Commands.html`)

Add command card and `CommandManager` binding:

```javascript
const newFeatureManager = new CommandManager('newfeature', '/api/settings/commands-new-feature');
newFeatureManager.loadSettings();
```

### Summary Workflow

1. Add default setting key.
2. Add command handler in `Core/Commands.py`.
3. Add backend settings routes.
4. Add command card in `Commands.html`.
5. Validate role-gated execution.

---

## Feature Playbooks (Real Modules)

### Welcome, Leave, DM, Auto-Role

Files:
- `Core/Welcome_Goodbye.py`
- `GUI/Welcome_Goodbye.html`
- `GUI/Welcome_Goodbye/Join_Server.js`
- `GUI/Welcome_Goodbye/Join_Private_message.js`
- `GUI/Welcome_Goodbye/Join_Role.js`
- `GUI/Welcome_Goodbye/Leave_Server.js`
- `Backend.py` routes: `/api/config/join|leave|dm|role/{guild_id}`

Playbook:
1. Keep mode handling aligned (`text`, `embed`, `card`).
2. Preserve placeholder rendering parity between GUI preview and runtime send.
3. If adding new card style field, add it in JS state + backend payload + runtime rendering.
4. Validate channel and role permissions before sending or assigning.

### Reaction Roles

Files:
- `Core/Reaction_Roles.py`
- `GUI/Reaction_Roles.html`
- `GUI/Reaction_Roles/Message.js`
- `GUI/Reaction_Roles/Reaction_And_Roles.js`
- `Backend.py` routes: `/api/config/reaction-roles/{guild_id}`, `/api/publish/reaction-roles/{guild_id}`

Playbook:
1. Keep payload shape normalized through `ReactionRoleDB.format_payload`.
2. Preserve support for both `emoji` and `dropdown` types.
3. Preserve mode handling (`default`, `reverse`).
4. Validate role existence and message publish success path.

### Levels + Leaderboard Data

Files:
- `Core/Level.py`
- `Message_Database.py`
- `GUI/Level.html`
- `GUI/Level/Message_Database.js`
- `Backend.py` routes: `/api/config/levels/{guild_id}`, `/api/messages/download/*`, `/api/stats/messages-today/*`

Playbook:
1. Keep no-xp channels and roles checks before gain logic.
2. Keep cooldown behavior deterministic.
3. Preserve formula safety and parsing guards.
4. When changing formula behavior, validate rebuild and live gain consistency.

### Scheduled Announcements

Files:
- `Core/scheduled_announcements.py`
- `GUI/Scheduled_Announcement.html`
- `GUI/Scheduled_Announcement/Message.js`
- `Backend.py` routes: `/api/config/scheduled-announcement/*`, `/api/publish/scheduled-announcement/*`

Playbook:
1. Keep draft vs scheduled status transitions explicit.
2. Preserve text/embed/card send paths.
3. Validate channel existence and graceful failure status updates.
4. Keep timezone parse behavior predictable.

### Commands and Permissions

Files:
- `Core/Commands.py`
- `GUI/Commands.html`
- `Backend.py` `/api/settings/commands-*`
- `Database.py` settings keys

Playbook:
1. Every command needs `enabled + role_ids` config.
2. GUI save must immediately affect permission behavior.
3. Refresh command permission cache after save.
4. Keep unauthorized error message clean and ephemeral.

---

## Additional High-Demand Missing Feature Examples (Simple)

### Example A: Voice Activity Tracker

Goal:
- Track who joins/leaves voice channels and how long they stayed.

Edit order:
1. Create `GUI/Voice_Tracker.html`.
2. Create `GUI/Voice_Tracker/Voice_Tracker.js`.
3. Add GET/POST config routes in `Backend.py`.
4. Save config under `voice_tracker` in `Database.py`.
5. Create `Core/Voice_Tracker.py` class for voice events.
6. Connect class in `Backend.py` clients list.

### Example B: Invite Tracker

Goal:
- Show which invite link user joined from.

Edit order:
1. Create `GUI/Invite_Tracker.html` and JS.
2. Add routes in `Backend.py`.
3. Save config in `Database.py`.
4. Create `Core/Invite_Tracker.py`.
5. On member join, compare invite counts and log result.
6. Test with new invites.

### Example C: Birthday Announcements

Goal:
- Save user birthdays and post birthday message automatically.

Edit order:
1. Create `GUI/Birthday.html` and JS.
2. Add birthday config routes in `Backend.py`.
3. Save birthday config and list in `Database.py`.
4. Create `Core/Birthday.py` daily check class.
5. Connect class in `Backend.py` clients list.
6. Test with a near date entry.

### Example D: Simple Moderation Notes

Goal:
- Store private mod notes per user.

Edit order:
1. Add notes page in GUI.
2. Add GET/POST routes in `Backend.py`.
3. Save notes safely in database layer.
4. Add slash command to view notes for mod roles only.
5. Test role permission and note retrieval.

## Root Cause Locator Matrix

Use this when a bug appears and you need immediate triage.

- Symptom: UI value not saving
- Check first: feature JS save payload + POST endpoint path
- Layer likely: GUI or Backend

- Symptom: value saves but resets on refresh
- Check first: GET route return shape + JS restore mapping
- Layer likely: Backend or GUI

- Symptom: config looks correct but no Discord behavior
- Check first: Core class uses same config keys + class wired in Backend clients list
- Layer likely: Core or Backend wiring

- Symptom: role assignment/reaction fails silently
- Check first: bot permissions and role hierarchy
- Layer likely: Discord runtime constraints

- Symptom: leaderboard values wrong
- Check first: Message_Database rebuild + formula + time range selection
- Layer likely: DB aggregation logic

---

## Final Delivery Format You Should Demand From AI

Ask AI to always return:

1. Changed files list.
2. Why each file changed.
3. New/updated routes.
4. New/updated config keys.
5. Testing checklist with pass/fail notes.
6. Edge cases and known risks.
7. Optional rollback steps.



## API Contract Map

- `GET /` : Serve GUI.html
- `GET /gui/welcome-goodbye` : Serve Welcome_Goodbye page
- `GET /gui/reaction-roles` : Serve Reaction_Roles page
- `GET /gui/scheduled-announcement` : Serve Scheduled_Announcement page
- `GET /api/servers` : Guild list + last server
- `GET /api/settings/token` : Load Discord token
- `POST /api/settings/token` : Save Discord token
- `GET /api/settings/github-token` : Load GitHub token
- `POST /api/settings/github-token` : Save GitHub token
- `GET /api/settings/hi-emoji` : Load hi-emoji config
- `POST /api/settings/hi-emoji` : Save hi-emoji config
- `GET /api/settings/commands-analytics` : Load analytics command perms
- `POST /api/settings/commands-analytics` : Save analytics command perms
- `GET /api/settings/commands-level` : Load level command perms
- `POST /api/settings/commands-level` : Save level command perms
- `GET /api/settings/commands-leaderboard` : Load leaderboard command perms
- `POST /api/settings/commands-leaderboard` : Save leaderboard command perms
- `GET /api/settings/commands-github` : Load github command perms
- `POST /api/settings/commands-github` : Save github command perms
- `GET /api/guilds/{guild_id}/select` : Set active guild context
- `GET /api/guilds/{guild_id}/channels` : Fetch guild text channels
- `GET /api/guilds/{guild_id}/roles` : Fetch guild roles
- `GET /api/config/join/{guild_id}` : Load join config
- `POST /api/config/join/{guild_id}` : Save join config
- `GET /api/config/leave/{guild_id}` : Load leave config
- `POST /api/config/leave/{guild_id}` : Save leave config
- `GET /api/config/dm/{guild_id}` : Load DM config
- `POST /api/config/dm/{guild_id}` : Save DM config
- `GET /api/config/role/{guild_id}` : Load auto-role config
- `POST /api/config/role/{guild_id}` : Save auto-role config
- `GET /api/config/levels/{guild_id}` : Load levels config
- `POST /api/config/levels/{guild_id}` : Save levels config
- `GET /api/config/reaction-roles/{guild_id}` : Load reaction role config
- `POST /api/config/reaction-roles/{guild_id}` : Save reaction role config
- `POST /api/publish/reaction-roles/{guild_id}` : Publish reaction role message
- `GET /api/scheduled-announcements/channels/{guild_id}` : Channels for scheduler
- `GET /api/config/scheduled-announcement/{guild_id}` : Load draft scheduled config
- `GET /api/config/scheduled-announcements/{guild_id}` : Load scheduled list
- `POST /api/config/scheduled-announcement/{guild_id}` : Save scheduled draft
- `POST /api/publish/scheduled-announcement/{guild_id}` : Publish scheduled item
- `DELETE /api/config/scheduled-announcement/{guild_id}/{announcement_id}` : Delete item
- `POST /api/roles/create` : Create role in guild
- `POST /api/upload/image` : Upload image to Database/Images
- `GET /api/stats/messages-today/{guild_id}` : Messages count today
- `GET /api/messages/download/{guild_id}` : Start history download
- `GET /api/messages/download/status/{guild_id}` : Download progress
- `GET /api/messages/export/{guild_id}` : Export messages JSON

---



