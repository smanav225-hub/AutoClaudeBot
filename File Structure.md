# 📁 AutoClaude Complete Project Structure & Architecture

AutoClaude is a comprehensive Discord server management and intelligence suite with 50+ scripts across Core services, Slash commands, Web GUI, and utilities.

---

# 🌟 Features Overview

## 🛡️ Advanced Moderation & Safety

### AI-Powered Moderation System
- **AI Triage System**: DeepSeek-powered analysis to rate message toxicity and intent
- **Dynamic Blocklist**: Real-time enforcement of banned words, regex patterns, and link filters
- **Violation Logging**: Comprehensive audit trail capturing Display Names, @handles, Full Message Content, and Timestamps
- **Automated Actions**: Configurable responses including warnings, message deletion, and native Discord timeouts

### Moderation Commands
- `/moderation add` - Add safety rule
- `/moderation remove` - Remove rule
- `/moderation list` - List all active rules
- `/punish ban` - Ban user from server
- `/punish kick` - Kick user from server
- `/punish warn` - Warn user with violation record
- `/punish mute` - Apply timeout to user

---

## 📊 Server Intelligence & Analytics

### Interaction Intelligence (Network Graph)
- **D3.js Visualization**: Interactive, physics-based spider-web graph of server social dynamics
- **Connection Tracking**: Maps every Reply, Mention, and "Thank" to visualize community clusters
- **Connection Strength**: Highlights the strongest interaction pairs in the server
- **Real-time Interaction**: Nodes can be dragged and zoomed to explore the social fabric

### Server Health & Growth Analytics
- **Visual Trends**: Multi-chart dashboard using Chart.js tracking server health over 24h, 7d, and 30d
- **Key Metrics**: Monitor message volume, peak active users, XP distribution, and new member growth
- **Hourly Rollups**: Automated background tasks capture data snapshots every hour for precise reporting
- `/health-check` - Force rollup check and update analytics

---

## 🏆 Ranking & Leaderboards

### Ranking Pro (Advanced Leaderboards)
- **Time-Sliced Rankings**: Switch between Daily, Weekly, Monthly, and All-Time leaderboards
- **Multi-Metric Support**: Rank users by XP, Total Messages, Activity Streaks, or Voice Minutes
- **Live Search**: Quickly find any member's position in global or local rankings
- **Visual Hierarchy**: Modern UI highlighting top performers with custom podium styles
- **Interactive Query Builder**: Dropdowns for metrics, time ranges, column display, and output formats
- **Multiple Output Formats**: Embed, Table (Code block), or Simple List views

### Leaderboard Commands
- `/xp leaderboard` - View top users by XP
- `/leaderboard` - Advanced query builder for custom rankings
- `/leaderboard-post` - Automated periodic leaderboard posting

---

## 👤 Profile & Member Intelligence

### Profile Pro (Member Intelligence)
- **Identity Cards**: Sleek profiles showing avatars, join dates, and unique IDs
- **Activity Heatmap**: 42-day message intensity grid (GitHub-style) to track individual engagement
- **Badge System**: Visual gallery of earned server achievements and Pro status
- **Gamification**: Real-time display of XP progress bars, streaks, and reputation scores

### Profile Commands
- `/profile [user]` - View detailed member profile with stats and badges
- `/achievements` - View personal badge gallery and earned achievements
- `/thank [user]` - Give reputation points to another user

---

## ⭐ Leveling & Experience System

### XP & Ranking System
- **Configurable XP Rates**: Adjust global XP gain multiplier (0.5x - 10x)
- **Anti-Spam Cooldown**: Set time intervals between XP gains to prevent farming
- **Dynamic Range**: Define min/max XP earned per valid message
- **No-XP Zones**: Blacklist specific channels or roles from earning XP
- **Level-Up Events**: Automatic announcements and role rewards at milestones
- **Rank Cards**: Beautiful graphical rank cards generated on level-up

### Role Rewards System
- Automatically grant roles at specific level thresholds
- Remove previous reward roles upon leveling up
- Configurable milestone rewards

