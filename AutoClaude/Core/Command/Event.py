import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
import time

class EventCog(commands.GroupCog, group_name="event", group_description="Create and manage server events"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_event", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="create", description="Schedule a new event (use 24h time in YOUR local timezone)")
    @app_commands.describe(
        title="Event title",
        date="Date (YYYY-MM-DD) e.g. 2026-03-01",
        time_str="Time in 24h format e.g. 18:30 (6:30 PM)",
        channel="Channel to post in",
        description="Event description",
        reminder="Send reminder X minutes before"
    )
    @app_commands.checks.has_permissions(manage_events=True)
    async def create(self, interaction: discord.Interaction, 
                     title: str, date: str, time_str: str, channel: discord.TextChannel, 
                     description: str = None, reminder: int = None):
        if not self._check_enabled(interaction): return
        
        try:
            scheduled_at = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
            ts = scheduled_at.timestamp()  # Converts using system local timezone
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid date or time format.\n"
                "• Date should be `YYYY-MM-DD` e.g. `2026-03-01`\n"
                "• Time should be `HH:MM` in 24h format e.g. `18:30` for 6:30 PM",
                ephemeral=True
            )
            return
            
        if ts <= time.time():
            await interaction.response.send_message(
                f"❌ That time is in the past!\n"
                f"• You entered: **{date} {time_str}** (local time)\n"
                f"• Discord shows that as: <t:{int(ts)}:F>\n"
                f"• Current time is: <t:{int(time.time())}:F>\n\n"
                f"**Tip:** Use 24-hour format. For example, 6:30 PM = `18:30`",
                ephemeral=True
            )
            return
            
        event_id = self.bot.msg_db.create_event(
            interaction.guild_id, channel.id, interaction.user.id, 
            title, description, ts, reminder
        )
        
        await interaction.response.send_message(
            f"✅ Event **#{event_id}** scheduled: **{title}**\n"
            f"📅 When: <t:{int(ts)}:F>\n"
            f"📢 Channel: {channel.mention}" + 
            (f"\n⏰ Reminder: {reminder} min before" if reminder else ""),
            ephemeral=True
        )

    @app_commands.command(name="cancel", description="Cancel a scheduled event")
    @app_commands.describe(event_id="The ID of the event to cancel")
    @app_commands.checks.has_permissions(manage_events=True)
    async def cancel(self, interaction: discord.Interaction, event_id: int):
        if not self._check_enabled(interaction): return
        
        self.bot.msg_db.cancel_event(event_id, interaction.guild_id)
        await interaction.response.send_message(f"✅ Event **#{event_id}** cancelled.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(EventCog(bot))
