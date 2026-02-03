from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Command, CommandObject
from  aiogram.types import Message, CallbackQuery
from get_cars.search_selen.main import search_car
from asyncio import sleep as async_sleep

main_router = Router()

@main_router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def cmd_start(message : Message):
    print(f" was start <start> with {message}")
    await message.answer(text='Не пиши в личку боту. Он не будет искать машину.!')

@main_router.message(CommandStart())
async def cmd_start(message : Message):
    print(f" was start <start> with {message}")
    await message.answer(text='В этом чате я работаю')

@main_router.message(Command('ping'))
async def cmd_menu(message : Message):
    await message.answer(text='pong')

@main_router.message(Command('search_car'))
async def cmd_search_by_id(message : Message, command : CommandObject):
    try:
        args = message.text.split(' ')[1]
    except Exception as e:
        print(f'ERROR in search_car for split ({e})')
        args = 0
        await  message.answer(text='неверный формат команды или номер авто НЕ на кириллице.\n'
                                   'введите команду в формате\n'
                                   '<b>/search_car АА999А43</b>')
        return

    msg_del = message.answer(text='обработка...') # после удалим. Отслеживание долгого ответа.
    await async_sleep(0.5)
    try:
        res = search_car(plate=args)
        print(f'find car by number {args} -- {res}')
    except Exception as e:
        print(f'ERROR in search_car_by_id')
        return

    if res is not None:
        await message.answer(text=f'ваш номер <b>{res.strip()}</b>')
    else:
        await message.answer(text=f'информация не найдена по номеру {args}')

    # await msg_del.