### Leveling Commands
- `/xp rank` - Display user's rank and XP progress
- `/xp leaderboard` - View top users by XP
- `/xp add` - Admin: add XP to user
- `/xp remove` - Admin: remove XP from user
- `/quests list` - View available daily challenges
- `/quests claim` - Claim quest rewards
- `/level-reward set` - Set role reward for specific level
- `/level-reward remove` - Remove level reward
- `/level-reward list` - List all configured rewards

---

## 🔔 Welcome, Goodbye & Auto-Roles

### Welcome & Goodbye Messages
- **Multiple Modes**: Text, Embed, or Custom Welcome Card
- **Text Mode**: Simple customizable messages with variable placeholders ({user}, {server}, etc.)
- **Embed Mode**: Full rich embed builder with color picker, author, title, description, images
- **Card Mode**: Custom welcome card designer with background image, fonts, text color, overlay opacity
- **Live Preview**: Instant visual updates while designing
- **DM Welcomes**: Send personalized welcome messages to new members in DMs

### Auto-Role Assignment
- **Searchable Role Selection**: Multi-select dropdown for role assignment
- **Role Creation**: Create new roles directly from the UI with color selection
- **Automatic Assignment**: Assign roles instantly when members join

### Leave Messages
- Notify specific channels when users leave the server
- Customizable leave message format

---

## ⚙️ Reaction Roles & Interactive Messages

### Reaction Role Builder
- **Dual Modes**: Default (react to add) or Reverse (react to remove)
- **Rich Embed Editor**: Full embed customization for role prompts
- **Image Support**: Upload and preview header, thumbnail, main, and footer images

### Interaction Types
- **Emoji Reactions**: Standard reaction buttons with emoji picker
- **Dropdown Menus**: Discord Select Menu components for cleaner role selection
- **Dynamic Rows**: Add/remove multiple emoji-role pairs or dropdown options
- **Role Linking**: Searchable dropdown to link roles to reactions/options

---

## 📅 Scheduled Announcements & Events

### Announcement Scheduler
- **Date & Time Picker**: Custom calendar UI and scrollable time inputs
- **Countdown Timer**: Live countdown showing time remaining until post
- **Multiple Formats**: Text, Welcome Card, or Embed modes
- **Management**: List, edit, and delete pending or sent announcements

### Event Management
- `/events list` - View upcoming server events
- `/event create` - Schedule new server event
- `/event cancel` - Cancel scheduled event

---

## 🎫 Ticket System

### Support Ticket Management
- Create support tickets for member requests
- Organized ticket channels and threads
- Ticket configuration and customization

### Ticket Commands
- `/ticket open` - Create new support ticket
- `/ticket close` - Close and archive ticket
- `/ticket setup` - Configure ticket system settings

---

## 👥 Role Management & Self-Roles

### Role Assignment System
- Assign roles to users with admin commands
- Remove roles from users
- Searchable role lists
- Self-assignable role system

### Role Commands
- `/role add` - Add role to user
- `/role remove` - Remove role from user
- `/role list` - List all assignable roles
- `/role-config add` - Admin: add self-assignable role
- `/role-config remove` - Admin: remove self-assignable role
- `/role-config give` - Give role from self-role system
- `/role-config list` - List self-assignable roles
- `/autorole set` - Set auto-role for new members
- `/autorole remove` - Remove auto-role

---

## 💬 Utility & Communication

### Polls & Voting
- Create custom polls with multiple options
- Real-time voting and results
- Poll management and closing

### Poll Commands
- `/poll create` - Create new poll
- `/poll close` - Close and finalize poll

### Status Management
- Set AFK (Away From Keyboard) status
- Automatic away message responses

### Status Commands
- `/afk set` - Set away status with optional message
- `/afk clear` - Clear away status

### Search & Information
- `/search [query]` - [PRO] DuckDuckGo-powered web search
- `/ping` - Check bot latency and status
- `/help` - View command menu
- `/help-admin` - View admin command menu

