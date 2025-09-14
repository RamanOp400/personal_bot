import sqlite3
import json
import datetime
from typing import List, Dict, Optional

class ChatMemory:
    def __init__(self, db_path: str = "chat_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                context TEXT
            )
        ''')
        
        # Create user_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_name TEXT,
                preferred_avatar TEXT,
                personality_notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, session_id: str, user_message: str, bot_response: str, context: str = ""):
        """Save a conversation turn to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, user_message, bot_response, context)
            VALUES (?, ?, ?, ?)
        ''', (session_id, user_message, bot_response, context))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, bot_response, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts and reverse to get chronological order
        history = []
        for row in reversed(results):
            history.append({
                'user': row[0],
                'bot': row[1],
                'timestamp': row[2]
            })
        
        return history
    
    def save_user_preferences(self, session_id: str, user_name: str = "", preferred_avatar: str = "", personality_notes: str = ""):
        """Save or update user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (session_id, user_name, preferred_avatar, personality_notes, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (session_id, user_name, preferred_avatar, personality_notes))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, session_id: str) -> Dict:
        """Get user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_name, preferred_avatar, personality_notes
            FROM user_preferences
            WHERE session_id = ?
        ''', (session_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_name': result[0] or "",
                'preferred_avatar': result[1] or "",
                'personality_notes': result[2] or ""
            }
        return {'user_name': "", 'preferred_avatar': "", 'personality_notes': ""}
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Get a summary of the conversation for context"""
        history = self.get_conversation_history(session_id, 5)
        if not history:
            return ""
        
        summary = "Recent conversation context:\n"
        for turn in history[-3:]:  # Last 3 exchanges
            summary += f"User: {turn['user']}\nBot: {turn['bot']}\n"
        
        return summary
