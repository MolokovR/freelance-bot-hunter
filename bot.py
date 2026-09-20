import asyncio
import os
import sys
import re
import feedparser
import aiohttp
from aiogram import Bot

FEEDS = {
    "FL.ru": "https://fl.ru",
    "Freelancehunt": "https://freelancehunt.com"
}

TOKEN = os.getenv("BOT_TOKEN")
MY_CHAT_ID = os.getenv("TELEGRAM_ID")

if not TOKEN or not MY_CHAT_ID:
    print("Error: BOT_TOKEN or TELEGRAM_ID environment variables are not set!")
    sys.exit(1)

bot = Bot(token=TOKEN)
seen_tasks = set()

KEYWORDS = [
    "парсинг", "парсер", "parsing", "parser", "scraping", "scraper", "скрап",
    "сбор баз", "сбор контакт", "выгрузить", "выгрузка", "перенос товар", 
    "написать скрипт", "скрипт на python", "интеграция по api", "собрать базу",
    "эксель", "excel", "wordpress", "вордпресс", "wp", "одностраничник", 
    "лендинг", "лэндинг", "landing", "правка сайта", "доработка сайта", 
    "исправить ошибку", "ошибка на сайте", "починить сайт", "tilda", "тильда", "html"
]

def match_keywords(text):
    if not text:
        return False
    text_lower = text.lower()
    
    STOP_WORDS = [
        "дизайн", "монтаж", "видеоролик", "логотип", "баннер", "креатив", "видеомонтаж",
        "fullstack", "фулстек", "devops", "девопс", "ios", "android", "мобильное приложение",
        "дизайнер", "3d", "моделирование", "backend", "бэкенд"
    ]
    for stop in STOP_WORDS:
        if stop in text_lower:
            return False
            
    for keyword in KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\w*', text_lower):
            return True
                
    return False

async def check_all_feeds(is_first_run):
    print("... НАЧИНАЮ СКАНИРОВАНИЕ ВСЕХ БИРЖ ...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*"
    }
    
    async with aiohttp.ClientSession() as session:
        for platform_name, url in FEEDS.items():
            try:
                print(f"🔄 Проверяю биржу {platform_name}...")
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status != 200:
                        print(f"❌ {platform_name} вернула статус: {response.status}")
                        continue
                        
                    raw_xml = await response.text()
                    feed = feedparser.parse(raw_xml)
                    
                    platform_sent_count = 0
                    entries_to_check = feed.entries if is_first_run else reversed(feed.entries)
                    
                    for entry in entries_to_check:
                        task_id = entry.id if 'id' in entry else entry.link
                        
                        if is_first_run and platform_sent_count >= 10:
                            seen_tasks.add(task_id)
                            continue
                        
                        if task_id not in seen_tasks:
                            seen_tasks.add(task_id)
                            
                            title = entry.title if 'title' in entry else ""
                            link = entry.link if 'link' in entry else ""
                            
                            summary = entry.get('summary', '')
                            description = entry.get('description', '')
                            content_text = ""
                            if 'content' in entry and len(entry.content) > 0:
                                content_text = entry.content.get('value', '') if isinstance(entry.content, list) else entry.content.get('value', '')
                            
                            full_text_to_check = f"{title} {summary} {description} {content_text}"
                            
                            if match_keywords(full_text_to_check):
                                if is_first_run:
                                    platform_sent_count += 1
                                
                                prefix = "📚 [АРХИВНЫЙ ЗАКАЗ]" if is_first_run else "🚨 [НОВЫЙ ЗАКАЗ]"
                                message = (
                                    f"{prefix}\n\n"
                                    f"🔹 <b>Platform:</b> {platform_name.upper()}\n"
                                    f"📌 <b>Task:</b> {title}\n"
                                    f"🔗 <a href='{link}'>Be the first to apply!</a>"
                                )
                                try:
                                    await bot.send_message(chat_id=MY_CHAT_ID, text=message, parse_mode="HTML")
                                    print(f"📢 [{platform_name}] Отправлено в TG: {title}")
                                    await asyncio.sleep(1.5)
                                except Exception as tg_err:
                                    print(f"❌ Ошибка Telegram: {tg_err}")
                                        
            except Exception as e:
                print(f"❌ Сбой при обработке {platform_name}: {e}")

async def main():
    print("Smart Autonomous Hunter Bot successfully started on the production server!")
    try:
        await bot.send_message(
            chat_id=MY_CHAT_ID,
            text="🤖 <b>Бот-охотник успешно запущен на биржах!</b> Включена функция часового отчета о статусе работы.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не удалось отправить стартовый пост в TG: {e}")

    await check_all_feeds(is_first_run=True)
    print("Initial scan complete. Moving to real-time tracking mode.")
    
    pulse_counter = 0
    total_checks = 0
    
    while True:
        try:
            pulse_counter += 1
            total_checks += 1
            await check_all_feeds(is_first_run=False)
            
            if pulse_counter >= 6:
                pulse_counter = 0
                try:
                    pulse_message = (
                        f"🖥️ <b>Проверка связи (Пингование)</b>\n\n"
                        f"🟢 Я работаю в штатном режиме.\n"
                        f"🔄 За последний час совершено: <b>6 проверок</b> всех бирж.\n"
                        f"📦 Всего проверено за сессию: <b>{total_checks} раз</b>.\n"
                        f"🗂️ В кэше от спама удерживается: <b>{len(seen_tasks)} заказов</b>.\n\n"
                        f"<i>Жду новые целевые проекты...</i>"
                    )
                    await bot.send_message(chat_id=MY_CHAT_ID, text=pulse_message, parse_mode="HTML")
                except Exception as tg_err:
                    print(f"Ошибка отправки часового статуса: {tg_err}")
        except Exception as e:
            print(f"Error in loop: {e}")
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