---

## 📦 Data & Configuration Management

### Backup & Export
- Export server configuration and settings
- Import configuration from backup
- Full data persistence and recovery

### Configuration Commands
- `/backup export` - Export server config to file
- `/backup import` - Import config from backup
- `/reputation [set|view]` - Configure reputation system

### Utility Tools
- `/giveaway-export` - Export giveaway participant data
- `/health-check` - Force rollup check and diagnostics

---

## 🎨 Web GUI Dashboard

### Pro Feature Pages (5 Advanced Interfaces)

**Health_Analytics.html** - Server Health Dashboard
- Chart.js multi-graph visualization
- 24h/7d/30d timeframe selector
- 5 key metrics: Messages, Users, XP, Growth, Reputation
- Data export capability

**Leaderboard_Pro.html** - Time-Sliced Rankings
- Filter by: All Time/Monthly/Weekly/Daily
- Metrics: XP/Messages/Streaks/Voice Minutes
- Live search functionality
- Top 3 podium visualization

**Moderation_Pro.html** - AI Triage & Rules
- Add/Delete safety rules
- Test messages against AI analyzer
- Recent violations feed
- Blocklist management

**Network_Graph.html** - Social Interaction Mapper
- D3.js interactive physics nodes
- Edge filtering and clustering
- Draggable nodes with zoom/pan
- Connection strength visualization

**Profile_Pro.html** - Member Intelligence
- Identity card (avatar, ID, join date)
- 42-day activity heatmap (GitHub-style)
- Badge gallery and stats grid
- Reputation and achievement showcase

### Standard Feature Pages (9 Interfaces)

**Level.html** - Leveling System Configuration
- XP rate slider (0.5x-10x multiplier)
- Cooldown and min/max XP settings
- Role rewards list manager
- No-XP zones (channels/roles)
- Message history downloader with progress

**Welcome_Goodbye.html** - Join/Leave/DM/Roles
- **Join_Server.js** - Text/Embed/Card modes
- **Join_Private_message.js** - DM welcome (3 modes)
- **Join_Role.js** - Searchable multi-role selector
- **Leave_Server.js** - Goodbye message editor
- Live preview for all formats

**Reaction_Roles.html** - Emoji/Dropdown Roles
- **Message.js** - Embed editor with image uploads
- **Reaction_And_Roles.js** - Emoji/dropdown logic
- Mode: Default/Reverse toggle
- Dynamic add/remove for emoji-role pairs

**Scheduled_Announcement.html** - Announcement Scheduler
- Date picker (calendar interface)
- Time picker (scrollable inputs)
- Live countdown timer
- Text/Card/Embed format support
- List view: pending and sent announcements

**Commands.html** - Command Management
- Command cards for documentation
- Permission toggle per command
- Role restriction dropdown
- Enable/disable commands globally

**Setting.html** - Global Configuration
- Bot token secure input
- "Hi" emoji toggle and picker
- Feature toggles and preferences

**Leaderboard.html** - Leaderboard Info Page
- `/leaderboard` command usage guide
- Query builder UI instructions
- Discord-native interaction documentation

**Moderation.html** - Legacy Moderation Settings
- Moderation rule configuration
- Automated action setup

**TEMPLATE.html** - Template for New Pages
- Base structure for feature development
- Standard component patterns

### GUI Architecture Features
- **Lazy Loading**: Sections load on-demand for performance
- **Global State Management**: Track changes across components
- **Dirty Check System**: Show "Save Changes" bar when needed
- **Rich Text Editors**: Full embed builders with live preview
- **Image Upload**: Integrated image management
- **Permission System**: Toggle commands and role restrictions
- **Real-time Preview**: Instant visual feedback while configuring

---

## 🔧 Backend & Infrastructure

