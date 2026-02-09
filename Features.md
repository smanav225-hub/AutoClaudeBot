# AutoClaude Features & Script Analysis

This document provides a detailed breakdown of the scripts within the `AutoClaude` project, explaining their purpose, features, and UI elements.

## Core System

### `Backend.py`
**Purpose:** The main entry point and API server for the application.
**Features:**
-   **FastAPI Server:** Serves the Web GUI (`GUI.html`) and provides API endpoints (`/api/...`) for the frontend to interact with the bot's settings and database.
-   **Bot Initialization:** Initializes and starts all specialized bot clients (Reaction Roles, Leveling, Logging, etc.) as background tasks.
-   **Database Management:** Connects to both `Database.py` (JSON) and `Message_Database.py` (SQLite).
-   **API Endpoints:**
    -   Server management (select, get channels/roles).
    -   Configuration saving/loading for all modules (Welcome, Leave, Levels, etc.).
    -   Image uploading.
    -   Message history downloading and exporting.
    -   Settings management (Tokens, toggles).

### `Database.py`
**Purpose:** Manages the JSON-based configuration database (`data.db`).
**Features:**
-   **Settings Storage:** Stores global settings (Tokens, "Hi" emoji toggle).
-   **Server Configs:** Stores per-server configurations for:
    -   Welcome/Goodbye messages.
    -   DM Welcomes.
    -   Auto-roles.
    -   Leveling settings.
    -   Reaction Roles.
    -   Scheduled Announcements.
-   **Data Persistence:** methods to save and load data to/from `data.db`.

### `Message_Database.py`
**Purpose:** Manages the SQLite database (`Message_Database.db`) for high-volume data.
**Features:**
-   **Message Logging:** Logs every message sent in the server (Content, User, Timestamp, Attachments, etc.).
-   **XP System:** Calculates and tracks user XP and Levels based on message activity.
-   **Data Analysis:** Provides methods to query message counts, word counts, and user rankings for leaderboards.
-   **History Download:** Handles the background task of scraping channel history to populate the database.

### `Start.py`
**Purpose:** The launcher script for the application.
**Features:**
-   **Process Management:** Starts the `Backend.py` process.
-   **Browser Launch:** Automatically opens the Web GUI (`http://localhost:port`) in the default web browser.
-   **Port Management:** Finds a free port to run the server on.

### `folder_metrics.py`
**Purpose:** A utility script for project analysis.
**Features:**
-   **Code Statistics:** Scans the project directory to count total lines of code, characters, and tokens across Python, JavaScript, and HTML files.
-   **Import Analysis:** Identifies and lists unique imports and dependencies used in the project.
-   **File Size Calculation:** Computes the total size of the project files.

---

## Graphical User Interface (GUI) (`AutoClaude/GUI/`)

This section details the web-based interface pages and their associated logic.

### `Welcome_Goodbye.html`
**Purpose:** Configuration page for welcome and goodbye messages, private messages, and auto-roles.
**Features & Modes:**
-   **Lazy Loading:** Features sections (Join, Leave, DM, Role) lazy load their content only when expanded to improve performance.
-   **Global State Management:** Uses a `state` object to track changes across all sub-components and a dirty check system to show a "Save Changes" bar.
-   **Components:**
    -   **Join Server (`Join_Server.js`):**
        -   **Modes:** Text, Embed, Card.
        -   **Text Mode:** Simple textarea with variable placeholders (e.g., `{user}`, `{server}`).
        -   **Embed Mode:** Full rich embed builder with color picker, author, title, description, image/thumbnail uploads, and footer.
        -   **Card Mode:** Custom "Welcome Card" designer with background image upload, font selection, text color pickers, and overlay opacity slider. Live preview updates instantly.
    -   **Join Private Message (`Join_Private_message.js`):**
        -   Identical feature set to Join Server but configures Direct Messages sent to new users.
        -   Supports Text, Embed, and Card modes.
    -   **Join Role (`Join_Role.js`):**
        -   **Role Selection:** Searchable dropdown to select multiple roles to assign on join.
        -   **Role Creation:** Interface to create new roles directly from the UI with color selection.
    -   **Leave Server (`Leave_Server.js`):**
        -   **Mode:** Text only.
        -   Configures the message sent to a channel when a user leaves.

### `Reaction_Roles.html`
**Purpose:** Advanced builder for creating messages that assign roles upon reaction.
**Features:**
-   **Modes:**
    -   **Default:** React to add role, un-react to remove.
    -   **Reverse:** React to remove role, un-react to add.
