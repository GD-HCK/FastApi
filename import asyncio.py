import asyncio
from concurrent.futures import ThreadPoolExecutor

# Simulate a blocking database call
def fetch_burgers_from_db(count: int):
    # Replace this with actual database fetching logic
    return [{"id": i, "name": f"Burger {i}"} for i in range(1, count + 1)]

async def get_burgers(count: int):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        burgers = await loop.run_in_executor(pool, fetch_burgers_from_db, count)
    print(f"Got {len(burgers)} burgers")
    return burgers

async def g():
    await get_burgers(2000)
    await get_burgers(1000)

if __name__ == "__main__":
    asyncio.run(g())