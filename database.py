import sqlite3
import asyncio
from datetime import datetime, timedelta
from config import logger, executor
import aiosqlite


def init_db():
    with sqlite3.connect('vpn_bot.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            username TEXT,
            subscription_status TEXT,
            start_date TEXT,
            end_date TEXT,
            balance REAL,
            access_level TEXT
        )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            price REAL NOT NULL,
            link TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            config_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (config_id) REFERENCES configs (id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            date TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            chat_id INTEGER,
            photo_file_id TEXT,
            status TEXT,
            amount REAL
            )
        ''')
        conn.commit()

async def execute_db(query: str, params=(), fetchone=False):
    def execute_db_sync(query, params, fetchone):
        with sqlite3.connect('vpn_bot.db') as conn:
            c = conn.cursor()
            try:
                c.execute(query, params)
                return c.fetchone() if fetchone else c.fetchall()
            except sqlite3.Error as e:
                logger.error(f"Database error: {e}")
                return None

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, execute_db_sync, query, params, fetchone)
