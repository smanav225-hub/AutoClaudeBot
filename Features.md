# 🌟 AutoClaude Pro Features & Complete Module Breakdown

---

## 🛡️ Advanced AI Moderation System

**Files:** `Core/Moderation_Pro.py`, `Core/Command/Moderation.py`, `Core/Command/Punishment.py`  
**GUI:** `Moderation_Pro.html`  
**API:** `/api/pro/moderation/{guild_id}/rules`, `/api/pro/moderation/{guild_id}/triage`

**Key Features:**
- DeepSeek-powered toxicity analysis and intent detection
- Dynamic blocklist: banned words, regex patterns, link filters
- Comprehensive violation audit trail: Display Names, @handles, timestamps, user IDs, full message content
- Automated actions: Delete, Warn, Discord timeout
- Rule add/remove interface
- AI Triage test box: paste message → see AI action

---

## 📊 Interaction Intelligence (Network Graph)

**Files:** `Core/Network_Pro.py`  
**GUI:** `Network_Graph.html`  
**API:** `/api/pro/network/{guild_id}`

**Features:**
- D3.js physics-based graph: user nodes + interaction edges
- Edge types: Replies, Mentions, Thanks
- Interactive controls: drag nodes, zoom, filter edges
- Strongest connections sidebar
- Community cluster identification

---

## 📈 Server Health & Growth Analytics

**Files:** `Core/Health_Metrics.py`, `Core/Lifecycle_Pro.py`  
**GUI:** `Health_Analytics.html`  
**API:** `/api/pro/health/{guild_id}?hours=168`

**Metrics:**
- Message volume & velocity
- Peak active user counts
- XP distribution and gains
- New member growth rate
- Reputation point flow

**Data:** Hourly automated rollups, 24h/7d/30d views, Chart.js graphs

---

## 🏆 Ranking Pro (Advanced Leaderboards)

**Files:** `Core/Leaderboard_Pro.py`, `Core/Command/Leaderboard_Command.py`, `Core/Command/Leaderboard_Post.py`  
**GUI:** `Leaderboard_Pro.html`, `Leaderboard.html`  
**API:** `/api/pro/leaderboard/{guild_id}`

**Features:**
- Time slicing: Daily, Weekly, Monthly, All-Time
- Metrics: XP, Messages, Streaks, Voice Minutes
- Live search by username
- Top 3 podium: Cyan/Blue/Violet styling
- Interactive Query Builder UI

---

## 👤 Profile Pro (Member Intelligence)

**Files:** `Core/Profile_Pro.py`, `Core/Command/Profile.py`  
**GUI:** `Profile_Pro.html`  
**API:** `/api/pro/profile/{guild_id}/{user_id}`, `/api/pro/profile/{guild_id}/search`

**Features:**
- Identity: avatar, Discord ID, join date, roles
- 42-day activity heatmap (GitHub style)
- Achievement badge gallery
- Stats: Rank, Level, XP, Reputation, Streaks
- Live member search

---

## 📊 XP & Leveling System (MEE6 Style)

**Files:** `Core/Level.py`, `Core/Command/Xp.py`, `Core/Command/Level_Rewards.py`, `Core/Command/Achievements.py`  
**GUI:** `Level.html`  
**Features:**
- XP gain on messages with cooldown prevention
- Customizable multiplier (0.5x-10x)
- Min/Max XP per message
- Role rewards at specific levels
- Level-up announcements with Rank Card preview
- No-XP zones: blacklist channels/roles
- Historical message import (retroactive XP)
- Badge/achievement system

---

## 🎭 Welcome & Goodbye System

**Files:** `Core/Welcome_Goodbye.py`  
**GUI:** `Welcome_Goodbye.html`  
**Sub-components:**
- `Join_Server.js`: Text/Embed/Card modes
- `Join_Private_message.js`: DM welcome (3 modes)
- `Join_Role.js`: Searchable role multi-select, create roles
- `Leave_Server.js`: Goodbye message

**Features:**
- Card designer with image upload + overlay
- Variable placeholders: `{user}`, `{server}`, `{role}`
- Embed builder: color picker, title, description, footer
- Auto-role assignment on join
- DM welcome cards with custom styling

---

## ⚙️ Reaction Roles System

**Files:** `Core/Reaction_Roles.py`  
**GUI:** `Reaction_Roles.html`  
**Sub-components:**
- `Message.js`: Embed editor, image handler
- `Reaction_And_Roles.js`: Emoji/dropdown logic

**Modes:**
- Default: React to add role
- Reverse: React to remove role
- Emoji picker with custom reactions
- Discord Select Menu dropdowns
- Dynamic add/remove rows