-   **Message Builder (`Message.js`):**
    -   **Embed Editor:** Rich embed builder similar to Welcome/Goodbye but specific for reaction role prompts.
    -   **Image Handling:** Supports uploading and previewing Header, Thumbnail, Main, and Footer images.
-   **Reaction Logic (`Reaction_And_Roles.js`):**
    -   **Interaction Types:**
        -   **Emoji:** Standard reaction buttons. Includes an emoji picker.
        -   **Dropdown:** Creates a Discord Select Menu component.
    -   **Dynamic Rows:** Add/remove multiple emoji-role pairs or dropdown options.
    -   **Role Selector:** Searchable dropdown to link roles to specific reactions or options.

### `Level.html`
**Purpose:** Dashboard for the leveling and XP system.
**Features:**
-   **XP Settings:**
    -   **Rate Slider:** Adjust global XP gain multiplier (0.5x - 10x).
    -   **Cooldown:** Set time interval between XP gains to prevent spam.
    -   **Range:** Define min/max XP earned per valid message.
-   **Role Rewards:**
    -   **Dynamic List:** Add levels and associate them with roles to be automatically granted.
    -   **Logic:** Option to remove previous reward roles upon leveling up.
-   **Announcements:**
    -   **Toggle:** Enable/disable level-up messages.
    -   **Custom Message:** Text area with variables (`{level}`, `{user}`).
    -   **Modes:** Switch between a simple Text Message or a graphical "Rank Card" preview.
-   **No-XP Zones:**
    -   **Channels/Roles:** Multi-select dropdowns to blacklist specific channels or roles from earning XP.
-   **Database Manager (`Message_Database.js`):**
    -   **Modal Interface:** Pop-up for managing historical data.
    -   **Download History:** Triggers the background task to scrape channel history and populate the database for retro-active leveling.
    -   **Status Tracking:** Real-time progress bar for message downloading and processing.

### `Scheduled_Announcement.html`
**Purpose:** Tool for scheduling future messages.
**Features:**
-   **Scheduler:**
    -   **Date Picker:** Custom calendar UI for selecting the date.
    -   **Time Picker:** Scrollable inputs for Hour/Minute/Second.
    -   **Countdown:** Live countdown timer showing time remaining until the post.
-   **Message Builder (`Message.js`):**
    -   **Tabs:** Switch between Text, Welcome Card (reused asset generator), and Embed modes.
    -   **Reuse:** Leverages the same rich embed and card building logic as other pages for consistency.
-   **Management:**
    -   **List View:** Shows all pending and sent announcements.
    -   **Edit/Delete:** Options to modify pending posts or remove them.

### `Setting.html`
**Purpose:** Global bot configuration.
**Features:**
-   **Token Management:** Secure input for the Discord Bot Token.
-   **"Hi" Emoji:** Toggle and emoji picker to configure the auto-reaction feature for greetings.

### `Commands.html`
**Purpose:** Management interface for slash commands.
**Features:**
-   **Command Cards:** Individual cards for `/analytics`, `/github`, `/level`, and `/leaderboard`.
-   **Permission System:**
    -   **Toggle:** Enable/disable each command globally.
    -   **Role Restrictions:** Multi-select dropdown to restrict command usage to specific roles (e.g., Admins, Mods).

### `Leaderboard.html`
**Purpose:** Placeholder/Info page for the Leaderboard feature.
**Features:**
-   **Informational:** Currently displays instructions on how to use the `/leaderboard` slash command in Discord, as the actual leaderboard UI is rendered within Discord itself via the `Leaderboard_Command.py` logic.

---

## Core Modules (`AutoClaude/Core/`)

### `Commands.py`
**Purpose:** A unified bot client handling slash commands.
**Features:**
-   **Slash Commands:**
    -   `/analytics member`: Shows a breakdown of members by role with visual indicators.
    -   `/github`: Search and download files from the AutoClaude repository directly in Discord.
    -   `/level`: Displays the user's Rank Card.
    -   `/leaderboard`: Opens the interactive Leaderboard Query Builder.
-   **GitHub Integration:** Caches and searches the GitHub repository tree.
-   **Dynamic Help:** (Implicit in command descriptions).

### `Leaderboard_Command.py`
**Purpose:** Contains the UI logic for the advanced Leaderboard command.
**Elements:**
-   **Interactive View (`LeaderboardQueryView`):** A persistent message with UI controls.
-   **Dropdowns:**
    -   `MetricsMultiSelect`: Select multiple metrics (Messages, XP, Words, etc.).
    -   `TimeRangeSelect`: Select time period (Today, Week, All Time, Custom).
    -   `ColumnDisplaySelect`: Choose which columns to show in the results.
    -   `OutputFormatSelect`: Choose between Embed, Table (Code block), or Simple List.
