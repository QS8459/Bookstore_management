import src.main as main


async def get_async_session() -> None:

    async with main.async_session_maker() as session:
        yield session