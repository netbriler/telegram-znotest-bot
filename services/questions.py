from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db.models import Question
from utils.misc.logging import logger


async def count_questions(session: AsyncSession, test_id: int):
    sql = select([func.count()]).where(
        and_(Question.test_id == test_id, Question.test_type.in_(['4x1', '4x4']))).select_from(Question)
    query = await session.execute(sql)

    return query.scalar()


async def get_question(session: AsyncSession, id: int) -> Question:
    sql = select(Question).where(Question.id == id)
    query = await session.execute(sql)

    question = query.scalar_one_or_none()

    return question


async def get_questions(session: AsyncSession, test_id: int, exclude_ids=None) -> list[Question]:
    if exclude_ids is None:
        exclude_ids = list()

    sql = select(Question).where(
        and_(Question.test_id == test_id, Question.test_type.in_(['4x1', '4x4']), ~Question.id.in_(exclude_ids)))
    query = await session.execute(sql)

    return [t for t, in query]


async def create_question(session: AsyncSession, test_id: int, question_image: str = None, question: str = None,
                          explanation_image: str = None, explanation: str = None, has_answer: bool = False,
                          _type: str = None, test_type: str = None, answer_test: str = None, input_count: int = None,
                          answer1: str = None,
                          answer2: str = None) -> Question:
    new_question = Question(test_id=test_id, question_image=question_image, question=question,
                            explanation_image=explanation_image, explanation=explanation, has_answer=has_answer,
                            type=_type, test_type=test_type, answer_test=answer_test, input_count=input_count,
                            answer1=answer1, answer2=answer2)

    session.add(new_question)
    await session.commit()

    logger.info(f'New question {new_question}')

    return new_question
