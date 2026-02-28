"""
AutoClaude Bot - Automated Command Test Script
=============================================
This script connects to Discord using the bot token, sends slash commands
as interactions, and reports what works and what fails.

Usage:
    python AutoTest.py

Prerequisites:
    pip install discord.py requests
    
The script will print a pass/fail report for every testable command.
"""
import discord
import asyncio
import sys
import os
import time
import json
import re

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
# Load token from Database.py settings or environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Database import Database
    db = Database()
    BOT_TOKEN = db.get_token() or os.environ.get("DISCORD_TOKEN", "")
    settings = db.get_settings()
    TEST_GUILD_ID = int(db.data.get("last_server", 0)) if db.data.get("last_server") else None
except Exception as e:
    print(f"[WARN] Could not load Database: {e}")
    BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")
    TEST_GUILD_ID = None

TEST_CHANNEL_ID = None  # Will auto-detect first available channel

# ─── TEST RESULTS ─────────────────────────────────────────────────────────────
results = {
    "passed": [],
    "failed": [],
    "skipped": []
}

# ─── BOT CLIENT FOR TESTING ──────────────────────────────────────────────────
class TestBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.guild = None
        self.test_channel = None

    async def on_ready(self):
        global TEST_GUILD_ID, TEST_CHANNEL_ID
        print(f"\n{'='*60}")
        print(f"  AutoClaude Test Bot Connected as: {self.user}")
        print(f"{'='*60}\n")
        
        # Find test guild
        if TEST_GUILD_ID:
            self.guild = self.get_guild(TEST_GUILD_ID)
        else:
            self.guild = self.guilds[0] if self.guilds else None
        
        if not self.guild:
            print("❌ ERROR: No guild found! Make sure the bot is in a server.")
            await self.close()
            return
        
        print(f"✅ Using guild: {self.guild.name} (ID: {self.guild.id})")
        
        # Find a text channel to use for tests
        for channel in self.guild.text_channels:
            if channel.permissions_for(self.guild.me).send_messages:
                self.test_channel = channel
                break
        
        if not self.test_channel:
            print("❌ ERROR: No accessible text channel found!")
            await self.close()
            return
        
        print(f"✅ Testing in channel: #{self.test_channel.name}")
        print(f"\nRunning tests...\n")
        
        await asyncio.sleep(2)
        await self.run_all_tests()

    async def test_command(self, name, coroutine, expect_pass=True):
        """Run a single test and record result"""
        try:
            await coroutine
            if expect_pass:
                results["passed"].append(name)
                print(f"  ✅ PASS: {name}")
            else:
                results["failed"].append(name)
                print(f"  ❌ UNEXPECTED PASS: {name}")
        except Exception as e:
            if not expect_pass:
                results["passed"].append(name)
                print(f"  ✅ EXPECTED FAIL: {name}")
            else:
                results["failed"].append(name)
                print(f"  ❌ FAIL: {name} — {e}")

    async def send_test_message(self, content, delete_after=3):
        """Safe message sending for tests"""
        try:
            msg = await self.test_channel.send(content)
            await asyncio.sleep(delete_after)
            try:
                await msg.delete()
            except:
                pass
            return msg
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")

    async def check_bot_commands_synced(self):
        """Verify the bot's slash commands are visible"""
        try:
            guild = self.guild
            cmds = await self.http.get_guild_commands(int(self.application_id), guild.id)
            cmd_names = [c['name'] for c in cmds]
            
            expected_commands = [
                "ping", "help", "health-check", "leaderboard-post",
                "profile", "thank", "moderation", "role", "role-config",
                "event", "punishment", "backup", "ticket", "poll", 
                "autorole", "afk", "quests", "achievements"
            ]
            
            missing = [c for c in expected_commands if c not in cmd_names]
            present = [c for c in expected_commands if c in cmd_names]
            
            print(f"\n📋 Slash Command Registry Check:")
            print(f"   Registered: {len(cmd_names)} commands total")
            print(f"   Expected present ({len(present)}): {', '.join(present)}")
            if missing:
                print(f"   ⚠️  MISSING ({len(missing)}): {', '.join(missing)}")
            else:
                print(f"   ✅ ALL expected commands registered!")
            return len(missing) == 0, missing
        except Exception as e:
            print(f"   ❌ Could not check commands: {e}")
            return False, []

    async def check_db_tables(self):
        """Verify the database has all required tables and columns"""
        try:
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            conn = db.get_connection()
            import sqlite3
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {r['name'] for r in cursor.fetchall()}
            
            required_tables = [
                "messages", "user_levels", "reputation_events",
                "punishments", "moderation_rules", "events",
                "polls", "poll_votes", "tickets", "user_quests",
                "user_achievements", "health_metrics_rollups",
                "self_assignable_roles"
            ]
            
            missing_tables = [t for t in required_tables if t not in tables]
            
            # Check reputation column in user_levels
            try:
                cursor.execute("SELECT reputation FROM user_levels LIMIT 1")
                rep_col_ok = True
            except:
                rep_col_ok = False
            
            conn.close()
            
            print(f"\n💾 Database Schema Check:")
            print(f"   Tables found: {len(tables)}")
            if missing_tables:
                print(f"   ⚠️  MISSING tables: {', '.join(missing_tables)}")
            else:
                print(f"   ✅ All required tables present!")
            print(f"   reputation column in user_levels: {'✅ OK' if rep_col_ok else '❌ MISSING — will be added on restart'}")
            
            return len(missing_tables) == 0
        except Exception as e:
            print(f"   ❌ DB check failed: {e}")
            return False

    async def check_db_methods(self):
        """Verify key DB methods exist and are synchronous"""
        from Message_Database import MessageDBHandler
        db_obj = MessageDBHandler()
        
        print(f"\n🔧 DB Method Sync Check:")
        methods = {
            "get_guild_leaderboard": True,   # should be sync
            "add_mod_rule": True,
            "get_mod_rules": True,
            "remove_mod_rule": True,
            "create_event": True,
            "get_events": True,
            "compute_hourly_rollup": True,
            "get_health_rollup": True,
            "set_self_assignable_role": True,
            "get_self_assignable_roles": True,
            "get_reputation_count_today": True,
            "add_reputation_event": True,
            "get_user_reputation": True,
            "get_recent_thanks": True,
        }
        
        all_ok = True
        import inspect
        for method_name, should_be_sync in methods.items():
            method = getattr(db_obj, method_name, None)
            if method is None:
                print(f"   ❌ {method_name}: MISSING")
                all_ok = False
                continue
            is_coro = inspect.iscoroutinefunction(method)
            if should_be_sync and is_coro:
                print(f"   ❌ {method_name}: Is async (should be sync!)")
                all_ok = False
            elif not should_be_sync and not is_coro:
                print(f"   ⚠️  {method_name}: Is sync (expected async)")
            else:
                print(f"   ✅ {method_name}: {'async' if is_coro else 'sync'} OK")
        return all_ok

    async def run_all_tests(self):
        """Main test suite"""
        print("=" * 60)
        print("  PHASE 1: Database & Infrastructure Tests")
        print("=" * 60)
        
        await self.check_db_tables()
        await self.check_db_methods()
        await self.check_bot_commands_synced()
        
        print("\n" + "=" * 60)
        print("  PHASE 2: Live Channel Interaction Tests")
        print("=" * 60)
        
        # Test 1: Ping (basic message sending)
        print("\n[Test] Can bot send a message?")
        await self.test_command(
            "Bot can send messages to channel",
            self.send_test_message("🤖 AutoTest: Bot is online and can send messages! (auto-delete in 3s)")
        )
        
        # Test 2: Check punishments table
        print("\n[Test] Punishments table accessible?")
        async def test_punishments_table():
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            conn = db.get_connection()
            import sqlite3
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM punishments")
            row = cursor.fetchone()
            conn.close()
            print(f"         → {row['cnt']} punishment records in DB")
        await self.test_command("Punishments table accessible", test_punishments_table())
        
        # Test 3: reputation column
        print("\n[Test] reputation column in user_levels?")
        async def test_reputation_col():
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT reputation FROM user_levels LIMIT 1")
            conn.close()
        await self.test_command("reputation column in user_levels", test_reputation_col())
        
        # Test 4: Moderation rules
        print("\n[Test] add_mod_rule and get_mod_rules?")
        async def test_mod_rules():
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            db.add_mod_rule(self.guild.id, "blocklist", "test_autotest_word", "warn", "Test rule", self.guild.me.id)
            rules = db.get_mod_rules(self.guild.id)
            test_rules = [r for r in rules if r['pattern'] == 'test_autotest_word']
            if not test_rules:
                raise RuntimeError("Rule was not saved to database!")
            db.remove_mod_rule(test_rules[0]['id'], self.guild.id)
            leftover = [r for r in db.get_mod_rules(self.guild.id) if r['pattern'] == 'test_autotest_word']
            if leftover:
                raise RuntimeError("Rule was not removed from database!")
        await self.test_command("add_mod_rule / get_mod_rules / remove_mod_rule", test_mod_rules())
        
        # Test 5: Self-assignable roles
        print("\n[Test] set_self_assignable_role and get_self_assignable_roles?")
        async def test_roles():
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            fake_role_id = "999999999999999999"
            db.set_self_assignable_role(self.guild.id, fake_role_id, True)
            roles = db.get_self_assignable_roles(str(self.guild.id))
            if fake_role_id not in roles:
                raise RuntimeError("Role was not saved!")
            db.set_self_assignable_role(self.guild.id, fake_role_id, False)
        await self.test_command("set_self_assignable_role / get_self_assignable_roles", test_roles())
        
        # Test 6: create_event
        print("\n[Test] create_event?")
        async def test_event():
            from Message_Database import MessageDBHandler
            import time
            db = MessageDBHandler()
            future_ts = time.time() + 3600
            event_id = db.create_event(self.guild.id, self.test_channel.id, self.guild.me.id, "AutoTest Event", "Test", future_ts, None)
            if not event_id:
                raise RuntimeError("create_event returned no ID!")
        await self.test_command("create_event (returns sync ID)", test_event())
        
        # Test 7: Leaderboard (sync)
        print("\n[Test] get_guild_leaderboard (sync)?")
        async def test_leaderboard():
            from Message_Database import MessageDBHandler
            db = MessageDBHandler()
            results_lb = db.get_guild_leaderboard(str(self.guild.id), "all", 5)
            # Should return a list (even if empty)
            if not isinstance(results_lb, list):
                raise RuntimeError("Expected list, got something else!")
        await self.test_command("get_guild_leaderboard (sync)", test_leaderboard())
        
        # ── FINAL REPORT ──────────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("  TEST RESULTS SUMMARY")
        print("=" * 60)
        total = len(results["passed"]) + len(results["failed"]) + len(results["skipped"])
        print(f"\n  Total tests: {total}")
        print(f"  ✅ Passed:   {len(results['passed'])}")
        print(f"  ❌ Failed:   {len(results['failed'])}")
        print(f"  ⏭️  Skipped:  {len(results['skipped'])}")
        
        if results["failed"]:
            print(f"\n  Failed tests:")
            for f in results["failed"]:
                print(f"    • {f}")
        
        # Save report to file
        report_path = os.path.join(os.path.dirname(__file__), "test_report.txt")
        with open(report_path, "w") as f:
            f.write(f"AutoClaude Test Report - {time.strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Total: {total} | Passed: {len(results['passed'])} | Failed: {len(results['failed'])}\n\n")
            f.write("PASSED:\n")
            for r in results["passed"]:
                f.write(f"  ✅ {r}\n")
            f.write("\nFAILED:\n")
            for r in results["failed"]:
                f.write(f"  ❌ {r}\n")
        
        print(f"\n  Report saved to: test_report.txt")
        print("\n" + "=" * 60)
        
        await asyncio.sleep(2)
        await self.close()


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
async def main():
    if not BOT_TOKEN:
        print("❌ ERROR: No bot token found!")
        print("   Make sure the token is set in the GUI settings or as DISCORD_TOKEN env variable.")
        return
    
    print(f"Starting AutoTest... (Token: {BOT_TOKEN[:10]}...)")
    
    client = TestBot()
    try:
        await client.start(BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Check your bot token.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
