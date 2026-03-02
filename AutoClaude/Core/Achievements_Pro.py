import sqlite3
import time
from typing import List, Dict
from Core.Command.Achievements import ACHIEVEMENTS

class AchievementsService:
    def __init__(self, msg_db):
        self.msg_db = msg_db

    def get_stats(self, guild_id: str) -> List[Dict]:
        """Returns all achievement milestones with the total count of earners for each."""
        conn = self.msg_db.get_connection()
        cursor = conn.cursor()
        
        results = []
        for ach in ACHIEVEMENTS:
            cursor.execute(
                "SELECT COUNT(*) FROM user_achievements WHERE guild_id=? AND achievement_id=?",
                (guild_id, ach["id"])
            )
            count = cursor.fetchone()[0]
            
            # Enrich with count and type
            results.append({
                **ach,
                "count": count,
                "icon": "trending-up" if ach.get("type") == "level" else "message-square"
            })
            
        conn.close()
        return results

    def get_earners(self, guild_id: str, achievement_id: str) -> List[Dict]:
        """Returns a detailed list of users who have earned a specific achievement."""
        conn = self.msg_db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT a.user_id, u.username, a.unlocked_at
            FROM user_achievements a
            LEFT JOIN user_levels u ON a.user_id = u.user_id AND a.guild_id = u.guild_id
            WHERE a.guild_id=? AND a.achievement_id=?
            ORDER BY a.unlocked_at DESC
            """,
            (guild_id, achievement_id)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{"user_id": r[0], "username": r[1] or "Unknown", "at": r[2]} for r in rows]

    async def check_user(self, guild_id: str, user_id: str):
        """Audit a specific user and award any milestones they've reached."""
        user_data = self.msg_db.get_user_level(guild_id, user_id)
        if not user_data: return
        
        current_level = int(user_data.get('level', 0))
        total_msgs = int(user_data.get('messages_total', 0))
        
        for ach in ACHIEVEMENTS:
            awarded = False
            if ach['type'] == "level" and current_level >= ach['threshold']:
                awarded = True
            elif ach['type'] == "messages" and total_msgs >= ach['threshold']:
                awarded = True
                
            if awarded:
                self.msg_db.award_achievement(guild_id, user_id, ach['id'])
