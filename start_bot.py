import asyncio
from create_bot import *
from aiogram.types import BotCommand, BotCommandScopeDefault
from tg_bot_car.handlers.handlers import main_router



def include_routers():
        dp.include_routers(main_router)
        print(f'роутеры успешно подключены')

async def set_commands():
    '''принимает словарь с командами'''
    func_list = BS.FUNC_LIST
    commands = []
    print(func_list)
    print(type(func_list))
    for command, descript in func_list.items():
        commands.append(BotCommand(command=command, description=descript))
    print("команды меню бота:", *commands, sep=' || ')
    await court_bot.set_my_commands(commands, BotCommandScopeDefault())
    print('SUCCES for SET COMMANDS')

async def main():
    '''основной асинхронный цикл бота'''
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start() # планировка и запуск задачи
    include_routers()  # запускаем все роутеры
    await court_bot.delete_webhook(
        drop_pending_updates=True)  # отключаем автообновление в окружении (skip_updates=True )
    await set_commands()  # сначала опеределим настройки бота (меню)
    await dp.start_polling(court_bot)  # запуск поллинга (опроса АПИ TG)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот выключен')