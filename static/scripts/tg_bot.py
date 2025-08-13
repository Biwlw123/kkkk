import asyncio
import random
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, time
import pytz

TOKEN = "7311871127:AAHC5x_gdomqcoGd6crSQF9j7CSvyI6dKhU"
BASE_LINK = f"https://t.me/driveeeX_bot?start="

# Варианты сообщений
MESSAGES = [
    "🔔 Ваша машина ждет заботы! Запишитесь в сервис.",
    "🚨 СТОП! Немедленно посетите сервис DriveX Garage!"
]

# Хранилище подписчиков (в реальном проекте используйте БД)
subscribers = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка перехода по ссылке"""
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        await update.message.reply_text(
            "✅ Вы подписаны на уведомления!\n"
            f"Ваша ссылка для друзей: {BASE_LINK}{chat_id}"
        )
    else:
        await update.message.reply_text("Вы уже подписаны!")

async def send_daily_notifications():
    """Ежедневная рассылка"""
    bot = Bot(token=TOKEN)
    for chat_id in subscribers:
        try:
            message = random.choice(MESSAGES)
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Ошибка для {chat_id}: {e}")

async def daily_task():
    """Фоновая задача"""
    while True:
        now = datetime.now(pytz.timezone("Europe/Moscow"))
        if now.hour == 12 and now.minute == 00:  # Рассылка в 12:00
            await send_daily_notifications()
            await asyncio.sleep(60)
        await asyncio.sleep(30)

if __name__ == "__main__":
    # Настройка бота
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Запуск задач
    loop = asyncio.get_event_loop()
    loop.create_task(daily_task())
    
    # Старт
    print(f"✨ Бот активен! Ссылка для подписки: {BASE_LINK}123")
    app.run_polling()
