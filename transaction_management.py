from datetime import datetime
from database import execute_db

async def add_transaction(username: str, amount: float, transaction_type: str):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await execute_db("INSERT INTO transactions (username, amount, transaction_type, date) VALUES (?, ?, ?, ?)", 
                     (username, amount, transaction_type, date))

async def get_all_transactions():
    return await execute_db("SELECT * FROM transactions ORDER BY date DESC")


async def update_receipt_status(status: str, id: int):
    await execute_db("UPDATE receipts SET status = ? WHERE id = ?",(status, id))