---

## 📅 Scheduled Announcements System

**Files:** `Core/scheduled_announcements.py`  
**GUI:** `Scheduled_Announcement.html`  
**Features:**
- Date picker (calendar UI)
- Time picker (scrollable hour/minute/second)
- Live countdown timer
- Message types: Text, Embed, Card
- Placeholder support: `{user}`, `{date}`, `{server}`
- List view: pending/sent announcements
- Edit/Delete management
- Cron-based delivery

---

## 🔥 Activity Streaks

**Integration:** `on_message` handler in `Level.py`  
**Features:**
- Real-time streak increment on message send
- Timezone-aware midnight reset
- Leaderboard metric ranking
- Profile heatmap integration

---

## 🕒 Automated Lifecycle (Cron Jobs)

**File:** `Core/Lifecycle_Pro.py`  
**Tasks:**
- Auto-Unbans (every 60s): Check expired punishments
- Hourly Health Rollups (every hour at :05): Analytics snapshots
- Midnight Resets (timezone-aware): Weekly/Monthly XP resets

---

## 🔍 GitHub Integration

**Files:** `Core/Commands.py`, `Core/Command/Search.py`  
**Commands:**
- `/search [query]` - DuckDuckGo web search with embeds
- `/github` - Access AutoClaude repo files in Discord

---

## ⌨️ All 30+ Slash Commands

### Moderation (Core/Command/)
1. `/moderation add` - Add safety rule
2. `/moderation remove` - Remove rule
3. `/moderation list` - List rules
4. `/punish ban` - Ban user
5. `/punish kick` - Kick user
6. `/punish warn` - Warn user
7. `/punish mute` - Timeout user

### Leveling
8. `/xp rank` - User rank/XP
9. `/xp leaderboard` - Top users
10. `/xp add` - Admin: add XP
11. `/xp remove` - Admin: remove XP
12. `/quests list` - Daily challenges
13. `/quests claim` - Claim reward
14. `/achievements` - Badge gallery
15. `/thank [user]` - Give reputation
16. `/level-reward set` - Set milestone role
17. `/level-reward remove` - Remove milestone
18. `/level-reward list` - List milestones

### Utility & Search
19. `/search [query]` - **[PRO]** Web search
20. `/ping` - Latency check
21. `/help` - Command menu
22. `/help-admin` - Admin menu
23. `/poll create` - Create poll
24. `/poll close` - Close poll
25. `/profile [user]` - Member profile

### System & Roles
26. `/ticket open` - Create support ticket
27. `/ticket close` - Close ticket
28. `/ticket setup` - Configure tickets
29. `/autorole set` - Set auto-role
30. `/autorole remove` - Remove auto-role
31. `/role add` - Add role to user
32. `/role remove` - Remove role
33. `/role list` - List assignable roles
34. `/role-config add` - Admin: add self-role
35. `/role-config remove` - Admin: remove self-role
36. `/afk set` - Set away status
37. `/afk clear` - Clear away status

### Events & Misc
38. `/events list` - Upcoming events
39. `/event create` - Create event
40. `/event cancel` - Cancel event
41. `/leaderboard` - Query builder
42. `/backup export` - Export config
43. `/backup import` - Import config
44. `/health-check` - Force rollup check
45. `/reputation [set|view]` - Rep config

---

## 🎨 Color & Design System

**Pure Black Theme:**
- Background: #000000
- Cards: #0A0A0A (border #1A1A1A)
- Primary: Neon Cyan (#00F2FF)
- Secondary: Slate Gray (#94A3B8)
- Glassmorphism: `backdrop-filter: blur(20px); background: rgba(10, 10, 10, 0.7)`

---

## 📊 API Endpoints (Complete)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/pro/health/{guild_id}` | GET | Server metrics |
| `/api/pro/leaderboard/{guild_id}` | GET | Rankings |
| `/api/pro/moderation/{guild_id}/rules` | GET/POST | Rules |
| `/api/pro/moderation/{guild_id}/rules/{rule_id}` | DELETE | Remove rule |
| `/api/pro/moderation/{guild_id}/triage` | POST | Test message |
| `/api/pro/network/{guild_id}` | GET | Social graph |
| `/api/pro/profile/{guild_id}/{user_id}` | GET | Member profile |
| `/api/pro/profile/{guild_id}/search` | GET | Member search |
| `/api/config/*` | POST | Feature config |
| `/api/settings/*` | POST | Global settings |
| `/api/guilds/{guild_id}/select` | GET | Server selection |

---

*Complete breakdown of AutoClaude Pro's 30+ commands and intelligent features.*
