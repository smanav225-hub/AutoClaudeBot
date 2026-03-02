import discord
from discord import app_commands
from discord.ext import commands

import json
import io

class BackupCog(commands.GroupCog, group_name="backup", group_description="Export or import guild settings"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        # We use a broader permission check for backup
        return interaction.user.guild_permissions.manage_guild

    @app_commands.command(name="export", description="Export guild settings as a JSON file")
    async def export_settings(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        # Get all config for this server
        server_data = self.db.data.get("servers", {}).get(guild_id, {})
        
        json_str = json.dumps(server_data, indent=4)
        file = discord.File(io.BytesIO(json_str.encode('utf-8')), filename=f"guild-settings-{guild_id}.json")
        
        embed = discord.Embed(
            title="📥 Settings Exported",
            description="Your guild settings have been exported. Keep this file safe!",
            color=0xC4A35B
        )
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)

    @app_commands.command(name="import", description="Import guild settings from a JSON file")
    @app_commands.describe(file="The JSON file to import")
    async def import_settings(self, interaction: discord.Interaction, file: discord.Attachment):
        if not file.filename.endswith(".json"):
            await interaction.response.send_message("❌ Please upload a valid `.json` file.", ephemeral=True)
            return
            
        await interaction.response.defer(ephemeral=True)
        
        try:
            content = await file.read()
            data = json.loads(content)
            
            # Very basic validation: it should be a dict
            if not isinstance(data, dict):
                await interaction.followup.send("❌ Invalid backup file format.", ephemeral=True)
                return
                
            guild_id = str(interaction.guild_id)
            # Merge or overwrite? The TS version seems to overwrite/apply keys
            for key, value in data.items():
                self.db.save_config(guild_id, key, value)
                
            embed = discord.Embed(
                title="📤 Settings Imported",
                description=f"Successfully applied settings from backup.",
                color=0xC4A35B
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except json.JSONDecodeError:
            await interaction.followup.send("❌ Failed to parse JSON file.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(BackupCog(bot))
