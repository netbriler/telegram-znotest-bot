import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from services.questions import get_question


class Question(BoundFilter):
    key = 'is_question'

    def __init__(self, is_question, *args, **kwargs):
        self.is_question = is_question

    async def check(self, message):
        if isinstance(message, CallbackQuery):
            text = message.data.lower()
        else:
            return False

        session = message.bot.get('session')

        match = re.match('^question_(\d+)(_(\w+))?$', text)

        if not match:
            return False

        question = await get_question(session, match.group(1))

        print(match.group(3), match.group(1), question)

        if not question:
            return False

        return {'question': question, 'action': match.group(3)}
