from datetime import datetime, timedelta
from database import execute_db

async def add_user(username: str, chat_id: int, subscription_status='inactive', balance=0.0, duration_days=30, access_level='User'):
    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_date = (datetime.now() + timedelta(days=duration_days)).strftime('%Y-%m-%d %H:%M:%S')
    await execute_db(
        "INSERT OR IGNORE INTO users (username, chat_id, subscription_status, start_date, end_date, balance, access_level) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (username, chat_id, subscription_status, start_date, end_date, balance, access_level)
    )

async def get_user(username: str):
    return await execute_db("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)

async def update_user(username: str, **kwargs):
    updates = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    query = f"UPDATE users SET {updates} WHERE username = ?"
    await execute_db(query, tuple(kwargs.values()) + (username,))
