Ось код з артефакту "Telegram Bot для ETH"! 👇
Код знаходиться в артефакті з назвою "Telegram Bot для ETH Мега-комбінацій" (ID: telegram_bot_integration).
Ось повний код, який потрібно скопіювати:
python"""
Telegram Bot для ETH Мега-комбінацій
Отримуйте миттєві сповіщення про всі 5 мега-комбінацій прямо в Telegram!

Функціонал:
- Миттєві алерти з TradingView
- Команди для перегляду статистики
- Історія сигналів
- Графіки та аналітика
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from datetime import datetime
import json
from collections import defaultdict

# ============================================================================
# НАЛАШТУВАННЯ
# ============================================================================

# Отримайте токен від @BotFather в Telegram
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ⬅️ ЗАМІНІТЬ НА ВАШ ТОКЕН!

# База даних сигналів (в реальному додатку використовуйте БД)
signals_db = []
user_stats = defaultdict(lambda: {
    'total_signals': 0,
    'by_combo': defaultdict(int),
    'subscribed': True
})

# ============================================================================
# ОСНОВНІ КОМАНДИ
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - привітання"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    welcome_message = f"""
🔥 **Вітаємо, {user_name}!**

Це бот для відстеження 5 найпотужніших торгових комбінацій ETH/USDT!

**📊 Доступні комбінації:**
⚡ Ідеальний шторм (75-85%)
🎯 Снайперський пробій (72-80%)
📉 Розворот магната (70-78%)
🌊 Золота хвиля (68-76%)
💥 Капітуляція+ (70-77%)

**🤖 Команди:**
/help - Допомога
/stats - Статистика сигналів
/history - Історія за 7 днів
/settings - Налаштування
/subscribe - Підписатись на алерти
/unsubscribe - Відписатись

