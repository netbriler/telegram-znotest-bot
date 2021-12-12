import asyncio
import json

from data.config import DIR
from services.chapters import create_chapter
from services.questions import create_question
from services.tests import create_test
from utils.db.base import create_async_database
from utils.misc.logging import logger


async def main():
    logger.info('Load data startup')

    session = await create_async_database()

    with open(DIR / 'mathematics.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for chapter in data:
            new_chapter = await create_chapter(session, chapter['name'])

            for page in chapter['pages']:
                new_test = await create_test(session, page['name'], new_chapter.id)
                await asyncio.sleep(1)

                for question in page['questions']:
                    del question['id']
                    print(await create_question(session, new_test.id, **question))


asyncio.run(main())
