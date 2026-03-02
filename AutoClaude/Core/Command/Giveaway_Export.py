import discord
from discord import app_commands
from discord.ext import commands

import io

class Giveaway_ExportCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_giveaway_export", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="giveaway-export", description="Export guild user data as CSV for giveaways")
    @app_commands.describe(
        limit="Max users to export (default 100)",
        exclude_role="Exclude members with this role",
        exclude_role_2="Exclude members with this role too"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def execute(self, interaction: discord.Interaction, 
                      limit: int = 100, 
                      exclude_role: discord.Role = None, 
                      exclude_role_2: discord.Role = None):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        
        exclude_ids = set()
        if exclude_role or exclude_role_2:
            # Fetch members if needed
            if interaction.guild.chunked == False:
                await interaction.guild.fetch_members().flatten()
            
            for role in [exclude_role, exclude_role_2]:
                if role:
                    for member in role.members:
                        exclude_ids.add(member.id)
                        
        csv_content, count = await self.bot.msg_db.export_users_csv(interaction.guild_id, list(exclude_ids), limit)
        
        file = discord.File(
            io.BytesIO(csv_content.encode('utf-8')), 
            filename=f"giveaway-export-{interaction.guild_id}.csv"
        )
        
        await interaction.followup.send(f"✅ Exported {count} users.", file=file, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway_ExportCog(bot))
