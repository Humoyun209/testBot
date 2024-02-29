import json
import asyncio
from aiogram import Bot, Dispatcher, types, filters
from main import get_result


bot = Bot(token="6154724599:AAEt6CqnT9di-_kKtucwLzWAFQWvW0erj4w")
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Бот работает...")


@dp.message()
async def worker(message: types.Message):
    try:
        data = json.loads(message.text)
        print(data)
        result = json.dumps(
            get_result(data.get("dt_from"), data.get("dt_upto"), data.get("group_type"))
        )
        await message.answer(result)
    except Exception as e:
        await message.answer("Данные неправильно отправлены...")


if __name__ == "__main__":
    asyncio.run(dp.run_polling(bot))
