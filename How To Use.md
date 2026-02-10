# How to Use AutoClaudeBot

This file explains how to **set up**, **start**, and **use all features** of AutoClaudeBot.

---

## Adding Your Discord Token

1. Open the `AutoClaudeBot` folder  
2. Go inside the `AutoClaude` folder  
3. Click on `Start.py`

4. Once the browser opens:
   - Click on **Settings** in the left sidebar
   - Inside Settings, click on the **Token** entry box
   - Paste your **Discord token**
   - Click on **Save**

5. Now:
   - Close the browser tab
   - Close the CMD / Terminal window that opened with the website

6. Click on `Start.py` **again**

Your token is now saved.

---

## How to Start Using the App

Once you restart the app:

- The app is ready to use
- You can choose any settings or customizations
- All changes are saved automatically

---

## Recommended (Backup Previous Messages)

It is recommended to back up your previous server messages before using features like Levels.

Steps:

1. Click on **Levels (+ Enable)**  
2. Inside Levels, click on the **Database** button (top of the screen)
3. Click on **Download All Previous Messages**
4. Wait for the process to complete

Once done, the app is fully ready.

---

## Welcome & Goodbye Feature

### Welcome Message (Server)

You can send a message when a user joins the server.

You can:
- Select a channel
- Choose message type:
  - Text message
  - Welcome card
  - Embed message

---

### Welcome Private Message (DM)

You can also send a private message to the user when they join.

You can choose:
- Text message
- Welcome card
- Embed message

This message will be sent in the user's private chat.

---

### Auto Role on Join

You can automatically give roles to new users.

Steps:
- Select one or multiple roles
- When a user joins the server, those roles will be given automatically

---

### Goodbye Message

You can send a message when a user leaves the server.

Steps:
- Select a channel
- Type your goodbye message

That message will be sent when a user leaves the server.

---

## Levels System

### Enable XP System

To start giving XP to players:

- Select **XP Multiplier**  
  (Used to increase XP during server events)

- Select **Message Cooldown**  
  (Usually 60 seconds)

- Select **Random XP per Message**  
  (Default: 15–25 XP)

---

### Role Rewards

Enable or disable the following options:

- ✅ Enable role rewards  
- ✅ Remove previous role on level up  

To add role rewards:

1. Click on **Add Reward**
2. Enter the level number
3. Select the role

Example:
- Level: 5
- Role: Level 5 Role

When a player reaches level 5, they will automatically receive that role.

You can add multiple rewards.

---

### Level Up Announcements

To enable level-up announcements:

- Toggle **Send level-up announcements**
- Select an **Announcement Channel**
- Choose output type:
  - Text message
  - Rank card

Whenever a user levels up, the announcement will appear in the selected channel.

---

### No XP Zone

You can block XP in specific places.

You can:
- Select channels where no XP is given
- Select roles that will not receive any XP

Multiple channels and roles can be selected.

---

## Commands System

There are **4 commands** available:

- `/analytics`
- `/github`
- `/level`
- `/leaderboard`

For each command:
- You can enable or disable it using a checkbox
- You can restrict usage to specific roles
- Only users with allowed roles can use that command

---

### `/analytics`

Shows:
- List of all roles in the server
- Sponsors (if any)
- Number of members in each role

---

### `/github`

Access files inside the AutoClaudeBot GitHub repository.

Features:
- Browse files and folders
- Select images or files
- Images are sent directly into Discord
- Files can be downloaded

---

### `/level`

Shows:
- Your level
- Your XP
- Your rank

---

### `/leaderboard`

Advanced leaderboard system.

You can select:

**Primary Metrics (Multi-select):**
- Total Messages
- Total XP
- Level
- Words Typed
- Images Sent
- Links Shared
- Emojis Used
- Activity Score
- Reactions Received
- Mentions Received

**Time Range:**
- All Time
- Today
- Last 7 Days
- Last 30 Days
- This Month
- This Year
- Custom Range

**Other Options:**
- Ascending or Descending order
- Number of users to display
- Output format:
  - Embed
  - Table
  - List
- Select which columns to display (name, XP, level, etc.)

---

## Reaction Roles

Steps:

1. Select a channel
2. Write your embed message (images supported)
3. Select reaction mode:
   - Emoji reaction
   - Dropdown selection
4. Assign roles to reactions

Reaction Modes:
- **Emoji**: User clicks emoji to get role
- **Dropdown**: User selects role from dropdown menu

---

## Scheduled Announcements

Steps:

1. Select a channel
2. Select date and time
3. Choose output format:
   - Text message
   - Welcome card
   - Embed
4. Click **Post**

The announcement will be sent at the scheduled time.

---

## Special Features

AutoClaudeBot remembers the last state you left it in.

This includes:
- Toggles
- Entry box text
- Text boxes
- Dropdown selections
- Saved settings

Everything will remain exactly the same when you reopen the app.

---

Happy using AutoClaudeBot 🚀
