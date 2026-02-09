import os
import sys
import time
from datetime import datetime, timedelta
import sqlite3

import discord
from discord import app_commands
from discord.ui import View, Select, Button, Modal, TextInput

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from Message_Database import MessageDBHandler
    from Database import Database
except Exception:
    sys.path.append(os.getcwd())
    from Message_Database import MessageDBHandler
    from Database import Database


_MSG_DB = None


def _get_msg_db():
    global _MSG_DB
    if _MSG_DB is None:
        _MSG_DB = MessageDBHandler()
    return _MSG_DB


def get_bot_token() -> str:
    db = Database()
    if db.token:
        return db.token
    token_paths = [
        os.path.join(BASE_DIR, "Token.txt"),
        os.path.join(os.getcwd(), "Token.txt"),
        "Token.txt",
    ]
    for path in token_paths:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    content = f.read()
                    if 'token = "' in content:
                        return content.split('token = "')[1].split('"')[0]
                    return content.strip().replace("token = ", "").replace('"', "")
            except Exception:
                continue
    return ""


METRIC_OPTIONS = [
    ("Total Messages", "total_messages", "💬"),
    ("Total XP", "total_xp", "⭐"),
    ("Level", "level", "📈"),
    ("Words Typed", "words_typed", "📝"),
    ("Images Sent", "images_sent", "🖼️"),
    ("Links Shared", "links_shared", "🔗"),
    ("Emojis Used", "emojis_used", "😄"),
    ("Activity Score", "activity_score", "🔥"),
    ("Reactions Received", "reactions_received", "👍"),
    ("Mentions Received", "mentions_received", "👥"),
]

TIME_OPTIONS = [
    ("All Time", "all", "♾️"),
    ("Today", "today", "📅"),
    ("Last 7 Days", "week", "📊"),
    ("Last 30 Days", "month", "🗓️"),
    ("This Month", "this_month", "🗓️"),
    ("This Year", "year", "📆"),
    ("Custom Range", "custom", "⚙️"),
]

DISPLAY_COLUMNS = [
    ("Rank", "rank"),
    ("Username", "username"),
    ("Total Messages", "total_messages"),
    ("Total XP", "total_xp"),
    ("Level", "level"),
    ("Words Typed", "words_typed"),
    ("Images Sent", "images_sent"),
    ("Links Shared", "links_shared"),
    ("Emojis Used", "emojis_used"),
    ("Reactions Received", "reactions_received"),
    ("Mentions Received", "mentions_received"),
    ("Activity Score", "activity_score"),
]

MESSAGE_METRICS = {
    "total_messages",
    "words_typed",
    "images_sent",
    "links_shared",
    "emojis_used",
    "reactions_received",
    "mentions_received",
}

USERLEVEL_METRICS = {"total_xp", "level", "total_messages", "words_typed"}


def _format_user_tag(username, discrim):
    if discrim and discrim != "0":
        return f"{username}#{discrim}"
    return username or "Unknown"


def _compute_activity_score(row):
    score = 0
    score += int(row.get("total_messages", 0) or 0)
    score += int(row.get("words_typed", 0) or 0) / 10
    score += int(row.get("images_sent", 0) or 0) * 2
    score += int(row.get("links_shared", 0) or 0) * 2
    score += int(row.get("emojis_used", 0) or 0) * 0.5
    score += int(row.get("mentions_received", 0) or 0) * 2
    score += int(row.get("reactions_received", 0) or 0) * 2
    score += int(row.get("total_xp", 0) or 0) / 25
    score += int(row.get("level", 0) or 0) * 5
    return int(score)


class MetricsMultiSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, value=value, emoji=emoji)
            for label, value, emoji in METRIC_OPTIONS
        ]
        super().__init__(
            placeholder="Select metrics (at least 1)...",
            min_values=1,
            max_values=len(options),
            options=options,
            custom_id="metrics_select",
            row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_metrics = self.values
        for opt in self.options:
            opt.default = opt.value in self.view.selected_metrics
        await self.view.update_summary(interaction)


class TimeRangeSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, value=value, emoji=emoji)
            for label, value, emoji in TIME_OPTIONS
        ]
        super().__init__(
            placeholder="Select one time range...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="timerange_select",
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_time = self.values[0]
        for opt in self.options:
            opt.default = opt.value == self.view.selected_time
        if self.view.selected_time == "custom":
            await interaction.response.send_modal(DatePickerModal(self.view))
        else:
            await self.view.update_summary(interaction)


class ColumnDisplaySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=label, value=value, default=value in {"rank", "username", "total_messages"})
            for label, value in DISPLAY_COLUMNS
        ]
        super().__init__(
            placeholder="Select columns to show...",
            min_values=1,
            max_values=8,
            options=options,
            custom_id="column_select",
            row=2,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.display_columns = self.values
        for opt in self.options:
            opt.default = opt.value in self.view.display_columns
        await self.view.update_summary(interaction)


class OutputFormatSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Embed (Fancy)", value="embed", emoji="✨"),
            discord.SelectOption(label="Table (Text)", value="table", emoji="📋"),
            discord.SelectOption(label="List (Simple)", value="list", emoji="📝"),
        ]
        super().__init__(
            placeholder="Choose output format...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="format_select",
            row=3,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.output_format = self.values[0]
        for opt in self.options:
            opt.default = opt.value == self.view.output_format
        await self.view.update_summary(interaction)


class DatePickerModal(Modal, title="Custom Date Range"):
    start_date = TextInput(
        label="Start Date (YYYY-MM-DD)",
        placeholder="2024-01-01",
        required=True,
        min_length=10,
        max_length=10,
    )
    end_date = TextInput(
        label="End Date (YYYY-MM-DD or today)",
        placeholder="today",
        required=True,
        min_length=5,
        max_length=10,
    )

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            start_str = self.start_date.value.strip()
            end_str = self.end_date.value.strip()

            if start_str.lower() == "today":
                start_dt = datetime.now()
            else:
                start_dt = datetime.strptime(start_str, "%Y-%m-%d")

            if end_str.lower() == "today":
                end_dt = datetime.now()
            else:
                end_dt = datetime.strptime(end_str, "%Y-%m-%d")

            if start_dt >= end_dt:
                await interaction.response.send_message("❌ Start date must be before end date.", ephemeral=True)
                return

            self.parent_view.custom_start_date = start_dt
            self.parent_view.custom_end_date = end_dt
            await self.parent_view.update_summary(interaction)
        except Exception:
            await interaction.response.send_message("❌ Invalid date format. Use YYYY-MM-DD.", ephemeral=True)


class ResultsLimitModal(Modal, title="Set Results Limit"):
    limit = TextInput(
        label="Number of results (1-500)",
        placeholder="50",
        default="50",
        required=True,
        min_length=1,
        max_length=3,
    )

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            limit_val = int(self.limit.value)
            if limit_val < 1 or limit_val > 500:
                await interaction.response.send_message("❌ Must be between 1 and 500.", ephemeral=True)
                return
            self.parent_view.results_limit = limit_val
            await self.parent_view.update_summary(interaction)
        except Exception:
            await interaction.response.send_message("❌ Invalid number.", ephemeral=True)


class LeaderboardQueryView(View):
    def __init__(self, guild_id):
        super().__init__(timeout=600)
        self.guild_id = str(guild_id)
        self.db = None
        self.message = None

        self.selected_metrics = ["total_messages"]
        self.display_columns = ["rank", "username", "total_messages"]
        self.selected_time = "all"
        self.custom_start_date = None
        self.custom_end_date = None
        self.results_limit = 50
        self.sort_direction = "desc"
        self.output_format = "embed"

        self.add_item(MetricsMultiSelect())
        self.add_item(TimeRangeSelect())
        self.add_item(ColumnDisplaySelect())
        self.add_item(OutputFormatSelect())

    async def update_summary(self, interaction: discord.Interaction = None):
        embed = None
        if interaction and interaction.message and interaction.message.embeds:
            embed = interaction.message.embeds[0]
        elif self.message and self.message.embeds:
            embed = self.message.embeds[0]

        if embed:
            embed.description = build_ui_text(self)
            if interaction and not interaction.response.is_done():
                await interaction.response.edit_message(embed=embed, view=self)
            elif self.message:
                await self.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Sort: DESC", style=discord.ButtonStyle.secondary, emoji="📉", row=4)
    async def toggle_sort(self, interaction: discord.Interaction, button: Button):
        if self.sort_direction == "desc":
            self.sort_direction = "asc"
            button.label = "Sort: ASC"
            button.emoji = "📈"
        else:
            self.sort_direction = "desc"
            button.label = "Sort: DESC"
            button.emoji = "📉"
        await self.update_summary(interaction)

    @discord.ui.button(label="Limit", style=discord.ButtonStyle.secondary, emoji="🔢", row=4)
    async def set_limit(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ResultsLimitModal(self))

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.success, emoji="✅", row=4)
    async def submit(self, interaction: discord.Interaction, button: Button):
        if not self.selected_metrics:
            await interaction.response.send_message("❌ Select at least one metric!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        results, note = await self.execute_query()
        await self.display_results(interaction, results, note)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="❌", row=4)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="Query cancelled.", embed=None, view=None)
        self.stop()

    async def execute_query(self):
        if self.db is None:
            self.db = _get_msg_db()
        time_mode = self.selected_time
        now = datetime.now()
        start_ts = 0
        end_ts = time.time()
        if time_mode == "today":
            start_ts = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        elif time_mode == "week":
            start_ts = (now - timedelta(days=7)).timestamp()
        elif time_mode == "month":
            start_ts = (now - timedelta(days=30)).timestamp()
        elif time_mode == "this_month":
            start_ts = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        elif time_mode == "year":
            start_ts = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        elif time_mode == "custom" and self.custom_start_date:
            start_ts = self.custom_start_date.timestamp()
            if self.custom_end_date:
                end_ts = self.custom_end_date.timestamp()

        selected = set(self.selected_metrics)
        wants_message_metrics = time_mode != "all" or any(m in MESSAGE_METRICS for m in selected)
        wants_userlevel = any(m in USERLEVEL_METRICS for m in selected) or any(
            c in USERLEVEL_METRICS for c in self.display_columns
        )

        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        base = {}

        if time_mode == "all":
            cur.execute(
                """
                SELECT user_id, username, user_discriminator,
                       messages_total as total_messages,
                       words_total as words_typed,
                       xp_total as total_xp,
                       level
                FROM user_levels
                WHERE guild_id=?
                """,
                (self.guild_id,),
            )
            for row in cur.fetchall():
                r = dict(row)
                user_id = str(r.get("user_id"))
                base[user_id] = {
                    "user_id": user_id,
                    "username": r.get("username") or "Unknown",
                    "user_discriminator": r.get("user_discriminator"),
                    "total_messages": int(r.get("total_messages", 0) or 0),
                    "words_typed": int(r.get("words_typed", 0) or 0),
                    "total_xp": int(r.get("total_xp", 0) or 0),
                    "level": int(r.get("level", 0) or 0),
                }

        if wants_message_metrics:
            if time_mode == "all":
                cur.execute(
                    """
                    SELECT user_id, username, user_discriminator,
                           COUNT(*) as total_messages,
                           SUM(word_count) as words_typed,
                           SUM(image_count) as images_sent,
                           SUM(links_count) as links_shared,
                           SUM(emoji_count) as emojis_used,
                           SUM(total_reactions_received) as reactions_received,
                           SUM(mentioned_count) as mentions_received
                    FROM messages
                    WHERE guild_id=? AND is_deleted=0
                    GROUP BY user_id
                    """,
                    (self.guild_id,),
                )
            else:
                cur.execute(
                    """
                    SELECT user_id, username, user_discriminator,
                           COUNT(*) as total_messages,
                           SUM(word_count) as words_typed,
                           SUM(image_count) as images_sent,
                           SUM(links_count) as links_shared,
                           SUM(emoji_count) as emojis_used,
                           SUM(total_reactions_received) as reactions_received,
                           SUM(mentioned_count) as mentions_received
                    FROM messages
                    WHERE guild_id=? AND created_at >= ? AND created_at <= ? AND is_deleted=0
                    GROUP BY user_id
                    """,
                    (self.guild_id, start_ts, end_ts),
                )

            for row in cur.fetchall():
                r = dict(row)
                user_id = str(r.get("user_id"))
                entry = base.get(user_id) or {
                    "user_id": user_id,
                    "username": r.get("username") or "Unknown",
                    "user_discriminator": r.get("user_discriminator"),
                    "total_xp": 0,
                    "level": 0,
                }
                entry["total_messages"] = int(r.get("total_messages", 0) or 0)
                entry["words_typed"] = int(r.get("words_typed", 0) or 0)
                entry["images_sent"] = int(r.get("images_sent", 0) or 0)
                entry["links_shared"] = int(r.get("links_shared", 0) or 0)
                entry["emojis_used"] = int(r.get("emojis_used", 0) or 0)
                entry["reactions_received"] = int(r.get("reactions_received", 0) or 0)
                entry["mentions_received"] = int(r.get("mentions_received", 0) or 0)
                base[user_id] = entry

        note = None
        if time_mode != "all" and wants_userlevel:
            cur.execute(
                """
                SELECT user_id, username, user_discriminator, xp_total, level
                FROM user_levels
                WHERE guild_id=?
                """,
                (self.guild_id,),
            )
            for row in cur.fetchall():
                r = dict(row)
                user_id = str(r.get("user_id"))
                entry = base.get(user_id)
                if not entry:
                    entry = {
                        "user_id": user_id,
                        "username": r.get("username") or "Unknown",
                        "user_discriminator": r.get("user_discriminator"),
                        "total_messages": 0,
                        "words_typed": 0,
                    }
                entry["total_xp"] = int(r.get("xp_total", 0) or 0)
                entry["level"] = int(r.get("level", 0) or 0)
                base[user_id] = entry
            note = "XP and Level are all-time values."

        conn.close()

        values = list(base.values())
        if not values:
            return [], note

        for v in values:
            v["user"] = _format_user_tag(v.get("username"), v.get("user_discriminator"))
            v["activity_score"] = _compute_activity_score(v)

        selected_metrics = self.selected_metrics or ["total_messages"]
        max_vals = {}
        for m in selected_metrics:
            max_vals[m] = max([v.get(m, 0) or 0 for v in values]) if values else 0

        for v in values:
            if len(selected_metrics) == 1:
                v["_score"] = v.get(selected_metrics[0], 0) or 0
            else:
                scores = []
                for m in selected_metrics:
                    mv = max_vals.get(m, 0)
                    scores.append((v.get(m, 0) or 0) / mv if mv > 0 else 0)
                v["_score"] = sum(scores) / len(scores)

        values.sort(key=lambda x: x["_score"], reverse=self.sort_direction == "desc")

        final_results = []
        for idx, v in enumerate(values[: int(self.results_limit)], 1):
            v["rank"] = idx
            final_results.append(v)

        return final_results, note

    async def display_results(self, interaction: discord.Interaction, results, note: str = None):
        if not results:
            await interaction.edit_original_response(content="No data found for this period.", embed=None, view=None)
            return

        if self.output_format == "embed":
            await self.display_embed(interaction, results, note)
        elif self.output_format == "table":
            await self.display_table(interaction, results, note)
        else:
            await self.display_list(interaction, results, note)

    async def display_embed(self, interaction: discord.Interaction, results, note: str = None):
        metric_text = ", ".join([m.replace("_", " ").title() for m in self.selected_metrics])
        time_text = self.selected_time.replace("_", " ").title()
        if self.selected_time == "custom" and self.custom_start_date and self.custom_end_date:
            time_text = f"Custom ({self.custom_start_date:%b %d, %Y} - {self.custom_end_date:%b %d, %Y})"

        embed = discord.Embed(
            title=f"📊 Leaderboard: Top {len(results)}",
            description=f"Metrics: {metric_text}\nTime: {time_text}",
            color=discord.Color.blurple(),
        )
        for r in results[:10]:
            medal = ["🥇", "🥈", "🥉"][r["rank"] - 1] if r["rank"] <= 3 else f"{r['rank']}."
            details = []
            for col in self.display_columns:
                if col in {"rank", "username"}:
                    continue
                label = col.replace("_", " ").title()
                details.append(f"**{label}:** {r.get(col, 0)}")
            embed.add_field(name=f"{medal} {r['user']}", value="\n".join(details) or "Active", inline=False)

        footer_parts = [f"Sort: {self.sort_direction.upper()}"]
        if note:
            footer_parts.append(note)
        embed.set_footer(text=" | ".join(footer_parts))

        channel = interaction.channel
        if channel:
            await channel.send(embed=embed)
        await interaction.edit_original_response(content="✅ Leaderboard posted publicly.", embed=None, view=None)

    async def display_table(self, interaction: discord.Interaction, results, note: str = None):
        header_map = {
            "rank": "#",
            "username": "User",
            "total_messages": "Msgs",
            "total_xp": "XP",
            "level": "Lvl",
            "words_typed": "Words",
            "images_sent": "Imgs",
            "links_shared": "Links",
            "emojis_used": "Emoj",
            "reactions_received": "React",
            "mentions_received": "Mentn",
            "activity_score": "Score",
        }
        col_widths = {
            "rank": 4,
            "username": 12,
            "total_messages": 6,
            "total_xp": 6,
            "level": 4,
            "words_typed": 7,
            "images_sent": 5,
            "links_shared": 5,
            "emojis_used": 5,
            "reactions_received": 5,
            "mentions_received": 5,
            "activity_score": 6,
        }

        cols = self.display_columns
        headers = [f"{header_map.get(c, c[:4]):<{col_widths.get(c, 6)}}" for c in cols]
        lines = [" ".join(headers), "-" * (sum(col_widths.get(c, 6) for c in cols) + len(cols) - 1)]

        for r in results:
            row = []
            for c in cols:
                val = str(r.get(c, 0))
                if c == "username":
                    val = val[: col_widths.get(c, 12)]
                row.append(f"{val:<{col_widths.get(c, 6)}}")
            lines.append(" ".join(row))

        content = "```\n" + "\n".join(lines[:25]) + "\n```"
        if len(lines) > 25:
            content += f"\n+ {len(lines) - 25} more results..."
        if note:
            content += f"\nNote: {note}"

        channel = interaction.channel
        if channel:
            await channel.send(content=content[:2000])
        await interaction.edit_original_response(content="✅ Leaderboard posted publicly.", embed=None, view=None)

    async def display_list(self, interaction: discord.Interaction, results, note: str = None):
        lines = [f"📊 **Leaderboard ({self.selected_time.replace('_',' ').title()})**", ""]
        for r in results[:30]:
            medal = "🏆" if r["rank"] == 1 else "🥈" if r["rank"] == 2 else "🥉" if r["rank"] == 3 else f"{r['rank']}."
            primary = self.selected_metrics[0]
            primary_label = primary.replace("_", " ").title()
            lines.append(f"{medal} **{r['user']}** — {r.get(primary, 0)} {primary_label}")
        if len(results) > 30:
            lines.append(f"...and {len(results) - 30} more.")
        if note:
            lines.append(f"Note: {note}")

        channel = interaction.channel
        if channel:
            await channel.send("\n".join(lines)[:2000])
        await interaction.edit_original_response(content="✅ Leaderboard posted publicly.", embed=None, view=None)


