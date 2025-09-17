import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from parsing import get_schedule

from datetime import datetime

dp = Dispatcher()


time = ["08:00-09:35", "09:45-11:20","11:30-13:05", "13:45-15:20", "15:30-17:05", "17:15-18:50", "19:00-20:25", "20:35-22:00", "22:10-23:35"]


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("👋 Привет Руслана!", reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📚 Расписание на сегодня")],[KeyboardButton(text="📅 Расписание на завтра")],[ KeyboardButton(text="🗓 Расписание на неделю")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие"))


@dp.message(F.text == "📚 Расписание на сегодня")
async def schedule_today(message: Message) -> None:
    await message.answer("⏳ Подождите, идет загрузка...")
    
    schedule = get_schedule()

    tosday = datetime.today().weekday()

    schedule_with_time = []
    for i, subject in enumerate(schedule[tosday]):
        if i < len(time):
            if "Нет пары" in subject:
                schedule_with_time.append(f"🕐 {time[i]} - ❌ {''.join(subject)}")
            else:
                schedule_with_time.append(f"🕐 {time[i]} - 📖 {''.join(subject)}")
        else:
            schedule_with_time.append(" ".join(subject))

    await message.answer("📚 Расписание на сегодня:\n" + "\n\n".join(schedule_with_time))


@dp.message(F.text == "📅 Расписание на завтра")
async def schedule_tomorrow(message: Message) -> None:
    await message.answer("⏳ Подождите, идет загрузка...")
    
    schedule = get_schedule()
    today = datetime.today().weekday()
    
    if today == 6:  # Воскресенье
        tomorrow = 0  # Понедельник
    elif today == 5:  # Суббота
        tomorrow = 0  # Понедельник
    else:
        tomorrow = today + 1

    schedule_with_time = []
    for i, subject in enumerate(schedule[tomorrow]):
        if i < len(time):
            if "Нет пары" in subject:
                schedule_with_time.append(f"🕐 {time[i]} - ❌ {''.join(subject)}")
            else:
                schedule_with_time.append(f"🕐 {time[i]} - 📖 {''.join(subject)}")
        else:
            schedule_with_time.append(" ".join(subject))

    await message.answer("📅 Расписание на завтра:\n" + "\n\n".join(schedule_with_time))


@dp.message(F.text == "🗓 Расписание на неделю")
async def schedule_week(message: Message) -> None:
    await message.answer("⏳ Подождите, идет загрузка...")
    
    schedule = get_schedule()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    
    week_schedule = []
    for day_idx, day_name in enumerate(days):
        week_schedule.append(f"📅 {day_name}:")
        for i, subject in enumerate(schedule[day_idx]):
            if i < len(time):
                if "Нет пары" in subject:
                    week_schedule.append(f"🕐 {time[i]} - ❌ {''.join(subject)}")
                else:
                    week_schedule.append(f"🕐 {time[i]} - 📖 {''.join(subject)}")
            else:
                week_schedule.append(" ".join(subject))
        week_schedule.append("")

    await message.answer("🗓 Расписание на неделю:\n" + "\n".join(week_schedule))


async def main() -> None:

    load_dotenv()
    TOKEN = getenv("TOKEN")

   

    
    bot = Bot(token=TOKEN) # pyright: ignore[reportArgumentType]

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())