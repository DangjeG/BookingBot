# todo сделать нормальное общение с ботом

from aiogram import Bot, Dispatcher, executor, types


class bot_controller:
    API_TOKEN = '5903687838:AAFciAPwabn0gSzfejp-YCkeaHOdeA9O2zI'

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)

    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)