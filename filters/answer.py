import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class Answer(BoundFilter):
    key = 'is_answer'

    def __init__(self, is_answer, *args, **kwargs):
        self.is_answer = is_answer

    async def check(self, message):
        if isinstance(message, CallbackQuery):
            text = message.data.lower()
        else:
            return False

        match = re.match('^answer_(\d|label|submit)$', text)

        if not match:
            return False

        return {'match': match.group(1)}
