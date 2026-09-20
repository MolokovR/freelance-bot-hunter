# 🕵️‍♂️ Smart Autonomous Freelance Hunter Bot

An asynchronous Telegram bot written in **Python 3.10+** designed to automatically aggregate, filter, and monitor projects from major freelance platforms in real-time.

## 🎯 Project Purpose
This software streamfuses real-time freelance market data to instantly capture commercial orders in targeted domains: **Data Scraping (Parsing)**, **Data Processing (Excel/CSV manipulation)**, **API Integrations**, and **CMS Tweaks (WordPress/Tilda)**. By delivering notifications within 10 minutes of a project's publication, the bot enables developers to apply ahead of competitors.

---

## ⚡ Key Features & Tech Stack

* **Core Stack:** `Python 3.10`, `aiogram v3` (Telegram Bot API Framework), `aiohttp` (Asynchronous HTTP Requests), `feedparser` (Robust XML/RSS parsing), `asyncio`.
* **Surgical Filtering (Regex Core):** Employs precise regular expressions (`re.search` bound with word boundaries `\b`) to scan project descriptions. This strictly prevents false positives (e.g., short technical tags like "bot" won't trigger on casual Russian root words like "работа/разработка").
* **Anti-Spam Shield (STOP_WORDS):** Features a hardcoded blacklist that instantly drops non-target entries, filtering out heavy backend engineering, mobile app development, graphic design, and video editing.
* **Smart Initialization (is_first_run mode):** On startup, the bot builds an initial tracking cache and displays up to 10 latest relevant archive orders per platform. It then locks those IDs into `seen_tasks = set()` to seamlessly switch to hot real-time catching without duplication.
* **Self-Diagnostic Heartbeat ("Pulse"):** Once per hour, the bot automatically broadcasts a short performance metrics report (Ping) to Telegram, showing the total execution cycles and the current cache size to guarantee the engine hasn't stalled.

---

## 🚀 Production Deployment
The project is container-native and successfully deployed in an isolated Docker environment on the cloud infrastructure of **Amvera.ru**. Sensitive access credentials and runtime tokens are safely decoupled from the codebase using system environment variables:
* `BOT_TOKEN` — Unique Telegram Bot API access token.
* `TELEGRAM_ID` — Target chat ID of the personal administrator channel.

---

## 📂 Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com
```
2. Populate dependencies (requires `requirements.txt` file):
```bash
pip install -r requirements.txt
```
3. Set your system environment variables and launch the core agent:
```bash
python bot.py
```