Готові отримувати сигнали? 🚀
Використовуйте /subscribe
"""
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data='stats'),
         InlineKeyboardButton("⚙️ Налаштування", callback_data='settings')],
        [InlineKeyboardButton("🔔 Підписатись", callback_data='subscribe'),
         InlineKeyboardButton("📖 Допомога", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help - довідка"""
    help_text = """
📖 **ДОВІДКА**

**Основні команди:**

/start - Почати роботу з ботом
/stats - Переглянути статистику сигналів
/history - Історія сигналів за останні 7 днів
/settings - Налаштування сповіщень
/subscribe - Увімкнути сповіщення
/unsubscribe - Вимкнути сповіщення

**Частота сигналів:**
2-3 на місяць (24-40 на рік)

**Очікуваний ROI:**
60-70% на рік без леверіджу
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats - статистика"""
    user_id = update.effective_user.id
    stats = user_stats[user_id]
    
    total_signals = len(signals_db)
    
    combo_counts = defaultdict(int)
    for signal in signals_db:
        combo_counts[signal.get('combo', 'Unknown')] += 1
    
    stats_text = f"""
📊 **СТАТИСТИКА СИГНАЛІВ**

**Загальна:**
Всього сигналів: {total_signals}
Ваші сигнали: {stats['total_signals']}

**По комбінаціях:**
⚡ Ідеальний шторм: {combo_counts.get('ІДЕАЛЬНИЙ ШТОРМ', 0)}
🎯 Снайперський пробій: {combo_counts.get('СНАЙПЕРСЬКИЙ ПРОБІЙ', 0)}
📉 Розворот магната: {combo_counts.get('РОЗВОРОТ МАГНАТА', 0)}
🌊 Золота хвиля: {combo_counts.get('ЗОЛОТА ХВИЛЯ', 0)}
💥 Капітуляція+: {combo_counts.get('КАПІТУЛЯЦІЯ+', 0)}

**Статус підписки:**
{'✅ Активна' if stats['subscribed'] else '❌ Неактивна'}
"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /history - історія сигналів"""
    
    if not signals_db:
        await update.message.reply_text("📭 Історія порожня. Очікуємо перших сигналів!")
        return
    
    recent_signals = signals_db[-10:]
    
    history_text = "📈 **ІСТОРІЯ СИГНАЛІВ** (останні 10)\n\n"
    
    for i, signal in enumerate(reversed(recent_signals), 1):
        emoji = {
            'ІДЕАЛЬНИЙ ШТОРМ': '⚡',
            'СНАЙПЕРСЬКИЙ ПРОБІЙ': '🎯',
            'РОЗВОРОТ МАГНАТА': '📉',
            'ЗОЛОТА ХВИЛЯ': '🌊',
            'КАПІТУЛЯЦІЯ+': '💥'
        }.get(signal.get('combo', ''), '🔔')
        
        history_text += f"""
{i}. {emoji} **{signal.get('combo', 'Unknown')}**
   💰 Ціна: ${signal.get('price', 0):.2f}
   📊 RSI: {signal.get('rsi', 0):.1f}
   ⏰ {signal.get('time', 'N/A')}
   {'─' * 30}
"""
    
    await update.message.reply_text(history_text, parse_mode='Markdown')


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /subscribe - підписатись"""
    user_id = update.effective_user.id
    user_stats[user_id]['subscribed'] = True
    
    await update.message.reply_text(
        "✅ **Підписку активовано!**\n\n"
        "Тепер ви отримуватимете сповіщення про всі мега-комбінації.\n\n"
        "Очікувана частота: 2-3 сигнали на місяць\n"
        "Для відписки: /unsubscribe",
        parse_mode='Markdown'
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /unsubscribe - відписатись"""
    user_id = update.effective_user.id
    user_stats[user_id]['subscribed'] = False
    
    await update.message.reply_text(
        "❌ **Підписку деактивовано**\n\n"
        "Ви більше не отримуватимете сповіщення.\n\n"
        "Для повторної підписки: /subscribe",
        parse_mode='Markdown'
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /settings - налаштування"""
    user_id = update.effective_user.id
    stats = user_stats[user_id]
    
    settings_text = f"""
⚙️ **НАЛАШТУВАННЯ**

**Статус підписки:**
{'✅ Увімкнено' if stats['subscribed'] else '❌ Вимкнено'}
"""
    
    keyboard = [
        [InlineKeyboardButton("🔔 Підписатись" if not stats['subscribed'] else "🔕 Відписатись", 
                            callback_data='toggle_subscription')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(settings_text, reply_markup=reply_markup, parse_mode='Markdown')


# ============================================================================
# ОБРОБКА WEBHOOK ВІД TRADINGVIEW
# ============================================================================

async def process_tradingview_alert(data: dict, application):
    """Обробка вхідного сигналу від TradingView"""
    
    signal = {
        'combo': data.get('combo', 'Unknown'),
        'ticker': data.get('ticker', 'ETH/USDT'),
        'price': float(data.get('price', 0)),
        'rsi': float(data.get('rsi', 0)),
        'time': data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }
    signals_db.append(signal)
    
    combo_emoji = {
        'ІДЕАЛЬНИЙ ШТОРМ': '⚡',
        'СНАЙПЕРСЬКИЙ ПРОБІЙ': '🎯',
        'РОЗВОРОТ МАГНАТА': '📉',
        'ЗОЛОТА ХВИЛЯ': '🌊',
        'КАПІТУЛЯЦІЯ+': '💥'
    }
    
    emoji = combo_emoji.get(signal['combo'], '🔔')
    
    alert_message = f"""
🚨 **НОВИЙ СИГНАЛ!** 🚨

{emoji} **{signal['combo']}**

💰 **Ціна:** ${signal['price']:.2f}
📊 **RSI:** {signal['rsi']:.1f}
📈 **Пара:** {signal['ticker']}
⏰ **Час:** {signal['time']}

{'─' * 30}

📌 **Рекомендації:**
"""
    
    if signal['combo'] == 'ІДЕАЛЬНИЙ ШТОРМ':
        alert_message += """
✅ Сильний бичачий сигнал
🎯 Точність: 75-85%
💼 Рекомендований вхід: 3-5% капіталу
🛡️ Стоп-лос: -2.5%
🎁 Тейк-профіт: +7-10%
"""
    elif signal['combo'] == 'СНАЙПЕРСЬКИЙ ПРОБІЙ':
        alert_message += """
✅ Імпульсний пробій
🎯 Точність: 72-80%
💼 Швидкий трейд
🛡️ Стоп-лос: -2%
🎁 Тейк-профіт: +5-7%
"""
    
    alert_message += "\n\n⚡ Діяйте швидко! Використовуйте стоп-лоси!"
    
    for user_id, stats in user_stats.items():
        if stats['subscribed']:
            try:
                await application.bot.send_message(
                    chat_id=user_id,
                    text=alert_message,
                    parse_mode='Markdown'
                )
                stats['total_signals'] += 1
                stats['by_combo'][signal['combo']] += 1
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")


# ============================================================================
# ОБРОБКА КНОПОК
# ============================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка натискань на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == 'subscribe':
        user_stats[user_id]['subscribed'] = True
        await query.edit_message_text("✅ Підписку активовано!")
    elif query.data == 'toggle_subscription':
        user_stats[user_id]['subscribed'] = not user_stats[user_id]['subscribed']
        status = "✅ Увімкнено" if user_stats[user_id]['subscribed'] else "❌ Вимкнено"
        await query.edit_message_text(f"Підписка: {status}")


# ============================================================================
# FLASK СЕРВЕР ДЛЯ WEBHOOK
# ============================================================================

from flask import Flask, request
import asyncio

flask_app = Flask(__name__)
telegram_app = None

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint для отримання алертів від TradingView"""
    try:
        data = request.json
        
        if telegram_app:
            asyncio.run(process_tradingview_alert(data, telegram_app))
        
        return {'status': 'success'}, 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return {'status': 'error', 'message': str(e)}, 500


@flask_app.route('/health', methods=['GET'])
def health():
    """Перевірка здоров'я сервера"""
    return {'status': 'ok', 'signals': len(signals_db)}, 200


# ============================================================================
# ЗАПУСК БОТА
# ============================================================================

def main():
    """Головна функція запуску"""
    global telegram_app
    
    print("🤖 Запуск Telegram бота...")
    
    telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(CommandHandler("stats", stats_command))
    telegram_app.add_handler(CommandHandler("history", history_command))
    telegram_app.add_handler(CommandHandler("subscribe", subscribe_command))
    telegram_app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    telegram_app.add_handler(CommandHandler("settings", settings_command))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Бот готовий до роботи!")
    print("📱 Знайдіть свого бота в Telegram та відправте /start")
    print("\n🌐 Запуск Flask сервера на порту 5000...")
    
    import threading
    
    bot_thread = threading.Thread(target=telegram_app.run_polling)
    bot_thread.daemon = True
    bot_thread.start()
    
    flask_app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
