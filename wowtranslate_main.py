import logging
from aiogram import Dispatcher, executor, Bot, types
from googletrans import Translator
from oxford_funktions import *
import settings
translator = Translator()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Assalomu alaykum men bepul, super tarjimon botman!\nMen istalgan tildagi so`zni inglizchaga, inglizchadan o`zbekchaga tarjima qilib beraman. \nTarjima qilinadigan so`z yoki gapingizni yozing.')

# @dp.message_handler(command='help')
# async def get_help(message: types.Message):
#     await message.reply('Biror muammo bormi?')

@dp.message_handler()
async def tarjimon(message: types.Message):
    print(message)
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest = 'en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions: \n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so`z topilmadi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
