from datetime import datetime
from database import execute_db

async def add_order(username: str, config_id: int):
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await execute_db("INSERT INTO orders (username, config_id, order_date) VALUES (?, ?, ?)", (username, config_id, order_date))

async def get_user_orders(username: str):
    return await execute_db("""
        SELECT o.id, c.name, c.location, c.price, o.order_date 
        FROM orders o 
        JOIN configs c ON o.config_id = c.id 
        WHERE o.username = ?
    """, (username,))