### Core System Architecture
- **FastAPI Server**: High-speed backend serving web GUI and API endpoints
- **Database Management**: Dual-database system (JSON for config, SQLite for analytics)
- **Bot Initialization**: Manages specialized bot clients as background tasks
- **Message Logging**: Logs every server message (content, user, timestamp, attachments)
- **XP Tracking**: Calculates and tracks user XP/levels based on message activity
- **API Endpoints**: 20+ routes for settings, configuration, channel/role management

### Database Features
- **Configuration Storage**: Global settings and per-server configurations
- **Message History**: Background scraping for retroactive leveling
- **Data Analysis**: Query counts, word counts, user rankings
- **Persistence**: Data survives restarts

### Automation
- **Automated Lifecycle**: Cron jobs for auto-unbans, XP resets, health snapshots
- **Background Tasks**: Hourly rollups, message downloading, scheduled announcements
- **Browser Launch**: Automatic GUI opener on startup
- **Port Management**: Finds free port for server

---

# 🤖 Root Directory Files

**Core Application:**
- `Backend.py` - FastAPI web server bridging Discord logic to Web GUI
- `Database.py` - JSON config manager for server settings and tokens
- `Message_Database.py` - SQLite handler for analytics and message logging
- `Start.py` - Main entry point to launch Discord Bot and Web Backend
- `GUI.html` - Main web UI entry point and navigation shell
- `AutoTest.py` - Automated testing suite for core functions
- `VerifyProFixes.py` - Verification suite for Pro features (Streaks, Lifecycle, Cron)
- `folder_metrics.py` - Project analysis utility for code statistics

---

# 🧠 Core Engine (`/Core/`)

### Main Service Modules (11 services)
- **`Commands.py`** - Main bot class and slash command registration
- **`Health_Metrics.py`** - Analytics engine for server growth and activity
- **`Leaderboard_Pro.py`** - Time-sliced ranking (Daily/Weekly/Monthly/All-Time)
- **`Moderation_Pro.py`** - AI triage service with DeepSeek analysis and blocklist
- **`Network_Pro.py`** - Social interaction mapper (replies/mentions/thanks)
- **`Profile_Pro.py`** - Member intelligence with heatmap and badges
- **`Lifecycle_Pro.py`** - Cron jobs for auto-unbans, XP resets, health snapshots
- **`Level.py`** - XP calculation, cooldowns, role rewards
- **`Reaction_Roles.py`** - Emoji/dropdown role assignment
- **`Welcome_Goodbye.py`** - Join/leave events with card generation
- **`scheduled_announcements.py`** - Cron-based announcement delivery
- **`Setting.py`** (HiEmojiReactor) - Auto-react to "hi"/"hello"

### Slash Commands (`/Core/Command/` - 27 commands)

**Moderation (2):**
- `Moderation.py` - `/moderation [add|remove|list]`
- `Punishment.py` - `/punish [ban|kick|warn|mute]`

**Leveling (7):**
- `Xp.py` - `/xp [rank|leaderboard|add|remove]`
- `Quests.py` - `/quests [list|claim]`
- `Achievements.py` - `/achievements`
- `Thank.py` - `/thank [user]`
- `Level_Rewards.py` - `/level-reward [set|remove|list]`

**Utility & Search (6):**
- `Search.py` - `/search [query]` (DuckDuckGo, **PRO**)
- `Help.py` - `/help`
- `Help_Admin.py` - `/help-admin`
- `Ping.py` - `/ping`
- `Poll.py` - `/poll [create|close]`
- `Profile.py` - `/profile [user]`

**System & Roles (8):**
- `Ticket.py` - `/ticket [open|close|list]`
- `Ticket_Setup.py` - `/ticket-setup`
- `Autorole.py` - `/autorole [set|remove]`
- `Role.py` - `/role [add|remove|list]`
- `Role_Config.py` - `/role-config [add|remove|list|give]`

**Events & Info (4):**
- `Event.py` - `/event [create|cancel]`
- `Events.py` - `/events list`
- `Leaderboard_Command.py` - `/leaderboard` (query builder UI)
- `Leaderboard_Post.py` - `/leaderboard-post` (auto-publish)

