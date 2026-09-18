import asyncio
import feedparser
import os
import sys
from aiogram import Bot

# Настройки безопасности: сервер сам подставит ключи из секретной панели
TOKEN = os.getenv("BOT_TOKEN")
MY_CHAT_ID = os.getenv("TELEGRAM_ID")
RSS_URL = "https://habr.com"

if not TOKEN or not MY_CHAT_ID:
    print("Error: BOT_TOKEN or TELEGRAM_ID environment variables are not set!")
    sys.exit(1)

bot = Bot(token=TOKEN)
seen_tasks = set()

async def check_orders():
    print("Checking freelance feed...")
    feed = feedparser.parse(RSS_URL)
    
    # При самом первом запуске запоминаем текущие заказы, чтобы не спамить старыми
    is_first_run = len(seen_tasks) == 0
    
    for entry in reversed(feed.entries):
        task_id = entry.id
        if task_id not in seen_tasks:
            seen_tasks.add(task_id)
            
            # Если это новый заказ, пришедший после запуска бота
            if not is_first_run:
                title = entry.title
                link = entry.link
                message = (
                    f"🎯 **NEW FREELANCE JOB FOUND!**\n\n"
                    f"📋 **Task:** {title}\n\n"
                    f"🔗 **Link:** {link}\n"
                    f"----------------------------------------\n"
                    f"💡 *Be the first to apply!*"
                )
                try:
                    await bot.send_message(chat_id=MY_CHAT_ID, text=message, parse_mode="Markdown")
                    print(f"[+] Notification sent: {title}")
                except Exception as e:
                    print(f"Failed to send message: {e}")

async def main():
    print("Freelance Hunter Bot is now running autonomously in the cloud!")
    while True:
        try:
            await check_orders()
        except Exception as e:
            print(f"Error checking feed: {e}")
        # Проверяем биржу каждые 10 минут (600 секунд)
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
