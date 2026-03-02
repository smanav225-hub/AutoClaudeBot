import discord
from discord import app_commands
from discord.ext import commands

class ThankCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_thank", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="thank", description="Thank a user to give them a reputation point")
    @app_commands.describe(user="The user you want to thank", reason="Optional reason for thanking")
    async def execute(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        if user.id == interaction.user.id:
            await interaction.response.send_message("❌ You cannot thank yourself!", ephemeral=True)
            return
            
        if user.bot:
            await interaction.response.send_message("❌ You cannot thank bots!", ephemeral=True)
            return

        try:
            # Get server specific config for reputation
            rep_cfg = self.db.get_config(str(interaction.guild_id), "reputation") or {}
            daily_cap = rep_cfg.get("daily_cap", 5)
            reciprocal_window = rep_cfg.get("reciprocal_window", 24)

            # 1. Daily Cap Check
            today_count = self.bot.msg_db.get_reputation_count_today(interaction.guild_id, interaction.user.id)
            if today_count >= daily_cap:
                await interaction.response.send_message(f"❌ You've reached your daily thank limit of {daily_cap}.", ephemeral=True)
                return

            # 2. Reciprocal Check
            if self.bot.msg_db.check_reciprocal_reputation(interaction.guild_id, interaction.user.id, user.id, reciprocal_window):
                await interaction.response.send_message("❌ Reciprocal cooldown! You cannot thank each other too frequently.", ephemeral=True)
                return

            # 3. Process Thank
            self.bot.msg_db.add_reputation_event(interaction.guild_id, interaction.user.id, user.id, reason)
            new_rep = self.bot.msg_db.get_user_reputation(interaction.guild_id, user.id)
            
            embed = discord.Embed(
                title="✨ Reputation Awarded!",
                description=f"{interaction.user.mention} thanked {user.mention}!",
                color=discord.Color.gold()
            )
            if reason:
                embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"{user.display_name} now has {new_rep} reputation point(s).")
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ThankCog(bot))
