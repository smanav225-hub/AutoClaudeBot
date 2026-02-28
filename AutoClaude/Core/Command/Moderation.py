import discord
from discord import app_commands
from discord.ext import commands
import re

class ModerationCog(commands.GroupCog, group_name="moderation", group_description="Manage content moderation rules"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_moderation", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="add", description="Add a moderation rule")
    @app_commands.describe(
        type="Rule type (regex, blocklist, link_filter)",
        pattern="The pattern to match",
        action="Action to take (delete, warn)",
        reason="Reason for this rule"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="Regex", value="regex"),
        app_commands.Choice(name="Blocklist", value="blocklist"),
        app_commands.Choice(name="Link Filter", value="link_filter")
    ])
    @app_commands.choices(action=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Warn", value="warn")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, 
                  type: str, pattern: str, action: str = "delete", reason: str = "Rule violation"):
        if not self._check_enabled(interaction): return
        
        # Synchronous implementation in Message_Database.py
        self.bot.msg_db.add_mod_rule(interaction.guild_id, type, pattern, action, reason, interaction.user.id)
        await interaction.response.send_message(f"✅ Rule added: **{type}** — `{pattern}` (action: {action})", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a moderation rule by ID")
    @app_commands.describe(rule_id="The ID of the rule to remove")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove(self, interaction: discord.Interaction, rule_id: int):
        if not self._check_enabled(interaction): return
        
        self.bot.msg_db.remove_mod_rule(rule_id, interaction.guild_id)
        await interaction.response.send_message(f"✅ Rule #{rule_id} removed.", ephemeral=True)

    @app_commands.command(name="list", description="List all moderation rules")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def list(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        rules = self.bot.msg_db.get_mod_rules(interaction.guild_id)
        if not rules:
            await interaction.response.send_message("No moderation rules configured.", ephemeral=True)
            return
            
        lines = [f"**#{r['id']}** [{r['type']}] `{r['pattern']}` → {r['action']}" for r in rules]
        embed = discord.Embed(title="🛡️ Moderation Rules", description="\n".join(lines), color=0xC4A35B)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
            
        # Check if moderation is enabled
        cfg = self.db.get_settings().get("commands_moderation", {})
        if not cfg.get("enabled", False):
            return

        if not hasattr(self.bot, "moderation_pro_service") or not self.bot.moderation_pro_service:
            return

        # Perform AI Triage (checks rules + toxicity)
        result = self.bot.moderation_pro_service.triage_message(
            guild_id=str(message.guild.id),
            content=message.content,
            user_id=str(message.author.id),
            message_id=str(message.id),
            actor_id=str(self.bot.user.id),
            username=message.author.display_name,
            metadata={
                "author_tag": str(message.author), # e.g. User#1234 or user
                "channel_name": message.channel.name if hasattr(message.channel, "name") else "Unknown"
            }
        )

        action = result.get("action", "allow")
        reason = result.get("reason", "Rule violation")
        
        if action == "allow":
            return

        print(f"[Moderation] Action '{action}' triggered for {message.author}: {reason}")

        if action == "delete":
            try:
                await message.delete()
                # Optionally notify the user
                await message.channel.send(f"⚠️ {message.author.mention}, your message was removed. Reason: {reason}", delete_after=10)
            except Exception as e:
                print(f"[Moderation] Failed to delete message: {e}")
        
        elif action == "warn":
            await message.channel.send(f"⚠️ {message.author.mention}, please follow server rules. (Reason: {reason})", delete_after=15)
        
        elif action in ["mute", "timeout"]:
            # Basic timeout implementation if bot has permissions (defaulting to 10 mins if not specified)
            try:
                import datetime
                duration = datetime.timedelta(minutes=10)
                await message.author.timeout(duration, reason=reason)
                await message.delete()
                await message.channel.send(f"🔇 {message.author.mention} has been muted for 10 minutes. Reason: {reason}")
            except Exception as e:
                print(f"[Moderation] Failed to timeout user: {e}")
                # Fallback to delete
                try: await message.delete()
                except: pass


async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