**Misc & Tools (4):**
- `Afk.py` - `/afk [set|clear]`
- `Backup.py` - `/backup [export|import]`
- `Giveaway_Export.py` - `/giveaway-export`
- `Health_Check.py` - `/health-check`
- `Reputation_Config.py` - `/reputation [set|view]`

---

# 🌐 Web GUI (`/GUI/`)

### Main Dashboard
- **`GUI.html`** - Primary navigation shell with server selection and feature sidebar

### Pro Feature Pages (5)
- **`Health_Analytics.html`** - Chart.js server health dashboard (24h/7d/30d)
- **`Leaderboard_Pro.html`** - Time-sliced rankings with filters and live search
- **`Moderation_Pro.html`** - AI triage and rule management
- **`Network_Graph.html`** - D3.js social interaction visualization
- **`Profile_Pro.html`** - Member intelligence with activity heatmap

### Standard Feature Pages (9)
- **`Commands.html`** - Command documentation and permission management
- **`Level.html`** - XP configuration with rewards and no-XP zones
- **`Leaderboard.html`** - Leaderboard info and command guide
- **`Moderation.html`** - Legacy moderation settings
- **`Reaction_Roles.html`** - Emoji/dropdown role setup
- **`Setting.html`** - Global bot configuration
- **`Welcome_Goodbye.html`** - Join/leave/DM message editor
- **`Scheduled_Announcement.html`** - Announcement scheduler
- **`TEMPLATE.html`** - Base template for new pages

### Sub-Folders with JavaScript
- **`Level/`** - `Message_Database.js` (history download manager)
- **`Reaction_Roles/`** - `Message.js`, `Reaction_And_Roles.js`
- **`Welcome_Goodbye/`** - `Join_Server.js`, `Join_Private_message.js`, `Join_Role.js`, `Leave_Server.js`
- **`Scheduled_Announcement/`** - Announcement scheduling scripts

---

# 🧪 Testing & Utilities (`/Testing/`)

**Bot Implementations (3):**
- `Analytics.py` - `/analytics member` test bot
- `Github.py` - GitHub search/download bot
- `Github2.py` - Contributor/sponsor fetcher

**Feature Tests (11):**
- `Command.py` - Token replacement testing
- `dropdown_role.py` - Dropdown reaction role test
- `Embed_test.py` - Welcome embed validation
- `get_server_info.py` - Server hierarchy dump
- `Leaderboard.py` / `Leaderboard1.py` / `Leaderboard2.py` - Leaderboard iterations
- `reaction_emoji.py` - Emoji reaction role test
- `send_hello.py` - Bot connection test
- `test_download.py` - Message history scraper validator
- `Welcome_card.py` - PIL welcome card generator

---

# 📊 Database Schema

### Database.db (JSON Configuration)
```
root/
├── settings/
│   ├── token (string)
│   └── hi_emoji (string)
└── servers/{guild_id}/
    ├── welcome (config)
    ├── goodbye (config)
    ├── dm_welcome (config)
    ├── auto_roles (array)
    ├── level_config (config)
    ├── reaction_roles (array)
    ├── announcements (array)
    ├── moderation_rules (array)
    ├── ticket_config (config)
    └── command_permissions (object)
```

### Message_Database.db (SQLite Analytics)
```
messages
├── id, guild_id, user_id, channel_id
├── content, timestamp, attachments

xp_records
├── user_id, guild_id, xp, level
├── timestamp

health_rollups
├── guild_id, timestamp
├── message_count, user_count
├── xp_awarded, new_members, reputation_awarded

violations
├── user_id, guild_id, timestamp
├── message_content, action_taken, rule_triggered

interactions
├── from_user_id, to_user_id, guild_id
├── interaction_type (reply/mention/thank)
├── timestamp
```

---

# 🔄 Startup & Architecture Flow

