import logging
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
cars_json = requests.get('https://cars-base.ru/api/cars?full=1').json()


# States
class Form(StatesGroup):
    name = State()
    mark = State()
    mark_index = 0
    model = State()
    doc_type = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    # Set state

    await Form.name.set()

    await message.reply(
        "Здравствуйте, вас приветствует бот. Пожалуйста введите свое имя. Чтобы отменить заявку введите команду 'Отменить'")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='отменить')
@dp.message_handler(Text(equals='отменить', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Заявка аннулирована.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Введите пожалуйста марку вашего автомобиля.")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: message.text.lower() not in [cars_json[i]['id'].lower().replace('_', ' ') for i in
                                                                 range(len(cars_json))], state=Form.mark)
async def process_mark_invalid(message: types.Message):
    return await message.reply("Такая марка машины не найдена попробуйте снова!")


@dp.message_handler(state=Form.mark)
@dp.message_handler(lambda message: message.text.lower() in [cars_json[i]['id'].lower().replace('_', ' ') for i in
                                                             range(len(cars_json))], state=Form.mark)
async def process_mark(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(mark=message.text)
    Form.mark_index = [i for i in range(len(cars_json)) if cars_json[i]['id'].lower().replace('_', ' ') == message.text.lower().replace('_', ' ')][0]
    await message.reply("Введите пожалуйста модель вашего автомобиля.")


@dp.message_handler(
    lambda message: message.text.lower() not in [cars_json[Form.mark_index]['models'][i]['id'].lower() for i in
                                                 range(len(cars_json[Form.mark_index]['models']))], state=Form.model)
async def process_model_invalid(message: types.Message):
    return await message.reply("Такая модель машины не найдена попробуйте снова!")


@dp.message_handler(state=Form.model)
@dp.message_handler(
    lambda message: message.text.lower() in [cars_json[Form.mark_index]['models'][i]['id'].lower() for i in
                                             range(len(cars_json[Form.mark_index]['models']))], state=Form.model)
async def process_model(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(model=message.text)
    # Configure ReplyKeyboardMarkup
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
        data['gender'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Уважаемый,', md.bold(data['name'])),
                md.text('Марка:', md.bold(data['mark'])),
                md.text('Модель:', md.bold(data['model'])),
                md.text('Тип:', data['gender']),
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
