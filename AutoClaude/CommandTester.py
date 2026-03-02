import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import unittest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import os
import sys
import json
import time
from datetime import datetime

# Add paths to sys.path so we can import from Core
sys.path.append(os.path.join(os.getcwd(), "Core"))
sys.path.append(os.getcwd())

from Database import Database
from Message_Database import MessageDBHandler
from Core.Commands import IntegratedCommandBot

class MockInteraction(AsyncMock):
    def __init__(self, user_id=1001, guild_id=123456789, channel_id=999, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = MagicMock(spec=discord.Member)
        self.user.id = user_id
        self.user.name = "Tester"
        self.user.mention = f"<@{user_id}>"
        self.user.roles = []
        self.user.display_avatar = MagicMock()
        self.user.display_avatar.url = "https://example.com/avatar.png"
        self.user.guild_permissions = discord.Permissions(administrator=True)
        
        self.guild = MagicMock(spec=discord.Guild)
        self.guild.id = guild_id
        self.guild.name = "Test Guild"
        self.guild.members = [self.user]
        self.guild.roles = []
        self.guild.premium_subscriber_role = None
        self.guild.premium_subscribers = []
        self.guild.me = MagicMock(spec=discord.Member)
        self.guild.me.top_role = MagicMock(spec=discord.Role)
        self.guild.me.top_role.position = 999
        
        self.guild.get_member = MagicMock(return_value=self.user)
        self.guild.get_role = MagicMock(return_value=MagicMock(spec=discord.Role))
        self.guild.get_channel = MagicMock(return_value=MagicMock(spec=discord.TextChannel))
        
        # Async generator for guild.bans()
        async def mock_bans():
            for b in []: yield b
        self.guild.bans = MagicMock(return_value=mock_bans())
        
        self.channel = MagicMock(spec=discord.TextChannel)
        self.channel.id = channel_id
        self.channel.name = "general"
        self.channel.mention = f"<#{channel_id}>"
        
        self.guild_id = guild_id
        self.channel_id = channel_id
        
        # Mock responses
        self.response = AsyncMock()
        self.followup = AsyncMock()
        
        self.captured_messages = []

    async def send_message(self, content=None, embed=None, view=None, ephemeral=False, file=None):
        msg = {"content": content, "embed": embed, "view": view, "ephemeral": ephemeral}
        self.captured_messages.append(msg)
        return MagicMock(spec=discord.Message)

    def is_done(self):
        return len(self.captured_messages) > 0

async def run_command_siege():
    print("INITIALIZING AUTO-CLAUDE COMMAND SIEGE (45+ COMMANDS)")
    
    # 1. Setup DBs
    db = Database()
    msg_db = MessageDBHandler("Test_Message_Database.db")
    
    # 2. Setup Bot
    bot = IntegratedCommandBot(db)
    
    # MOCK DISCORD INTERNALS
    bot.wait_until_ready = AsyncMock()
    bot.login = AsyncMock()
    bot.connect = AsyncMock()
    bot.fetch_user = AsyncMock(return_value=MagicMock(spec=discord.User))
    
    # Mock bot.user and bot.latency
    mock_bot_user = MagicMock()
    mock_bot_user.id = 999999
    mock_bot_user.name = "AutoClaudeTester"
    
    # Mock some bot attributes
    bot.repo_manager = MagicMock()
    bot.repo_manager.tree_cache = [{"path": "README.md", "type": "blob", "url": "..."}]
    bot.repo_manager.download_file = AsyncMock(return_value=(b"test data", "README.md"))
    bot.repo_manager.fetch_tree = AsyncMock(return_value=True)
    
    with patch.object(IntegratedCommandBot, 'user', new_callable=PropertyMock) as mock_user_prop, \
         patch.object(IntegratedCommandBot, 'latency', new_callable=PropertyMock) as mock_latency_prop:
        
        mock_user_prop.return_value = mock_bot_user
        mock_latency_prop.return_value = 0.05
        
        # Suppress task loops
        with patch("discord.ext.tasks.Loop.start", return_value=None):
            await bot.setup_hook()
        
        # Gather all commands
        all_commands = []
        for cmd in bot.tree.get_commands():
            if isinstance(cmd, app_commands.Group):
                for sub in cmd.commands:
                    all_commands.append((f"/{cmd.name} {sub.name}", sub))
            else:
                all_commands.append((f"/{cmd.name}", cmd))

        print(f"Found {len(all_commands)} registered slash commands.")

        results = []
        
        # 3. Iterate and Test
        for name, cmd in all_commands:
            print(f"Testing {name}...", end=" ", flush=True)
            it = MockInteraction(guild_id=123456789)
            it.response.send_message = it.send_message
            it.followup.send = it.send_message
            it.response.defer = AsyncMock()
            
            try:
                kwargs = {}
                params = cmd.parameters
                for p in params:
                    type_val = p.type.value if hasattr(p.type, 'value') else p.type
                    
                    if type_val in (6, 9): # user=6, member=6, mentionable=9
                        kwargs[p.name] = it.user
                    elif type_val == 7: # channel
                        kwargs[p.name] = it.channel
                    elif type_val in (4, 10): # integer=4, number=10
                        kwargs[p.name] = 10
                    elif type_val == 3: # string
                        if p.name == "date": kwargs[p.name] = "2026-03-01"
                        elif p.name == "time_str": kwargs[p.name] = "18:30"
                        else: kwargs[p.name] = "test_siege"
                    elif type_val == 5: # boolean
                        kwargs[p.name] = True
                    elif type_val == 8: # role
                        role = MagicMock(spec=discord.Role)
                        role.position = 1
                        kwargs[p.name] = role
                    elif type_val == 11: # attachment
                        att = MagicMock(spec=discord.Attachment)
                        att.filename = "test.json"
                        att.read = AsyncMock(return_value=b'{"test":1}')
                        kwargs[p.name] = att
                    elif not p.required:
                        kwargs[p.name] = None

                # Handle GroupCog subcommands vs standard commands
                # Use it.response.is_done() check to avoid RuntimeWarnings
                it.response.is_done = MagicMock(return_value=False)

                if hasattr(cmd, 'binding') and cmd.binding is not None:
                    # FIX: Handle cases where binding is None for some reason
                    res = await cmd.callback(cmd.binding, it, **kwargs)
                    if asyncio.iscoroutine(res): await res
                else:
                    try:
                        res = await cmd.callback(it, **kwargs)
                        if asyncio.iscoroutine(res): await res
                    except TypeError as te:
                        if "positional argument" in str(te):
                            res = await cmd.callback(bot, it, **kwargs)
                            if asyncio.iscoroutine(res): await res
                        else:
                            raise te
                
                if len(it.captured_messages) > 0 or it.response.defer.called:
                    print("PASS")
                    results.append((name, "PASS", it.captured_messages[0] if it.captured_messages else "Deferred"))
                else:
                    print("WARN (No Response)")
                    results.append((name, "WARN", "No response sent"))
                    
            except Exception as e:
                print(f"FAIL: {e}")
                results.append((name, "FAIL", str(e)))

        # 4. Summary Report
        print("\n" + "="*50)
        print("SIEGE SUMMARY REPORT")
        print("="*50)
        passed = sum(1 for r in results if r[1] == "PASS")
        failed = sum(1 for r in results if r[1] == "FAIL")
        warned = sum(1 for r in results if r[1] == "WARN")
        
        for name, status, detail in results:
            indicator = "OK" if status == "PASS" else "FAIL" if status == "FAIL" else "WARN"
            print(f"[{indicator}] {name.ljust(30)} | {status}")
            if status == "FAIL":
                print(f"   Error: {detail}")

        print("\n" + "="*50)
        print(f"TOTAL: {len(results)} | PASSED: {passed} | FAILED: {failed} | WARNED: {warned}")
        print("="*50)

if __name__ == "__main__":
    with patch("discord.http.HTTPClient.static_login", return_value=AsyncMock()):
        asyncio.run(run_command_siege())
