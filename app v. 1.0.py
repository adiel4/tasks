import logging
import vininfo as vi
import requests
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5673559197:AAFrmQhxZTlFp0b_emwE8ZxzuAEgwa8AlUo'

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()
    vin = State()
    model = State()
    doc_type = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()

    await message.reply(
        "'Здравствуйте, вас приветствует бот. Пожалуйста введите свое имя. Чтобы отменить заявку введите команду 'Отменить'"
    )

@dp.message_handler(state='*', commands='отменить')
@dp.message_handler(Text(equals='отменить',ignore_case=True), state='*')
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    await state.finish()

    await message.reply('Заявка аннулирована.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply('Введите пожалуйсте VIN или номер кузова вашего автомобиля.')

@dp.message_handler(lambda message: len(message.text) != 17,state=Form.vin)
async def process_mark_invalid(message: types.Message):
    return await message.reply("VIN или номер кузова введены неверно! Попробуйте снова.")

@dp.message_handler(state=Form.vin)
@dp.message_handler(lambda message: len(message.text) == 17,state=Form.vin)
async def process_vin(message: types.Message,state: FSMContext):
    await Form.next()
    await state.update_data(vin=message.text)
    await message.reply('Введите марку и модель автомобиля.')

@dp.message_handler(state=Form.model)
async def process_model(message:types.Message,state: FSMContext):
    await Form.next()
    await  state.update_data(model=message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Возмещение убытка")
    markup.add("Оценка для страховой компании")
    await message.reply("Для каких целей вы используете услугу оценщиков?", reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["Оценка для страховой компании", "Возмещение убытка"],
                    state=Form.doc_type)
async def process_doc_type_invalid(message: types.Message):
    return await message.reply("Выберите цель.")

@dp.message_handler(state=Form.doc_type)
async def process_doc_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['doc_type'] = message.text
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Уважаемый,', md.bold(data['name'])),
                md.text('VIN:', md.bold(data['vin'])),
                md.text('Модель:', md.bold(data['model'])),
                md.text('Тип:', md.bold(data['doc_type'])),
                md.text('Ваша заявка в процессе. Благодарим за сотрудничество. Свяжемся с вами в ближайшее время'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Начать оформление заявки")
