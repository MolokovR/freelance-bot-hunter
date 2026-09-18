# Freelance Task Hunter Bot 🎯

An autonomous Telegram bot designed to monitor freelance platforms in real-time, filtering and delivering new web scraping, lead generation, and automation jobs directly to your chat.

## 🚀 Key Features
- **Real-time Monitoring:** Automatically scans freelance feeds using robust RSS parsing.
- **Smart Filtering:** Extracts target jobs containing custom keywords like "parsing", "scraping", and "data collection".
- **Instant Alerts:** Sends beautifully formatted clean Markdown notifications with direct application links to Telegram.
- **Production-Ready:** Configured for secure deployment using environment variables for sensitive API tokens.

## 🛠️ Tech Stack
- **Language:** Python 3
- **Telegram Framework:** Aiogram 3 (Asyncio-driven)
- **Data Fetching:** Feedparser

## ⚙️ Infrastructure & Deployment
- Implemented as a background loop with asynchronous sleep periods to avoid rate limiting.
- Ready for zero-cost deployment on cloud platforms (Render / Koyeb).

