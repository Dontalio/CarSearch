import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BotSet as BS


'''
Для создания бота
'''

car_bot = Bot(token=BS.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
admins = [int(admin_id) for admin_id in BS.ADMINS.split(',')]
logger = logging.getLogger(__name__)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')