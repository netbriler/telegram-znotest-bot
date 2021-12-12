import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from services.tests import get_test


class Test(BoundFilter):
    key = 'is_test'

    def __init__(self, is_test, *args, **kwargs):
        self.is_test = is_test

    async def check(self, message):
        if isinstance(message, CallbackQuery):
            text = message.data.lower()
        else:
            return False

        session = message.bot.get('session')

        match = re.match('^test_(\d+)$', text)
        if not match:
            return False

        test = await get_test(session, match.group(1))

        if not test:
            return False

        return {'test': test}
