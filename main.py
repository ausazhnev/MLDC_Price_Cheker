# Телеграмм бот для проверки изменения цен

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет {message.from_user.first_name}\n'
                           f'Я бот по проверки измения цен. Буду помогать тебе в работе.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)