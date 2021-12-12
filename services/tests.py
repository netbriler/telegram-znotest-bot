from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db.models import Test, Chapter
from utils.misc.logging import logger


async def get_test(session: AsyncSession, id: int) -> Test:
    sql = select(Test).where(Test.id == id)
    query = await session.execute(sql)

    test = query.scalar_one_or_none()

    return test


async def get_tests(session: AsyncSession, chapter_id: int) -> list[Test]:
    sql = select(Test).where(Test.chapter_id == chapter_id)
    query = await session.execute(sql)

    return [t for t, in query]


async def create_test(session: AsyncSession, name: str, chapter_id: int) -> Test:
    new_test = Test(name=name, chapter_id=chapter_id)

    session.add(new_test)
    await session.commit()

    logger.info(f'New test {new_test}')

    return new_test
