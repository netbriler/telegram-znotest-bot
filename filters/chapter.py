import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from services.chapters import get_chapter


class Chapter(BoundFilter):
    key = 'is_chapter'

    def __init__(self, is_chapter, *args, **kwargs):
        self.is_chapter = is_chapter

    async def check(self, message):
        if isinstance(message, CallbackQuery):
            text = message.data.lower()
        else:
            return False

        session = message.bot.get('session')

        match = re.match('^chapter_(\d+)$', text)
        if not match:
            return False

        chapter = await get_chapter(session, match.group(1))

        if not chapter:
            return False

        return {'chapter': chapter}