```
Start.py
  ↓
Backend.py (FastAPI initialization)
  ├─→ Database.py connection
  ├─→ Message_Database.py connection
  ├─→ Core/ modules initialization
  └─→ Discord.py bot clients (async)
  ↓
Browser opens GUI.html
  ↓
User selects server (modal)
  ↓
Dashboard loads feature pages from GUI/
  ↓
GUI pages fetch APIs from Backend.py
  ↓
Backend.py executes Core/ logic
  ↓
Databases persist state
  ↓
Discord bot executes features in real-time
```

---

# 🔌 API Route Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `/api/guilds/*` | Server selection/data | `/api/guilds/{id}/select`, `/api/guilds/{id}/channels` |
| `/api/config/*` | Feature configuration | `/api/config/welcome/save`, `/api/config/level/get` |
| `/api/pro/*` | Pro analytics | `/api/pro/health/{id}`, `/api/pro/network/{id}` |
| `/api/upload/*` | Image/file handling | `/api/upload/image` |
| `/api/settings/*` | Global settings | `/api/settings/token` |
| `/api/message-history/*` | Logging/download | `/api/message-history/download` |

---

# 🏗️ Feature Addition Workflow

### Step 1: Create Backend Logic
1. Create `Core/YourFeature.py` with business class
2. Implement Discord event handlers and logic

### Step 2: Create Web Interface
1. Copy `GUI/TEMPLATE.html` → `GUI/YourFeature.html`
2. Build UI with buttons, forms, displays
3. Create `GUI/YourFeature/` folder if complex (add JavaScript)

### Step 3: Wire Backend Endpoints
1. Add routes to `Backend.py`
2. Connect Core logic to HTTP endpoints
3. Handle request/response data

### Step 4: Connect Frontend
1. Add fetch() calls in JavaScript
2. Update `GUI.html` sidebar navigation
3. Implement state management and save/load

### Step 5: Test & Verify
1. Test all buttons and inputs
2. Verify API responses
3. Check database persistence
4. Run `VerifyProFixes.py`

### Step 6: Refactor & Document
1. Ensure `Backend.py` stays clean
2. Move classes to `Core/YourFeature.py`
3. Update documentation

---

# 📈 Performance & Scale

- **SQLite**: 1000+ messages/sec
- **Leaderboards**: Cached hourly
- **Network Graph**: Async, cached results
- **Health Analytics**: Rolled up hourly
- **API Response**: <100ms average

---

# 🔐 Security & Data

- **Token**: Encrypted in Database.py, never exposed
- **Backups**: Automated via `/backup export`
- **Privacy**: Messages only for analytics
- **Tampering**: Admin-only XP commands
- **Rate Limiting**: Planned for future releases

---

# 📝 File Naming Convention

- **GUI Files**: `FeatureName.html`
- **Core Services**: `FeatureName.py`
- **Slash Commands**: `/Core/Command/CommandName.py`
- **Sub-Scripts**: `GUI/FeatureName/FeatureName_SubModule.js`

---

# ⌨️ Complete Command Reference (30+ Commands)

**Moderation (7):** `/moderation add` • `/moderation remove` • `/moderation list` • `/punish ban` • `/punish kick` • `/punish warn` • `/punish mute`

**Leveling (11):** `/xp rank` • `/xp leaderboard` • `/xp add` • `/xp remove` • `/quests list` • `/quests claim` • `/achievements` • `/thank` • `/level-reward set` • `/level-reward remove` • `/level-reward list`

**Utility (6):** `/search` • `/ping` • `/help` • `/help-admin` • `/poll create` • `/poll close` • `/profile`

**System (8):** `/ticket open` • `/ticket close` • `/ticket setup` • `/autorole set` • `/autorole remove` • `/role add` • `/role remove` • `/role list` • `/role-config add` • `/role-config remove`

**Events (4):** `/events list` • `/event create` • `/event cancel` • `/leaderboard` • `/leaderboard-post`

**Config (4):** `/backup export` • `/backup import` • `/health-check` • `/reputation` • `/afk set` • `/afk clear`

---

*Last Updated: February 28, 2026*
*Total Scripts: 50+ | Features: 30+ | Database Tables: 5 | API Routes: 20+*
