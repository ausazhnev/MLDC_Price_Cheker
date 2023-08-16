# Телеграмм бот для проверки изменения цен

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
from app import keyboards as kb
from app import api_query as aq
from app import db_query as dq
from datetime import date


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет {message.from_user.first_name}\n'
                           f'Я бот по проверки измения цен. Буду помогать тебе в работе.',
                           reply_markup=kb.main_kb)

@dp.message_handler()
async def text_processing(message: types.Message) -> None:
    print(message.text)
    if message.text == 'Проверить цены.':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Начинаю обработку цен.\n'
                                    'Это может занять время. Пожалуйста подождите.',
                                reply_markup=kb.main_kb)
        product_list = dq.get_product_list()
        if type(product_list) == list:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Список товаров получен...')
            # Проверить есть в списке дата актуальности отличающаяся от сегодня.
            if dq.check_act_date(str(date.today())):
                for elem in product_list:
                    # Проверяем актуальность даты
                    if str(date.today()) != elem[3]:
                        # Если дата не актуальна, то проверяем изменилась ли цена
                        answer = aq.get_price(elem[1], elem[2])
                        print(type(answer))
                        if type(answer) is float and float(answer) != float(elem[4]):
                            await bot.send_message(chat_id=message.from_user.id,
                                                   text=f'Стоимость {elem[1]} {elem[2]}, изменилась и составляет {answer}')
                            # Внести изменения в базу, записать новую ценц
                            dq.set_new_price(elem[0], answer)
                    dq.set_act_date(elem[0], str(date.today()))
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Обработка данных завершина')
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Все цены на сегодня уже проверены. Повторная проверка не требуется.')
        elif type(product_list) == str:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=product_list)
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Попробуйте повторить попытку еще раз.',
                                   reply_markup=kb.main_kb)
    else:
         await bot.send_message(chat_id=message.from_user.id,
                                text='Я не понимаю, воспользутесь кнопками меню.',
                                   reply_markup=kb.main_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
