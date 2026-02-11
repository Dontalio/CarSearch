import asyncio
import time
from  aiogram.types import Message



class ValidSearch:
    LAST_TIME = time.time() - 9 # для более быстрого тестирования без ожидания после запуска.

    @classmethod
    def can_use(cls) -> bool:
        '''запоминает свой вызов и вернёт True если вызов был менее 10 сек назад.
        в случае возвращения True обновит счётчик'''
        if abs(time.time() - cls.LAST_TIME) > 10:
            cls.LAST_TIME = time.time()
            return True
        else:
            return False

async def auto_dell_msg(msg : Message, time_sec : int = 10):
    await asyncio.sleep(time_sec)
    await msg.delete()
    print(f"was dell msg : {msg}")
