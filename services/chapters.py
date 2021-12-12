from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db.models import Chapter
from utils.misc.logging import logger


async def get_chapter(session: AsyncSession, id: int) -> Chapter:
    sql = select(Chapter).where(Chapter.id == id)
    query = await session.execute(sql)

    chapter = query.scalar_one_or_none()

    return chapter


async def get_chapters(session: AsyncSession) -> list[Chapter]:
    sql = select(Chapter).order_by(Chapter.id.asc())
    query = await session.execute(sql)

    return [c for c, in query]


async def create_chapter(session: AsyncSession, name: str) -> Chapter:
    new_chapter = Chapter(name=name)

    session.add(new_chapter)
    await session.commit()

    logger.info(f'New chapter {new_chapter}')

    return new_chapter
