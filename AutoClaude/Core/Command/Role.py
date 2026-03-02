import discord
from discord import app_commands
from discord.ext import commands

class RoleCog(commands.GroupCog, group_name="role", group_description="Self-assign roles"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(name="list", description="List available self-assignable roles")
    async def list_roles(self, interaction: discord.Interaction):
        try:
            role_ids = self.bot.msg_db.get_self_assignable_roles(str(interaction.guild_id))
            if not role_ids:
                await interaction.response.send_message(
                    "No self-assignable roles configured yet.\n"
                    "Ask an admin to use `/role-config add` to add some.",
                    ephemeral=True
                )
                return
            roles = []
            for rid in role_ids:
                r = interaction.guild.get_role(int(rid))
                roles.append(r.mention if r else f"Unknown({rid})")
            await interaction.response.send_message(f"**Available roles:** {', '.join(roles)}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="add", description="Add a role to yourself")
    @app_commands.describe(role="Role to add")
    async def add_role(self, interaction: discord.Interaction, role: discord.Role):
        try:
            role_ids = self.bot.msg_db.get_self_assignable_roles(str(interaction.guild_id))
            if str(role.id) not in role_ids:
                await interaction.response.send_message(
                    f"❌ **{role.name}** is not self-assignable.\n"
                    f"Use `/role list` to see what's available.",
                    ephemeral=True
                )
                return
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Added {role.mention} to you!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to add that role.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a role from yourself")
    @app_commands.describe(role="Role to remove")
    async def remove_role(self, interaction: discord.Interaction, role: discord.Role):
        try:
            role_ids = self.bot.msg_db.get_self_assignable_roles(str(interaction.guild_id))
            if str(role.id) not in role_ids:
                await interaction.response.send_message(
                    f"❌ **{role.name}** is not self-assignable.",
                    ephemeral=True
                )
                return
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"✅ Removed {role.mention} from you.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to remove that role.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleCog(bot))
