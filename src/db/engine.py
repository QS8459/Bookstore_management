from src.configuration import async_session_maker

async def get_async_session() -> None:

    async with async_session_maker() as session:
        yield session