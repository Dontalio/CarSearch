from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Command, CommandObject
from  aiogram.types import Message, CallbackQuery
from get_cars.search_selen.main import search_car
from asyncio import sleep as async_sleep
from get_cars.tg_bot_car.utility.main_utils import ValidSearch, auto_dell_msg
main_router = Router()

@main_router.message(F.chat.type == ChatType.PRIVATE)
async def cmd_start(message : Message):
    print(f" was start <start> with {message}")
    await message.answer(text='Не пиши в личку боту. Он работает только в чатах')

@main_router.message(CommandStart())
async def cmd_start(message : Message):
    print(f" was start <start> with {message}")
    msg = await message.answer(text='В этом чате я работаю')
    await auto_dell_msg(msg)

@main_router.message(Command('ping'))
async def cmd_menu(message : Message):
    msg = await message.answer(text='pong')
    await auto_dell_msg(msg)

@main_router.message(Command('search_car'))
async def cmd_search_by_id(message : Message, command : CommandObject):
    try:
        args = message.text.split(' ')[1]
    except Exception as e:
        print(f'ERROR in search_car for split ({e})')
        msg_1 = await  message.reply(text='неверный формат команды или номер авто НЕ на кириллице.\n'
                                   'введите команду в формате\n'
                                   '<b>/search_car АА999А43</b>')
        await auto_dell_msg(msg_1)
        return

    await async_sleep(0.5)

    if not ValidSearch.can_use():
        msg_1 = await message.answer(text=f'<b>Слишком много запросов. ОПопробуйте через 10 секунд...</b>')
        await auto_dell_msg(msg_1, 30)
        return  # закончим работу.
    try:
        ValidSearch.can_use() # отмечаемся об имспользовании. Флаг нам уже не нужен
        res = await search_car(plate=args)
        print(f'find car by number {args} -- {res}')
    except Exception as e:
        print(f'ERROR in search_car_by_id is {e}')
        return

    if res is not None:
        value_str = "".join([f'<b>{x[0]} </b>: {x[1]}\n' for x in res])
        msg1 = await message.reply(text=f'''ваш номер <b>{args.upper()}</b>:\n{value_str}''')
    else:
        msg1 = await message.reply(text=f'информация не найдена по номеру {args.upper()}')





