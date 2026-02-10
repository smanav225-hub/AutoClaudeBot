import sqlite3
import os
import time
import json
import asyncio
import random
from datetime import datetime
import discord
from Core.Welcome_Goodbye import BaseDiscordClient

# Absolute path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE_PATH = os.path.join(BASE_DIR, "Message_Database.db")

class MessageDBHandler:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_FILE_PATH
        print(f"[MessageDB] Initializing database at: {self.db_path}")
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL;")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                guild_id TEXT,
                channel_id TEXT,
                channel_name TEXT,
                user_id TEXT,
                username TEXT,
                user_discriminator TEXT,
                avatar_url TEXT,
                content TEXT,
                content_length INTEGER,
                word_count INTEGER,
                links_count INTEGER,
                links_list TEXT,
                has_links BOOLEAN,
                has_attachments BOOLEAN,
                attachment_count INTEGER,
                attachment_types TEXT,
                image_ids TEXT,
                image_count INTEGER,
                file_ids TEXT,
                emoji_used TEXT,
                emoji_count INTEGER,
                total_reactions_received INTEGER,
                reaction_details TEXT,
                reply_count INTEGER,
                mentioned_users TEXT,
                mentioned_count INTEGER,
                mentioned_roles TEXT,
                has_thread BOOLEAN,
                thread_id TEXT,
                is_pinned BOOLEAN,
                is_deleted BOOLEAN DEFAULT 0,
                bot_message BOOLEAN,
                webhook_message BOOLEAN,
                system_message BOOLEAN,
                created_at REAL,
                edited_at REAL,
                deleted_at REAL,
                updated_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_levels (
                user_id TEXT PRIMARY KEY,
                guild_id TEXT,
                username TEXT,
                user_discriminator TEXT,
                avatar_url TEXT,
                messages_total INTEGER,
                characters_total INTEGER,
                words_total INTEGER,
                xp_total INTEGER,
                xp_current INTEGER,
                level INTEGER,
                last_message_at REAL,
                updated_at REAL
            )
        ''')
        
        # Index updates for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_guild_created ON messages(guild_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_channel_created ON messages(channel_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_levels_guild ON user_levels(guild_id, xp_total)")
        
        conn.commit()
        conn.close()

    def process_message_data(self, message):
        # Extract basic info
        content = message.content or ""
        
        # Links processing (simple heuristic)
        links = [word for word in content.split() if word.startswith("http://") or word.startswith("https://")]
        
        # Attachments
        attachment_types = [a.content_type for a in message.attachments if a.content_type]
        image_attachments = [a for a in message.attachments if a.content_type and a.content_type.startswith("image/")]
        
        # Mentions
        mentioned_users = [str(u.id) for u in message.mentions]
        mentioned_roles = [str(r.id) for r in message.role_mentions]
        
        return {
            "message_id": str(message.id),
            "guild_id": str(message.guild.id) if message.guild else None,
            "channel_id": str(message.channel.id),
            "channel_name": message.channel.name if hasattr(message.channel, "name") else "DM",
            "user_id": str(message.author.id),
            "username": message.author.name,
            "user_discriminator": message.author.discriminator,
            "avatar_url": str(message.author.display_avatar.url) if message.author.display_avatar else "",
            "content": content,
            "content_length": len(content),
            "word_count": len(content.split()),
            "links_count": len(links),
            "links_list": json.dumps(links),
            "has_links": len(links) > 0,
            "has_attachments": len(message.attachments) > 0,
            "attachment_count": len(message.attachments),
            "attachment_types": json.dumps(attachment_types),
            "image_ids": json.dumps([str(a.id) for a in image_attachments]),
            "image_count": len(image_attachments),
            "file_ids": json.dumps([str(a.id) for a in message.attachments]),
            "emoji_used": json.dumps([]), # Complex parsing omitted for brevity
            "emoji_count": 0,
            "total_reactions_received": 0,
            "reaction_details": json.dumps({}),
            "reply_count": 0, # Discord API doesn't provide this directly in message object easily without cache
            "mentioned_users": json.dumps(mentioned_users),
            "mentioned_count": len(mentioned_users),
            "mentioned_roles": json.dumps(mentioned_roles),
            "has_thread": message.thread is not None,
            "thread_id": str(message.thread.id) if message.thread else None,
            "is_pinned": message.pinned,
            "bot_message": message.author.bot,
            "webhook_message": message.webhook_id is not None,
            "system_message": message.is_system(),
            "created_at": message.created_at.timestamp(),
            "updated_at": time.time()
        }

    def log_message(self, message):
        data = self.process_message_data(message)
        self.upsert_message(data)

    def upsert_message(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        placeholders = ", ".join(["?"] * len(data))
        headers = ", ".join(data.keys())
        values = list(data.values())
        
        sql = f'''
            INSERT INTO messages ({headers}) VALUES ({placeholders})
            ON CONFLICT(message_id) DO UPDATE SET
                content=excluded.content,
                updated_at=excluded.updated_at,
                edited_at=excluded.updated_at
        '''
        
        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"[MessageDB] Error logging message: {e}")
        finally:
            conn.close()

    def batch_insert_messages(self, messages_data):
        if not messages_data: return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Assume all dicts have same keys
        keys = messages_data[0].keys()
        headers = ", ".join(keys)
        placeholders = ", ".join(["?"] * len(keys))
        
        sql = f'''
            INSERT OR IGNORE INTO messages ({headers}) VALUES ({placeholders})
        '''
        
        values_list = [list(d.values()) for d in messages_data]
        
        try:
            cursor.executemany(sql, values_list)
            conn.commit()
        except Exception as e:
            print(f"[MessageDB] Batch insert error: {e}")
        finally:
            conn.close()

    def mark_deleted(self, message_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET is_deleted=1, deleted_at=? WHERE message_id=?", (time.time(), str(message_id)))
        conn.commit()
        conn.close()

    def get_messages_today_count(self, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get start of day timestamp
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        
        cursor.execute("SELECT COUNT(*) FROM messages WHERE guild_id=? AND created_at >= ?", (str(guild_id), start_of_day))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_last_message_id(self, channel_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT message_id FROM messages WHERE channel_id=? ORDER BY created_at DESC LIMIT 1", (str(channel_id),))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def get_all_messages(self, guild_id):
        conn = self.get_connection()
        # Use row factory for dict-like access
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE guild_id=? ORDER BY created_at ASC", (str(guild_id),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_user_level(self, guild_id, user_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_levels WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def upsert_user_level(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(data))
        headers = ", ".join(data.keys())
        values = list(data.values())
        sql = f'''
            INSERT INTO user_levels ({headers}) VALUES ({placeholders})
            ON CONFLICT(user_id) DO UPDATE SET
                guild_id=excluded.guild_id,
                username=excluded.username,
                user_discriminator=excluded.user_discriminator,
                avatar_url=excluded.avatar_url,
                messages_total=excluded.messages_total,
                characters_total=excluded.characters_total,
                words_total=excluded.words_total,
                xp_total=excluded.xp_total,
                xp_current=excluded.xp_current,
                level=excluded.level,
                last_message_at=excluded.last_message_at,
                updated_at=excluded.updated_at
        '''
        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"[MessageDB] Error upserting user_levels: {e}")
        finally:
            conn.close()

    def update_user_level_from_message(self, message, xp_gain, level, xp_current, xp_total):
        content = message.content or ""
        chars = len(content)
        words = len(content.split())
        now = time.time()
        existing = self.get_user_level(message.guild.id, message.author.id)

        if existing:
            data = {
                "user_id": str(message.author.id),
                "guild_id": str(message.guild.id),
                "username": message.author.name,
                "user_discriminator": message.author.discriminator,
                "avatar_url": str(message.author.display_avatar.url) if message.author.display_avatar else "",
                "messages_total": int(existing.get("messages_total", 0)) + 1,
                "characters_total": int(existing.get("characters_total", 0)) + chars,
                "words_total": int(existing.get("words_total", 0)) + words,
                "xp_total": int(existing.get("xp_total", 0)) + int(xp_gain),
                "xp_current": int(xp_current),
                "level": int(level),
                "last_message_at": now,
                "updated_at": now
            }
        else:
            data = {
                "user_id": str(message.author.id),
                "guild_id": str(message.guild.id),
                "username": message.author.name,
                "user_discriminator": message.author.discriminator,
                "avatar_url": str(message.author.display_avatar.url) if message.author.display_avatar else "",
                "messages_total": 1,
                "characters_total": chars,
                "words_total": words,
                "xp_total": int(xp_gain),
                "xp_current": int(xp_current),
                "level": int(level),
                "last_message_at": now,
                "updated_at": now
            }

        self.upsert_user_level(data)

    def get_user_rank(self, guild_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT xp_total FROM user_levels WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        xp_total = row[0] or 0
        cursor.execute("SELECT COUNT(*) FROM user_levels WHERE guild_id=? AND xp_total > ?", (str(guild_id), xp_total))
        count = cursor.fetchone()[0]
        conn.close()
        return int(count) + 1

    def _safe_eval(self, expr, variables):
        expr = (expr or "").replace("^", "**")
        return eval(expr, {"__builtins__": {}}, variables)

    def _xp_needed(self, level, formula):
        default_formula = "5 * (level ** 2) + (50 * level) + 100"
        try:
            return int(self._safe_eval(formula or default_formula, {"level": level}))
        except Exception:
            return int(self._safe_eval(default_formula, {"level": level}))

    def _compute_level_from_total(self, xp_total, formula):
        level = 0
        remaining = int(xp_total)
        safety = 0
        while True:
            needed = self._xp_needed(level, formula)
            if remaining >= needed:
                remaining -= needed
                level += 1
            else:
                break
            safety += 1
            if safety > 10000:
                break
        return level, remaining

    def rebuild_user_levels_from_messages(self, guild_id, xp_min=15, xp_max=25, formula=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user_levels WHERE guild_id=?", (str(guild_id),))
        cursor.execute(
            """
            SELECT user_id, username, user_discriminator, avatar_url,
                   content_length, word_count, created_at, bot_message, is_deleted
            FROM messages
            WHERE guild_id=?
            """,
            (str(guild_id),)
        )
        rows = cursor.fetchall()
        conn.close()

        users = {}
        for row in rows:
            if row["bot_message"]:
                continue
            if row["is_deleted"]:
                continue

            uid = str(row["user_id"])
            if uid not in users:
                users[uid] = {
                    "user_id": uid,
                    "guild_id": str(guild_id),
                    "username": row["username"] or "",
                    "user_discriminator": row["user_discriminator"] or "",
                    "avatar_url": row["avatar_url"] or "",
                    "messages_total": 0,
                    "characters_total": 0,
                    "words_total": 0,
                    "xp_total": 0,
                    "last_message_at": 0,
                }

            u = users[uid]
            u["messages_total"] += 1
            u["characters_total"] += int(row["content_length"] or 0)
            u["words_total"] += int(row["word_count"] or 0)
            u["xp_total"] += int(random.randint(int(xp_min), int(xp_max)))
            created_at = float(row["created_at"] or 0)
            if created_at > u["last_message_at"]:
                u["last_message_at"] = created_at

        now = time.time()
        for u in users.values():
            level, xp_current = self._compute_level_from_total(u["xp_total"], formula or "")
            u["level"] = int(level)
            u["xp_current"] = int(xp_current)
            u["updated_at"] = now
            self.upsert_user_level(u)

        return len(users)

class MessageLoggerClient(BaseDiscordClient):
    def __init__(self, db, msg_db_handler):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True
        discord.Client.__init__(self, intents=intents)
        self.db = db
        self.token = db.token
        self.msg_db = msg_db_handler

    async def on_ready(self):
        print(f"[MessageLogger] Logged in as {self.user}")

    async def on_message(self, message):
        if not message.guild: return
        self.msg_db.log_message(message)

    async def on_message_edit(self, before, after):
        if not after.guild: return
        self.msg_db.log_message(after)

    async def on_message_delete(self, message):
        self.msg_db.mark_deleted(message.id)

    async def download_history_background(self, guild_id, status_tracker):
        guild = self.get_guild(int(guild_id))
        if not guild:
            status_tracker["status"] = "error"
            status_tracker["error"] = "Guild not found"
            return
        
        status_tracker["status"] = "downloading"
        total_downloaded = 0
        total_channels = len(guild.text_channels)
        processed_channels = 0
        
        for channel in guild.text_channels:
            try:
                # Check cancellation
                # if status_tracker.get("cancel"): break
                
                processed_channels += 1
                status_tracker["progress_text"] = f"Processing #{channel.name} ({processed_channels}/{total_channels})"
                
                permissions = channel.permissions_for(guild.me)
                if not permissions.read_message_history:
                    continue

                last_id_str = self.msg_db.get_last_message_id(channel.id)
                last_msg_obj = None
                
                if last_id_str:
                    try:
                        last_msg_obj = await channel.fetch_message(int(last_id_str))
                    except:
                        pass
                
                batch = []
                async for message in channel.history(limit=None, after=last_msg_obj, oldest_first=True):
                    data = self.msg_db.process_message_data(message)
                    batch.append(data)
                    
                    if len(batch) >= 100:
                        self.msg_db.batch_insert_messages(batch)
                        total_downloaded += len(batch)
                        status_tracker["total_downloaded"] = total_downloaded
                        batch = []
                        await asyncio.sleep(0.1)
                
                if batch:
                    self.msg_db.batch_insert_messages(batch)
                    total_downloaded += len(batch)
                    status_tracker["total_downloaded"] = total_downloaded
                    
            except Exception as e:
                print(f"[MessageLogger] Error in {channel.name}: {e}")
        
        status_tracker["status"] = "rebuilding"
        status_tracker["progress_text"] = "Updating user XP totals..."

        try:
            levels_config = self.db.get_config(str(guild_id), "levels") or {}
            formula = levels_config.get("formula", "5 * (level ** 2) + (50 * level) + 100")
            updated_users = self.msg_db.rebuild_user_levels_from_messages(
                guild_id,
                xp_min=15,
                xp_max=25,
                formula=formula
            )
            status_tracker["total_users"] = updated_users
            status_tracker["status"] = "completed"
            status_tracker["progress_text"] = f"Complete: {updated_users} users updated"
        except Exception as e:
            status_tracker["status"] = "error"
            status_tracker["error"] = f"Rebuild failed: {e}"
