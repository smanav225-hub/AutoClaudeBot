import discord
from discord import app_commands
from discord.ext import commands

class ProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_profile", {})
        return self.bot._check_perms(interaction, cfg)

    def _progress_bar(self, progress, length=15):
        filled = int(progress * length)
        return "█" * filled + "░" * (length - filled)

    @app_commands.command(name="profile", description="View your or another member's profile")
    @app_commands.describe(user="User to view")
    async def execute(self, interaction: discord.Interaction, user: discord.Member = None):
        if not self._check_enabled(interaction): return
        
        target = user or interaction.user
        await interaction.response.defer()
        
        guild_id = str(interaction.guild_id)
        user_id = str(target.id)
        
        user_data = self.bot.msg_db.get_user_level(guild_id, user_id)
        if not user_data:
            await interaction.followup.send("No profile data found for this user yet.")
            return

        # Fetch Rank and Recent Thanks
        rank = self.bot.msg_db.get_user_rank(guild_id, user_id)
        
        # Safe fetch for recent thanks (might not be implemented yet)
        recent_thanks = []
        try:
            if hasattr(self.bot.msg_db, 'get_recent_thanks'):
                recent_thanks = self.bot.msg_db.get_recent_thanks(guild_id, user_id, limit=5)
        except: pass
        
        # XP Progress Logic
        levels_cfg = self.db.get_config(guild_id, "levels") or {}
        formula = levels_cfg.get("formula", "5 * (level ** 2) + (50 * level) + 100")
        
        level = user_data.get("level", 0)
        xp_current = user_data.get("xp_current", 0)
        xp_needed = self.bot.msg_db._xp_needed(level, formula)
        progress = xp_current / xp_needed if xp_needed > 0 else 0
        
        embed = discord.Embed(color=0xC4A35B)
        embed.set_author(name=target.display_name, icon_url=target.display_avatar.url)
        embed.set_thumbnail(url=target.display_avatar.url)
        
        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="Rank", value=f"#{rank}" if rank else "N/A", inline=True)
        embed.add_field(name="Reputation", value=str(user_data.get("reputation", 0)), inline=True)
        
        progress_text = f"{self._progress_bar(progress)} {int(progress*100)}%\n{xp_current:,} / {xp_needed:,} XP"
        embed.add_field(name="XP Progress", value=progress_text, inline=False)
        
        embed.add_field(name="Total XP", value=f"{user_data.get('xp_total', 0):,}", inline=True)
        embed.add_field(name="Messages", value=f"{user_data.get('messages_total', 0):,}", inline=True)

        if recent_thanks:
            thanks_list = []
            for t in recent_thanks:
                giver_id = t.get('giver_id')
                if not giver_id: continue
                giver = interaction.guild.get_member(int(giver_id))
                giver_name = giver.display_name if giver else f"<@{giver_id}>"
                reason_text = f" — {t['reason']}" if t.get('reason') else ""
                thanks_list.append(f"**{giver_name}**{reason_text}")
            if thanks_list:
                embed.add_field(name="Recent Thanks", value="\n".join(thanks_list), inline=False)

        embed.set_footer(text=f"ID: {target.id}")
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ProfileCog(bot))
