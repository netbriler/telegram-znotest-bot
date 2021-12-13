import hashlib
from time import time

from loader import bot


def generate_inline_id(query: str):
    return hashlib.md5(f'{query}{time()}'.encode()).hexdigest()


async def clean_messages(state, message):
    async with state.proxy() as data:
        if 'delete_messages' not in data:
            data['delete_messages'] = list()

        for message_id in data['delete_messages']:
            try:
                await bot.delete_message(message.chat.id, message_id)
            except:
                pass

        data['delete_messages'] = list()
