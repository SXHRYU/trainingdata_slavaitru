from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from cvat_utils import read_token, read_xlsx
from to_excel import excel_creation_main


# Need to create file "token" with token from @BotFather
bot = Bot(token=read_token("token"))
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message: types.Message):
    excel_creation_main()
    cvat_users = read_xlsx("cvat_users.xlsx")
    await message.answer_document(cvat_users, caption="cvat_users.xlsx")

executor.start_polling(dp, skip_updates=True)
