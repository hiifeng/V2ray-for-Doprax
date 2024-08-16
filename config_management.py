from database import execute_db

async def add_config(name: str, location: str, price: float, link: str):
    await execute_db("INSERT INTO configs (name, location, price, link) VALUES (?, ?, ?, ?)", (name, location, price, link))

async def get_all_configs():
    return await execute_db("SELECT * FROM configs")

async def get_config(config_id: int):
    return await execute_db("SELECT * FROM configs WHERE id = ?", (config_id,), fetchone=True)
