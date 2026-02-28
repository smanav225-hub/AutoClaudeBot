import discord
from discord import app_commands
from discord.ext import commands

class AfkCog(commands.GroupCog, group_name="afk", group_description="Set an AFK status to notify others when you are away"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db
        self.afk_users = {}  # In-memory store: (guild_id, user_id) -> message
        
    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_afk", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="set", description="Set yourself as AFK")
    @app_commands.describe(message="Your AFK message")
    async def set_afk(self, interaction: discord.Interaction, message: str):
        if not self._check_enabled(interaction): return
        
        guild_id = interaction.guild_id
        user_id = interaction.user.id
        self.afk_users[(guild_id, user_id)] = message
        
        await interaction.response.send_message(f"You are now AFK: **{message}**", ephemeral=True)

    @app_commands.command(name="clear", description="Clear your AFK status")
    async def clear_afk(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        guild_id = interaction.guild_id
        user_id = interaction.user.id
        
        if (guild_id, user_id) in self.afk_users:
            del self.afk_users[(guild_id, user_id)]
            await interaction.response.send_message("Welcome back! Your AFK status has been cleared.", ephemeral=True)
        else:
            await interaction.response.send_message("You are not currently AFK.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild: return
        
        guild_id = message.guild.id
        user_id = message.author.id
        
        # 1. Clear AFK if the user speaks
        if (guild_id, user_id) in self.afk_users:
            del self.afk_users[(guild_id, user_id)]
            try:
                await message.reply(f"Welcome back {message.author.mention}! Your AFK status has been removed.")
            except: pass
            
        # 2. Notify if mentioning an AFK user
        for mention in message.mentions:
            if (guild_id, mention.id) in self.afk_users:
                afk_msg = self.afk_users[(guild_id, mention.id)]
                try:
                    await message.reply(f"**{mention.display_name}** is currently AFK: {afk_msg}")
                except: pass

async def setup(bot: commands.Bot):
    await bot.add_cog(AfkCog(bot))
