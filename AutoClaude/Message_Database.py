import sqlite3
import os
import time
import json
import asyncio
import random
from datetime import datetime, timedelta
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
                parent_message_id TEXT,
                reply_to_user_id TEXT,
                is_deleted BOOLEAN DEFAULT 0,
                bot_message BOOLEAN,
                webhook_message BOOLEAN,
                system_message BOOLEAN,
                xp_gain INTEGER DEFAULT 0,
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
                reputation INTEGER DEFAULT 0,
                last_message_at REAL,
                updated_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reputation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                giver_id TEXT,
                receiver_id TEXT,
                reason TEXT,
                created_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                channel_id TEXT,
                message_id TEXT,
                creator_id TEXT,
                question TEXT,
                options TEXT, -- JSON list
                created_at REAL,
                ends_at REAL,
                is_closed BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS poll_votes (
                poll_id INTEGER,
                user_id TEXT,
                option_index INTEGER,
                created_at REAL,
                PRIMARY KEY (poll_id, user_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moderation_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                type TEXT, -- regex, blocklist, link_filter
                pattern TEXT,
                action TEXT, -- delete, warn
                reason TEXT,
                creator_id TEXT,
                enabled BOOLEAN DEFAULT 1,
                created_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_quests (
                guild_id TEXT,
                user_id TEXT,
                quest_id TEXT,
                completed_at REAL,
                PRIMARY KEY (guild_id, user_id, quest_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS self_assignable_roles (
                guild_id TEXT,
                role_id TEXT,
                PRIMARY KEY (guild_id, role_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                channel_id TEXT,
                creator_id TEXT,
                title TEXT,
                description TEXT,
                scheduled_at REAL,
                reminder_minutes INTEGER,
                cancelled_at REAL,
                created_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                guild_id TEXT,
                user_id TEXT,
                achievement_id TEXT,
                unlocked_at REAL,
                PRIMARY KEY (guild_id, user_id, achievement_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_roles (
                guild_id TEXT,
                role_id TEXT,
                is_self_assignable BOOLEAN DEFAULT 0,
                PRIMARY KEY (guild_id, role_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                channel_id TEXT,
                user_id TEXT,
                subject TEXT,
                status TEXT DEFAULT 'open',
                closed_by TEXT,
                closed_at REAL,
                transcript_json TEXT,
                created_at REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_metrics_rollups (
                guild_id TEXT,
                bucket REAL,
                message_count INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                xp_awarded INTEGER DEFAULT 0,
                new_members INTEGER DEFAULT 0,
                reputation_given INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, bucket)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS punishments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                user_id TEXT,
                type TEXT,
                reason TEXT,
                expires_at REAL,
                created_by TEXT,
                created_at REAL,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_streaks (
                guild_id TEXT,
                user_id TEXT,
                streak_type TEXT DEFAULT 'message',
                current_count INTEGER DEFAULT 0,
                best_count INTEGER DEFAULT 0,
                last_active_day TEXT,
                updated_at REAL,
                PRIMARY KEY (guild_id, user_id, streak_type)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moderation_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT,
                rule_id INTEGER,
                message_id TEXT,
                actor_id TEXT,
                target_user_id TEXT,
                username TEXT,
                content TEXT,
                action TEXT,
                reason TEXT,
                metadata_json TEXT,
                created_at REAL
            )
        ''')
        
        # Index updates for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_guild_created ON messages(guild_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_channel_created ON messages(channel_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_levels_guild ON user_levels(guild_id, xp_total)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rep_giver ON reputation_events(giver_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rep_receiver ON reputation_events(receiver_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_polls_guild ON polls(guild_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mod_rules_guild ON moderation_rules(guild_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_quests ON user_quests(guild_id, user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_guild ON events(guild_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_achievements ON user_achievements(guild_id, user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_guild_roles ON guild_roles(guild_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_guild ON tickets(guild_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_channel ON tickets(channel_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_metrics ON health_metrics_rollups(guild_id, bucket)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_punishments_user ON punishments(guild_id, user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_streaks_guild ON user_streaks(guild_id, streak_type, current_count)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mod_actions_guild ON moderation_actions(guild_id, created_at)")
        
        # === MIGRATIONS: Safely add missing columns to existing databases ===
        migrations = [
            ("user_levels", "reputation INTEGER DEFAULT 0"),
            ("user_levels", "xp_current INTEGER DEFAULT 0"),
            ("user_levels", "level INTEGER DEFAULT 0"),
            ("user_levels", "messages_total INTEGER DEFAULT 0"),
            ("messages", "reply_to_user_id TEXT"),
            ("messages", "parent_message_id TEXT"),
            ("messages", "xp_gain INTEGER DEFAULT 0"),
            ("moderation_actions", "content TEXT"),
            ("moderation_actions", "username TEXT"),
            ("health_metrics_rollups", "xp_awarded INTEGER DEFAULT 0"),
            ("health_metrics_rollups", "new_members INTEGER DEFAULT 0"),
            ("health_metrics_rollups", "reputation_given INTEGER DEFAULT 0"),
        ]
        for table, col_def in migrations:
            col_name = col_def.split()[0]
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
                print(f"[Migration] Added column '{col_name}' to '{table}'")
            except Exception:
                pass  # Column already exists, that's fine
        
        conn.commit()
        conn.close()

    def process_message_data(self, message, **kwargs):
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
        
        # Emoji processing
        import re
        custom_emojis = re.findall(r'<a?:\w+:\d+>', content)
        # Simple unicode emoji check (common ranges)
        unicode_emojis = re.findall(r'[\U00010000-\U0010ffff]', content)
        emoji_count = len(custom_emojis) + len(unicode_emojis)
        
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
            "emoji_used": json.dumps(custom_emojis + unicode_emojis),
            "emoji_count": emoji_count,
            "total_reactions_received": 0,
            "reaction_details": json.dumps({}),
            "reply_count": 0, # Discord API doesn't provide this directly in message object easily without cache
            "mentioned_users": json.dumps(mentioned_users),
            "mentioned_count": len(mentioned_users),
            "mentioned_roles": json.dumps(mentioned_roles),
            "has_thread": message.thread is not None,
            "thread_id": str(message.thread.id) if message.thread else None,
            "is_pinned": message.pinned,
            "parent_message_id": str(message.reference.message_id) if message.reference and message.reference.message_id else None,
            "reply_to_user_id": str(message.reference.resolved.author.id) if message.reference and message.reference.resolved and hasattr(message.reference.resolved, "author") else None,
            "bot_message": message.author.bot,
            "webhook_message": message.webhook_id is not None,
            "system_message": message.is_system(),
            "xp_gain": kwargs.get("xp_gain", 0),
            "created_at": message.created_at.timestamp(),
            "updated_at": time.time()
        }

    def log_message(self, message, **kwargs):
        data = self.process_message_data(message, **kwargs)
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
                xp_gain=CASE WHEN excluded.xp_gain > 0 THEN excluded.xp_gain ELSE messages.xp_gain END,
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
        
        # Ensure all required columns are present in the first dict
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

    def has_message(self, message_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM messages WHERE message_id=?", (str(message_id),))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def get_all_messages(self, guild_id):
        conn = self.get_connection()
        # Use row factory for dict-like access
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE guild_id=? ORDER BY created_at ASC", (str(guild_id),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_guild_leaderboard(self, guild_id, period="all", limit=15, metric="total_xp"):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        guild_id_str = str(guild_id)
        now = datetime.now()
        start_ts = 0
        
        if period == "today":
            start_ts = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        elif period == "weekly":
            start_ts = (now - timedelta(days=7)).timestamp()
        elif period in ("monthly", "this_month"):
            start_ts = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        
        if period == "all" and metric in ("total_xp", "level", "total_messages"):
            col = "messages_total" if metric == "total_messages" else metric
            cur.execute(
                f"SELECT user_id, username, user_discriminator, xp_total, level, messages_total as total_messages "
                f"FROM user_levels WHERE guild_id=? ORDER BY {col} DESC LIMIT ?",
                (guild_id_str, limit)
            )
        else:
            cur.execute(
                """
                SELECT user_id, username, user_discriminator, 
                       COUNT(*) as total_messages,
                       SUM(word_count) as words_typed,
                       SUM(xp_gain) as total_xp
                FROM messages
                WHERE guild_id=? AND created_at >= ? AND is_deleted=0
                GROUP BY user_id
                ORDER BY total_xp DESC
                LIMIT ?
                """,
                (guild_id_str, start_ts, limit)
            )
            
        rows = cur.fetchall()
        conn.close()
        
        results = []
        for i, row in enumerate(rows, 1):
            r = dict(row)
            r["rank"] = i
            r["user_tag"] = f"{r['username']}#{r['user_discriminator']}" if r.get('user_discriminator') and r['user_discriminator'] != '0' else r.get('username', 'Unknown')
            results.append(r)
            
        return results

    def add_mod_rule(self, guild_id, rule_type, pattern, action, reason, creator_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO moderation_rules (guild_id, type, pattern, action, reason, creator_id, enabled, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
            (str(guild_id), rule_type, pattern, action, reason, str(creator_id), now)
        )
        conn.commit()
        conn.close()

    def get_mod_rules(self, guild_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM moderation_rules WHERE guild_id=? AND enabled=1 ORDER BY id ASC",
            (str(guild_id),)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def remove_mod_rule(self, rule_id, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE moderation_rules SET enabled=0 WHERE id=? AND guild_id=?", (rule_id, str(guild_id)))
        conn.commit()
        conn.close()

    def create_event(self, guild_id, channel_id, creator_id, title, description, scheduled_at, reminder_minutes):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO events (guild_id, channel_id, creator_id, title, description, scheduled_at, reminder_minutes, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(guild_id), str(channel_id), str(creator_id), title, description, scheduled_at, reminder_minutes, now)
        )
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return row_id

    def cancel_event(self, event_id, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET status='cancelled' WHERE id=? AND guild_id=?", (event_id, str(guild_id)))
        conn.commit()
        conn.close()

    def get_events(self, guild_id, status='active'):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE guild_id=? AND status=? ORDER BY scheduled_at ASC",
            (str(guild_id), status)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def compute_hourly_rollup(self, guild_id, bucket_start, bucket_end):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*), COUNT(DISTINCT user_id) FROM messages "
            "WHERE guild_id=? AND created_at >= ? AND created_at < ?",
            (str(guild_id), bucket_start, bucket_end)
        )
        msg_count, active_users = cursor.fetchone()
        cursor.execute(
            "SELECT COUNT(*) FROM reputation_events "
            "WHERE guild_id=? AND created_at >= ? AND created_at < ?",
            (str(guild_id), bucket_start, bucket_end)
        )
        rep_given = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO health_metrics_rollups (guild_id, bucket, message_count, active_users, reputation_given) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(guild_id, bucket) DO UPDATE SET "
            "message_count=excluded.message_count, active_users=excluded.active_users, reputation_given=excluded.reputation_given",
            (str(guild_id), bucket_start, msg_count, active_users, rep_given)
        )
        conn.commit()
        conn.close()

    def get_health_rollup(self, guild_id, bucket):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM health_metrics_rollups WHERE guild_id=? AND bucket=?",
            (str(guild_id), bucket)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_health_rollups(self, guild_id, start_bucket, end_bucket):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM health_metrics_rollups
            WHERE guild_id=? AND bucket >= ? AND bucket <= ?
            ORDER BY bucket ASC
            """,
            (str(guild_id), float(start_bucket), float(end_bucket))
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    async def export_users_csv(self, guild_id, exclude_ids=None, limit=100):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        exclude_ids = exclude_ids or []
        placeholders = ",".join(["?"] * len(exclude_ids))
        query = (
            f"SELECT user_id, username, user_discriminator, level, xp_total "
            f"FROM user_levels WHERE guild_id=? "
        )
        if exclude_ids:
            query += f"AND user_id NOT IN ({placeholders}) "
        query += "ORDER BY RANDOM() LIMIT ?"
        
        params = [str(guild_id)] + [str(uid) for uid in exclude_ids] + [limit]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        import io
        import csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["User ID", "Username", "Discriminator", "Level", "XP Total"])
        for row in rows:
            writer.writerow([row['user_id'], row['username'], row['user_discriminator'], row['level'], row['xp_total']])
            
        return output.getvalue(), len(rows)

    def set_self_assignable_role(self, guild_id, role_id, is_assignable):
        conn = self.get_connection()
        cursor = conn.cursor()
        if is_assignable:
            cursor.execute(
                "INSERT INTO self_assignable_roles (guild_id, role_id) VALUES (?, ?) "
                "ON CONFLICT(guild_id, role_id) DO NOTHING",
                (str(guild_id), str(role_id))
            )
        else:
            cursor.execute(
                "DELETE FROM self_assignable_roles WHERE guild_id=? AND role_id=?",
                (str(guild_id), str(role_id))
            )
        conn.commit()
        conn.close()

    def get_self_assignable_roles(self, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM self_assignable_roles WHERE guild_id=?", (str(guild_id),))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    async def get_quest_progress(self, guild_id, user_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_quests WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    async def complete_quest(self, guild_id, user_id, quest_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO user_quests (guild_id, user_id, quest_id, completed_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(guild_id, user_id, quest_id) DO NOTHING",
            (str(guild_id), str(user_id), quest_id, now)
        )
        conn.commit()
        conn.close()

    async def create_punishment(self, guild_id, user_id, p_type, reason, expires_at, created_by):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO punishments (guild_id, user_id, type, reason, expires_at, created_by, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (str(guild_id), str(user_id), p_type, reason, expires_at, str(created_by), now)
        )
        row_id = cursor.lastrowid
        cursor.execute("SELECT * FROM punishments WHERE id=?", (row_id,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(row)

    def deactivate_punishments(self, guild_id, user_id, p_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE punishments SET is_active=0 WHERE guild_id=? AND user_id=? AND type=? AND is_active=1",
            (str(guild_id), str(user_id), p_type)
        )
        conn.commit()
        conn.close()

    # compute_hourly_rollup and get_health_rollup are now defined earlier as sync methods

    def create_ticket(self, guild_id, channel_id, user_id, subject):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO tickets (guild_id, channel_id, user_id, subject, created_at) VALUES (?, ?, ?, ?, ?)",
            (str(guild_id), str(channel_id), str(user_id), subject, now)
        )
        ticket_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(row)

    def get_ticket_by_channel(self, channel_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE channel_id=? AND status='open'", (str(channel_id),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def close_ticket(self, ticket_id, closed_by_id, transcript_json):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "UPDATE tickets SET status='closed', closed_by=?, closed_at=?, transcript_json=? WHERE id=?",
            (str(closed_by_id), now, transcript_json, ticket_id)
        )
        conn.commit()
        conn.close()

    # set_self_assignable_role and get_self_assignable_roles are now defined earlier as sync methods

    def get_user_achievements(self, guild_id, user_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_achievements WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def award_achievement(self, guild_id, user_id, achievement_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO user_achievements (guild_id, user_id, achievement_id, unlocked_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(guild_id, user_id, achievement_id) DO NOTHING",
            (str(guild_id), str(user_id), achievement_id, now)
        )
        conn.commit()
        conn.close()

    def add_mod_rule(self, guild_id, rule_type, pattern, action, reason, creator_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            """INSERT INTO moderation_rules (guild_id, type, pattern, action, reason, creator_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (str(guild_id), rule_type, pattern, action, reason, str(creator_id), now)
        )
        conn.commit()
        conn.close()

    def remove_mod_rule(self, rule_id, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM moderation_rules WHERE id=? AND guild_id=?", (rule_id, str(guild_id)))
        conn.commit()
        conn.close()

    def get_mod_rules(self, guild_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moderation_rules WHERE guild_id=? AND enabled=1", (str(guild_id),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create_event(self, guild_id, channel_id, creator_id, title, description, scheduled_at, reminder_minutes):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            """INSERT INTO events (guild_id, channel_id, creator_id, title, description, scheduled_at, reminder_minutes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(guild_id), str(channel_id), str(creator_id), title, description, float(scheduled_at), reminder_minutes, now)
        )
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return event_id

    def cancel_event(self, event_id, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute("UPDATE events SET cancelled_at=? WHERE id=? AND guild_id=?", (now, event_id, str(guild_id)))
        conn.commit()
        conn.close()

    def list_upcoming_events(self, guild_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "SELECT * FROM events WHERE guild_id=? AND scheduled_at > ? AND cancelled_at IS NULL ORDER BY scheduled_at ASC",
            (str(guild_id), now)
        )
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

    def get_reputation_count_today(self, guild_id, giver_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        cursor.execute(
            "SELECT COUNT(*) FROM reputation_events WHERE guild_id=? AND giver_id=? AND created_at >= ?",
            (str(guild_id), str(giver_id), start_of_day)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def check_reciprocal_reputation(self, guild_id, giver_id, receiver_id, window_hours):
        conn = self.get_connection()
        cursor = conn.cursor()
        window_start = time.time() - (window_hours * 3600)
        cursor.execute(
            "SELECT COUNT(*) FROM reputation_events WHERE guild_id=? AND giver_id=? AND receiver_id=? AND created_at >= ?",
            (str(guild_id), str(receiver_id), str(giver_id), window_start)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def add_reputation_event(self, guild_id, giver_id, receiver_id, reason):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO reputation_events (guild_id, giver_id, receiver_id, reason, created_at) VALUES (?, ?, ?, ?, ?)",
            (str(guild_id), str(giver_id), str(receiver_id), reason, now)
        )
        # Also increment the receiver's reputation in user_levels
        cursor.execute(
            "UPDATE user_levels SET reputation = reputation + 1, updated_at = ? WHERE guild_id=? AND user_id=?",
            (now, str(guild_id), str(receiver_id))
        )
        conn.commit()
        conn.close()

    def create_poll(self, guild_id, channel_id, creator_id, question, options_list, ends_at=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        options_json = json.dumps(options_list)
        cursor.execute(
            """INSERT INTO polls (guild_id, channel_id, creator_id, question, options, created_at, ends_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (str(guild_id), str(channel_id), str(creator_id), question, options_json, now, ends_at)
        )
        poll_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return poll_id

    def set_poll_message(self, poll_id, message_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE polls SET message_id=? WHERE id=?", (str(message_id), poll_id))
        conn.commit()
        conn.close()

    def cast_poll_vote(self, poll_id, user_id, option_index):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            "INSERT INTO poll_votes (poll_id, user_id, option_index, created_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(poll_id, user_id) DO UPDATE SET option_index=excluded.option_index, created_at=excluded.created_at",
            (poll_id, str(user_id), option_index, now)
        )
        conn.commit()
        conn.close()

    def close_poll(self, poll_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("UPDATE polls SET is_closed=1 WHERE id=?", (poll_id,))
        cursor.execute("SELECT * FROM polls WHERE id=?", (poll_id,))
        poll = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(poll) if poll else None

    def get_poll_results(self, poll_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT option_index, COUNT(*) as count FROM poll_votes WHERE poll_id=? GROUP BY option_index", (poll_id,))
        rows = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM poll_votes WHERE poll_id=?", (poll_id,))
        total = cursor.fetchone()[0]
        
        results = {row[0]: row[1] for row in rows}
        conn.close()
        return results, total
    def get_user_reputation(self, guild_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT reputation FROM user_levels WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

    def get_recent_thanks(self, guild_id, user_id, limit=5):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reputation_events WHERE guild_id=? AND receiver_id=? ORDER BY created_at DESC LIMIT ?",
            (str(guild_id), str(user_id), limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def log_moderation_action(self, guild_id, rule_id, message_id, actor_id, target_user_id, action, reason, username=None, content=None, metadata=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = time.time()
        cursor.execute(
            """
            INSERT INTO moderation_actions
            (guild_id, rule_id, message_id, actor_id, target_user_id, username, content, action, reason, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(guild_id),
                rule_id,
                str(message_id) if message_id is not None else None,
                str(actor_id) if actor_id is not None else None,
                str(target_user_id) if target_user_id is not None else None,
                str(username) if username is not None else None,
                str(content) if content is not None else None,
                str(action or ""),
                str(reason or ""),
                json.dumps(metadata or {}),
                now
            )
        )
        conn.commit()
        conn.close()

    def get_moderation_actions(self, guild_id, limit=50):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM moderation_actions
            WHERE guild_id=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (str(guild_id), int(limit))
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_user_streak(self, guild_id, user_id, streak_type="message", event_ts=None):
        ts = float(event_ts or time.time())
        today = datetime.utcfromtimestamp(ts).date()
        now_ts = time.time()

        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM user_streaks WHERE guild_id=? AND user_id=? AND streak_type=?",
            (str(guild_id), str(user_id), str(streak_type))
        )
        row = cursor.fetchone()

        current_count = 1
        best_count = 1
        last_active_day = today.isoformat()

        if row:
            prev_day_raw = row["last_active_day"]
            prev_day = None
            if prev_day_raw:
                try:
                    prev_day = datetime.strptime(prev_day_raw, "%Y-%m-%d").date()
                except Exception:
                    prev_day = None

            old_current = int(row["current_count"] or 0)
            old_best = int(row["best_count"] or 0)
            if prev_day == today:
                current_count = max(1, old_current)
            elif prev_day and (today - prev_day).days == 1:
                current_count = max(1, old_current + 1)
            else:
                current_count = 1
            best_count = max(old_best, current_count)

        cursor.execute(
            """
            INSERT INTO user_streaks
            (guild_id, user_id, streak_type, current_count, best_count, last_active_day, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(guild_id, user_id, streak_type) DO UPDATE SET
                current_count=excluded.current_count,
                best_count=excluded.best_count,
                last_active_day=excluded.last_active_day,
                updated_at=excluded.updated_at
            """,
            (
                str(guild_id),
                str(user_id),
                str(streak_type),
                int(current_count),
                int(best_count),
                last_active_day,
                now_ts
            )
        )
        conn.commit()
        conn.close()
        return {
            "guild_id": str(guild_id),
            "user_id": str(user_id),
            "streak_type": str(streak_type),
            "current_count": int(current_count),
            "best_count": int(best_count),
            "last_active_day": last_active_day,
            "updated_at": now_ts
        }

    def get_user_streak(self, guild_id, user_id, streak_type="message"):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_streaks WHERE guild_id=? AND user_id=? AND streak_type=?",
            (str(guild_id), str(user_id), str(streak_type))
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {
            "guild_id": str(guild_id),
            "user_id": str(user_id),
            "streak_type": str(streak_type),
            "current_count": 0,
            "best_count": 0,
            "last_active_day": None
        }

    def get_top_streaks(self, guild_id, streak_type="message", limit=10):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.user_id, s.current_count, s.best_count, s.last_active_day,
                   COALESCE(u.username, s.user_id) AS username,
                   COALESCE(u.avatar_url, '') AS avatar_url
            FROM user_streaks s
            LEFT JOIN user_levels u ON u.guild_id = s.guild_id AND u.user_id = s.user_id
            WHERE s.guild_id=? AND s.streak_type=?
            ORDER BY s.current_count DESC, s.best_count DESC, s.updated_at DESC
            LIMIT ?
            """,
            (str(guild_id), str(streak_type), int(limit))
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_guild_ids(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT guild_id FROM messages WHERE guild_id IS NOT NULL
            UNION
            SELECT guild_id FROM user_levels WHERE guild_id IS NOT NULL
            UNION
            SELECT guild_id FROM punishments WHERE guild_id IS NOT NULL
            UNION
            SELECT guild_id FROM health_metrics_rollups WHERE guild_id IS NOT NULL
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return [str(r[0]) for r in rows if r and r[0]]

    def get_expired_punishments(self, now_ts=None):
        threshold = float(now_ts or time.time())
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM punishments
            WHERE is_active=1 AND expires_at IS NOT NULL AND expires_at <= ?
            ORDER BY expires_at ASC
            """,
            (threshold,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def deactivate_punishment_by_id(self, punishment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE punishments SET is_active=0 WHERE id=?",
            (int(punishment_id),)
        )
        conn.commit()
        conn.close()

    def get_last_rollup_bucket(self, guild_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(bucket) FROM health_metrics_rollups WHERE guild_id=?",
            (str(guild_id),)
        )
        row = cursor.fetchone()
        conn.close()
        if row and row[0] is not None:
            return float(row[0])
        return None

    def reset_guild_levels(self, guild_id):
        now = time.time()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE user_levels
            SET xp_total=0,
                xp_current=0,
                level=0,
                updated_at=?
            WHERE guild_id=?
            """,
            (now, str(guild_id))
        )
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return int(affected or 0)

    def get_profile_activity_heatmap(self, guild_id, user_id, days=42):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        days = max(1, int(days))
        since_ts = (datetime.utcnow() - timedelta(days=days)).timestamp()
        cursor.execute(
            """
            SELECT strftime('%Y-%m-%d', datetime(created_at, 'unixepoch')) AS day,
                   COUNT(*) AS count
            FROM messages
            WHERE guild_id=? AND user_id=? AND created_at >= ? AND is_deleted=0
            GROUP BY day
            ORDER BY day ASC
            """,
            (str(guild_id), str(user_id), since_ts)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_guild_leaderboard(self, guild_id, period='all', limit=10):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT *, (ROW_NUMBER() OVER(ORDER BY xp_total DESC)) as rank FROM user_levels WHERE guild_id=? ORDER BY xp_total DESC LIMIT ?"
        cursor.execute(query, (str(guild_id), limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

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

    async def adjust_user_xp(self, guild_id, user_id, amount, formula):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Get current XP
        cursor.execute("SELECT xp_total FROM user_levels WHERE guild_id=? AND user_id=?", (str(guild_id), str(user_id)))
        row = cursor.fetchone()
        current_xp = row[0] if row else 0
        
        # 2. Add amount
        new_total_xp = max(0, current_xp + amount)
        
        # 3. Recalculate Level and Current XP using formula
        level, xp_current = self._compute_level_from_total(new_total_xp, formula)
        
        # 4. Update
        now = time.time()
        cursor.execute(
            """UPDATE user_levels SET xp_total=?, xp_current=?, level=?, updated_at=? 
               WHERE guild_id=? AND user_id=?""",
            (new_total_xp, xp_current, level, now, str(guild_id), str(user_id))
        )
        conn.commit()
        conn.close()
        return new_total_xp, level

    def update_message_xp(self, message_id, xp_gain):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE messages SET xp_gain=? WHERE message_id=?",
            (int(xp_gain), str(message_id))
        )
        conn.commit()
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

    def update_user_rank(self, guild_id, user_id):
        # Implementation of get_user_rank exists below
        return self.get_user_rank(guild_id, user_id)

    def add_xp_to_user_incremental(self, message, xp_gain, formula):
        conn = self.get_connection()
        cursor = conn.cursor()
        user_id = str(message.author.id)
        guild_id = str(message.guild.id)
        
        # 1. Get CURRENT state
        cursor.execute("SELECT xp_total FROM user_levels WHERE user_id=? AND guild_id=?", (user_id, guild_id))
        row = cursor.fetchone()
        current_xp = int(row[0] or 0) if row else 0
        
        # 2. ADD new XP
        new_total_xp = current_xp + xp_gain
        
        # 3. Calculate New Level from New Total
        level, xp_current = self._compute_level_from_total(new_total_xp, formula)
        
        # 4. UPSERT update
        data = {
            "user_id": user_id,
            "guild_id": guild_id,
            "username": message.author.name,
            "user_discriminator": message.author.discriminator,
            "avatar_url": str(message.author.display_avatar.url) if message.author.display_avatar else "",
            "xp_total": new_total_xp,
            "xp_current": xp_current,
            "level": level,
            "updated_at": time.time()
        }
        # Only increment message count if it's a new message being added
        # (Already handled by the caller logic usually, but we use COALESCE here)
        upsert_sql = f'''
            INSERT INTO user_levels (user_id, guild_id, username, user_discriminator, avatar_url, messages_total, xp_total, xp_current, level, updated_at)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                messages_total = user_levels.messages_total + 1,
                xp_total = excluded.xp_total,
                xp_current = excluded.xp_current,
                level = excluded.level,
                username = excluded.username,
                avatar_url = excluded.avatar_url,
                updated_at = excluded.updated_at
        '''
        cursor.execute(upsert_sql, (
            data["user_id"], data["guild_id"], data["username"], data["user_discriminator"], 
            data["avatar_url"], data["xp_total"], data["xp_current"], data["level"], data["updated_at"]
        ))
        conn.commit()
        conn.close()

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

        print(f"[MessageDB] Rebuilding user levels for guild {guild_id}...")
        
        # 1. First, update any messages that are missing xp_gain
        cursor.execute(
            "SELECT message_id FROM messages WHERE guild_id=? AND xp_gain=0 AND bot_message=0 AND is_deleted=0", 
            (str(guild_id),)
        )
        msg_ids = [r[0] for r in cursor.fetchall()]
        if msg_ids:
            print(f"[MessageDB] Generating XP for {len(msg_ids)} untracked messages...")
            updates = [(random.randint(int(xp_min), int(xp_max)), mid) for mid in msg_ids]
            cursor.executemany("UPDATE messages SET xp_gain=? WHERE message_id=?", updates)
            conn.commit()

        # 2. Get aggregated XP totals per user
        cursor.execute(
            """
            SELECT user_id, username, user_discriminator, avatar_url,
                   COUNT(*) as messages_total, 
                   SUM(content_length) as characters_total, 
                   SUM(word_count) as words_total, 
                   SUM(xp_gain) as xp_total,
                   MAX(created_at) as last_message_at
            FROM messages
            WHERE guild_id=? AND bot_message=0 AND is_deleted=0
            GROUP BY user_id
            """,
            (str(guild_id),)
        )
        
        users_processed = 0
        now = time.time()
        
        # Clear existing levels for this guild to ensure SoT rebuild
        # But we'll do an UPSERT to keep other servers intact
        for u in cursor:
            uid = u["user_id"]
            xp_total = int(u["xp_total"] or 0)
            level, xp_current = self._compute_level_from_total(xp_total, formula)
            
            data = {
                "user_id": uid,
                "guild_id": str(guild_id),
                "username": u["username"] or "",
                "user_discriminator": u["user_discriminator"] or "",
                "avatar_url": u["avatar_url"] or "",
                "messages_total": int(u["messages_total"] or 0),
                "characters_total": int(u["characters_total"] or 0),
                "words_total": int(u["words_total"] or 0),
                "xp_total": xp_total,
                "xp_current": xp_current,
                "level": level,
                "last_message_at": u["last_message_at"],
                "updated_at": now
            }
            # Internal upsert
            placeholders = ", ".join(["?"] * len(data))
            headers = ", ".join(data.keys())
            values = list(data.values())
            upsert_sql = f'''
                INSERT INTO user_levels ({headers}) VALUES ({placeholders})
                ON CONFLICT(user_id) DO UPDATE SET
                    guild_id=excluded.guild_id,
                    username=excluded.username,
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
            # Need a second cursor for the upsert while the first is iterating
            conn.execute(upsert_sql, values)
            users_processed += 1
            if users_processed % 100 == 0:
                conn.commit()

        conn.commit()
        conn.close()
        return users_processed

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
        if not getattr(message.author, "bot", False):
            try:
                self.msg_db.update_user_streak(message.guild.id, message.author.id, "message", message.created_at.timestamp())
            except Exception:
                pass

    async def on_message_edit(self, before, after):
        if not after.guild: return
        self.msg_db.log_message(after)

    async def on_message_delete(self, message):
        self.msg_db.mark_deleted(message.id)

    async def download_history_background(self, guild_id, status_tracker):
        guild = self.get_guild(int(guild_id))
        if not guild:
            status_tracker["status"] = "error"; status_tracker["error"] = "Guild not found"
            return
        
        status_tracker["status"] = "downloading"
        total_new_messages = 0
        
        # Get XP Rules
        xp_cfg = self.db.get_xp_config(str(guild_id))
        
        # 1. Deep Discovery
        channels_to_search = []
        for channel in guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.ForumChannel)):
                channels_to_search.append(channel)
                if hasattr(channel, 'archived_threads'):
                    try:
                        async for thread in channel.archived_threads(limit=None):
                            channels_to_search.append(thread)
                    except Exception: pass
        channels_to_search.extend(guild.threads)
        
        total_channels = len(channels_to_search)
        processed_channels = 0
        
        for channel in channels_to_search:
            try:
                processed_channels += 1
                status_tracker["progress_text"] = f"Filling gaps in {channel.name} ({processed_channels}/{total_channels})"
                
                if not channel.permissions_for(guild.me).read_message_history:
                    continue

                # GAP-FILLING Logic: Scan all history but filter by uniqueness
                # This ensures we find messages sent while bot was offline
                # even if it has logged newer messages recently.
                batch = []
                async for message in channel.history(limit=None, oldest_first=True):
                    if message.author.bot: continue
                    
                    # UNIQUE CHECK: Skip if message is already in ledger
                    # This prevents double-counting XP and protects manual edits.
                    if self.msg_db.has_message(message.id):
                        continue

                    # Generate random XP for this TRULY NEW message
                    xp_gain = random.randint(xp_cfg["xp_min"], xp_cfg["xp_max"])
                    data = self.msg_db.process_message_data(message, xp_gain=xp_gain)
                    batch.append(data)
                    
                    # ADDITIVE LEVELING: Only for this unique new message
                    self.msg_db.add_xp_to_user_incremental(message, xp_gain, xp_cfg["formula"])
                    
                    if len(batch) >= 50:
                        self.msg_db.batch_insert_messages(batch)
                        total_new_messages += len(batch)
                        status_tracker["total_downloaded"] = total_new_messages
                        batch = []
                        await asyncio.sleep(0.01)
                
                if batch:
                    self.msg_db.batch_insert_messages(batch)
                    total_new_messages += len(batch)
                    status_tracker["total_downloaded"] = total_new_messages
                    
            except Exception as e:
                print(f"[MessageLogger] Error in {channel.name}: {e}")
        
        status_tracker["status"] = "completed"
        status_tracker["progress_text"] = f"Success: Added {total_new_messages} new unique messages to history."
