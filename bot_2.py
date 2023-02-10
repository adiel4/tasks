from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup

bot = Bot(token='5673559197:AAFrmQhxZTlFp0b_emwE8ZxzuAEgwa8AlUo')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне VIN или номер кузова и я попробую выслать его параметры и ссылку на каталог его деталей!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю тебе много интересной инфы!")


@dp.message_handler()
async def echo_message(msg: types.Message):

    url = 'https://www.ilcats.ru/?vin=' + msg.text + '&VinAction=Search'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        vin_info = soup.find('div', {'class': 'VinInfo'})
        vin_table = vin_info.find('table')
    except:
        await bot.send_message(msg.from_user.id,"Введен некорректный вин или номер кузова")
        return None
    vin_data = {}
    for row in vin_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            key = cells[0].text.strip().replace('\xa0', '')
            value = cells[1].text.strip().replace('\xa0', '')
            vin_data[key] = value
            await bot.send_message(msg.from_user.id, key + ' ' + value)
        elif len(cells) ==1:
            url_info = soup.find('td',{'class': 'Center'})
            link = url_info.contents
            await bot.send_message(msg.from_user.id, 'Ссылка на полный каталог деталей для данной машины')
            await bot.send_message(msg.from_user.id, 'https://www.ilcats.ru'+str(link[0]).split('"')[1])


if __name__ == '__main__':
    executor.start_polling(dp)