-   **Buttons:**
    -   Sort Toggle (ASC/DESC).
    -   Limit Button (Open Modal).
    -   Submit/Cancel.
-   **Modals:**
    -   `DatePickerModal`: Input start/end dates for custom ranges.
    -   `ResultsLimitModal`: Input exact number of results to show.

### `Level.py`
**Purpose:** Handles the leveling and experience system.
**Features:**
-   **XP Calculation:** specific formulas (default quadratic) to calculate XP gain per message.
-   **Cooldowns:** Prevents spam-farming XP.
-   **Level Up Events:**
    -   **Announcements:** Sends a message or a **Rank Card** when a user levels up.
    -   **Role Rewards:** Automatically adds/removes roles upon reaching specific levels.
-   **Exclusions:** checks for "No-XP" channels or roles.

### `Reaction_Roles.py`
**Purpose:** Manages reaction-based role assignment.
**Features:**
-   **Reaction Handling:** Listens for raw reaction add/remove events.
-   **Modes:**
    -   `Default`: React to add, remove to remove.
    -   `Reverse`: React to remove, remove to add.
-   **UI Elements:**
    -   **Dropdowns:** Supports creating messages with Discord Select Menus for role selection (defined in config).
    -   **Buttons/Embeds:** Publishes configured messages with embeds and optional images.

### `scheduled_announcements.py`
**Purpose:** Manages scheduled tasks.
**Features:**
-   **Task Polling:** regularly checks for due announcements.
-   **Message Types:**
    -   **Text:** Simple text messages.
    -   **Embed:** Rich embeds with titles, descriptions, and images.
    -   **Card:** Generates a custom image card (similar to welcome cards) using PIL.
-   **Placeholders:** Replaces `{user}`, `{date}`, `{server}`, etc., with actual values.

### `Setting.py` (`HiEmojiReactor`)
**Purpose:** A simple fun feature.
**Features:**
-   **Auto-React:** Detects "hi" or "hello" in messages and reacts with a configured emoji (default 👋).

### `Welcome_Goodbye.py`
**Purpose:** Handles member join and leave events.
**Features:**
-   **Welcome Messages:**
    -   **Text:** Standard customizable text.
    -   **Embed:** Rich embed with user details.
    -   **Card:** Generates a custom "Welcome Card" image with user avatar and server stats.
-   **Goodbye Messages:** Notifies when a user leaves.
-   **DM Welcome:** Sends a welcome message/card directly to the user's DMs.
-   **Auto-Role:** Automatically assigns specific roles to new members.

---

## Testing & Utilities (`AutoClaude/Testing/`)

These scripts are standalone components used for development, testing, or specific utility functions.

-   **`Analytics.py`**: A standalone bot for the `/analytics member` command.
    -   *Elements:* Slash commands, text response formatting.
-   **`Command.py`**: Tests token replacement logic (e.g., `{user}`, `{server}`) by sending test messages to "welcome" channels.
-   **`dropdown_role.py`**: A test script for **Dropdown Reaction Roles**.
    -   *Elements:* `discord.ui.Select` (Multiselect), Embeds with attachments.
-   **`Embed_test.py`**: Sends a hardcoded sample **Welcome Embed** to test layout and assets.
-   **`get_server_info.py`**: Dumps server hierarchy (Channels, Roles) to the console.
-   **`Github.py`**: A standalone bot implementing the GitHub search/download commands.
-   **`Github2.py`**: A utility script to fetch and print GitHub Contributors and Sponsors.
-   **`Leaderboard.py`, `Leaderboard1.py`, `Leaderboard2.py`**: Iterations of the Leaderboard bot.
    -   `Leaderboard2.py` is the most advanced, featuring the full **Query Builder UI** (Dropdowns, Modals, Buttons) and SQLite integration.
-   **`reaction_emoji.py`**: Tests standard **Emoji Reaction Roles** (Toggle logic).
-   **`send_hello.py`**: Simple bot connection test (Sends "hello" to welcome channels).
-   **`test_download.py`**: A utility to scrape message history and count stats per channel, validating `Message_Database` logic.
-   **`Welcome_card.py`**: Standalone script to generate and send a **Modern Welcome Card** image using `PIL` (Python Imaging Library).