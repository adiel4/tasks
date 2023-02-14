from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time

TOKEN = '5825700109:AAG71DAGnQUWzsVsTEU8jXQAt4-CbDh-VfQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет Сачи! Это твой личный бот для напоминаний! Он может писать тебе в определенное время и напоминать об определенных вещах.')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Если напишешь что нибудь мне я ничего не отвечу. Будут доработки.")

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=False)
    