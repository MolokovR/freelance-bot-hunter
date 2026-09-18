import asyncio
import feedparser
import os
import sys
from aiogram import Bot

# Берутся настройки из секретных переменных сервера
TOKEN = os.getenv("BOT_TOKEN")
MY_CHAT_ID = os.getenv("TELEGRAM_ID")

if not TOKEN or not MY_CHAT_ID:
    print("Error: BOT_TOKEN or TELEGRAM_ID environment variables are not set!")
    sys.exit(1)

# Список всех RSS-лент крупнейших бирж СНГ
FEEDS = {
    "Habr Freelance": "https://habr.com",
    "Freelance.ru": "https://freelance.ru",
    "Weblancer": "https://weblancer.net"
}

# Облако ключевых слов для умного поиска
KEYWORDS = [
    "парсинг", "парсер", "parsing", "parser", 
    "сбор дан", "выгрузк", "экспорт", "scraping", "scraper", "скрап",
    "автоматизац", "сбор контакт", "выгрузить", "баз"
]

bot = Bot(token=TOKEN)
seen_tasks = set()

def match_keywords(text):
    """Умный фильтр: проверяет наличие ключевых слов в названии заказа"""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)

async def check_all_feeds(is_first_run):
    print("Scanning all freelance platforms...")
    
    for platform_name, url in FEEDS.items():
        # feedparser автоматически чистит любые спецсимволы и ошибки разметки!
        feed = feedparser.parse(url)
        
        for entry in reversed(feed.entries):
            task_id = entry.id if 'id' in entry else entry.link
            
            if task_id not in seen_tasks:
                seen_tasks.add(task_id)
                
                title = entry.title if 'title' in entry else ""
                link = entry.link if 'link' in entry else ""
                
                # Если это не самый первый запуск бота И заказ прошел наш умный фильтр keywords
                if not is_first_run and match_keywords(title):
                    message = (
                        f"🎯 **NEW FREELANCE JOB ALERT!**\n\n"
                        f"📋 **Platform:** {platform_name.upper()}\n"
                        f"📋 **Task:** {title}\n\n"
                        f"🔗 **Link:** {link}\n"
                        f"----------------------------------------\n"
                        f"💡 *Be the first to apply!*"
                    )
                    try:
                        await bot.send_message(chat_id=MY_CHAT_ID, text=message, parse_mode="Markdown")
                        print(f"[+] Notification sent for: {title}")
                    except Exception as e:
                        print(f"Failed to send message: {e}")

async def main():
    print("Smart Autonomous Multi-Feed Hunter Bot successfully started in the cloud!")
    
    # При самом первом включении просто запоминаем текущие заказы с бирж, чтобы не спамить старыми
    await check_all_feeds(is_first_run=True)
    
    while True:
        try:
            # Последующие проверки будут присылать только новые горячие заказы
            await check_all_feeds(is_first_run=False)
        except Exception as e:
            print(f"Error checking feeds: {e}")
        # Проверяем все биржи каждые 10 минут (600 секунд)
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