def build_ui_text(view: LeaderboardQueryView) -> str:
    def mark_multi(selected, key):
        return "☑" if key in selected else "☐"

    def mark_one(selected, key):
        return "◉" if selected == key else "○"

    metrics_lines = []
    for i in range(0, len(METRIC_OPTIONS), 2):
        left = METRIC_OPTIONS[i]
        right = METRIC_OPTIONS[i + 1] if i + 1 < len(METRIC_OPTIONS) else None
        left_text = f"{mark_multi(view.selected_metrics, left[1])} {left[0]}"
        right_text = f"{mark_multi(view.selected_metrics, right[1])} {right[0]}" if right else ""
        metrics_lines.append(f"  {left_text:<26} {right_text}")

    time_lines = []
    for i in range(0, len(TIME_OPTIONS), 2):
        left = TIME_OPTIONS[i]
        right = TIME_OPTIONS[i + 1] if i + 1 < len(TIME_OPTIONS) else None
        left_text = f"{mark_one(view.selected_time, left[1])} {left[0]}"
        right_text = f"{mark_one(view.selected_time, right[1])} {right[0]}" if right else ""
        time_lines.append(f"  {left_text:<24} {right_text}")

    metrics_text = ", ".join([m.replace("_", " ").title() for m in view.selected_metrics])
    time_text = view.selected_time.replace("_", " ").title()
    if view.selected_time == "custom" and view.custom_start_date and view.custom_end_date:
        time_text = f"Custom ({view.custom_start_date:%b %d, %Y} - {view.custom_end_date:%b %d, %Y})"

    custom_range = "Only visible for Custom Range"
    if view.selected_time == "custom":
        custom_range = f"Start: {view.custom_start_date:%b %d, %Y} | End: {view.custom_end_date:%b %d, %Y}"

    out = (
        "📊 **LEADERBOARD QUERY BUILDER**\n\n"
        "**PRIMARY METRICS (Multi-select)**\n"
        + "\n".join(metrics_lines)
        + f"\nSelected: {metrics_text}\n\n"
        "**TIME RANGE (Single-select)**\n"
        + "\n".join(time_lines)
        + f"\nSelected: {time_text}\n\n"
        f"**CUSTOM DATE RANGE**\n  {custom_range}\n\n"
        f"**RESULTS LIMIT:** {view.results_limit}\n"
        f"**SORT:** {view.sort_direction.upper()}\n"
        f"**DISPLAY COLUMNS:** {', '.join([c.replace('_',' ').title() for c in view.display_columns])}\n"
        f"**OUTPUT FORMAT:** {view.output_format.title()}\n"
    )
    return out


class LeaderboardBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        @self.tree.command(name="leaderboard", description="Query the leaderboard with custom filters")
        async def leaderboard_command(interaction: discord.Interaction):
            view = LeaderboardQueryView(interaction.guild_id)
            embed = discord.Embed(title="📊 Leaderboard Query Builder", color=discord.Color.blurple())
            embed.description = build_ui_text(view)
            try:
                if interaction.response.is_done():
                    view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                    try:
                        view.message = await interaction.original_response()
                    except Exception:
                        view.message = None
            except (discord.NotFound, discord.HTTPException):
                return
            try:
                view.message = await interaction.original_response()
            except Exception:
                view.message = None

        await self.tree.sync()


if __name__ == "__main__":
    token = get_bot_token()
    if not token:
        print("Token not found.")
        raise SystemExit(1)
    client = LeaderboardBot()
    client.run(token)
