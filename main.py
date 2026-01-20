import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я твой Telegram-бот на Python! 🚀

Доступные команды:
/start - начальное приветствие
/help - помощь по командам

Напиши мне что-нибудь, и я отвечу! 😊
    """
    await update.message.reply_text(welcome_text)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📚 Доступные команды:

/start - Начать работу с ботом
/help - Показать это сообщение

🤖 Просто напиши мне любое сообщение, и я отвечу!
    """
    await update.message.reply_text(help_text)

# ✅ Функция echo (исправляет ошибку)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-ответ на текстовые сообщения"""
    user_text = update.message.text
    
    # Простой эхо-ответ
    response = f"Вы написали: '{user_text}'"
    
    # Или более полезный ответ
    if 'привет' in user_text.lower():
        response = f"И тебе привет, {update.effective_user.first_name}! 👋"
    elif 'как дела' in user_text.lower():
        response = f"У бота всё отлично! А у вас, {update.effective_user.first_name}?"
    elif 'спасибо' in user_text.lower():
        response = f"Пожалуйста! Рад помочь! 😊"
    elif 'бот' in user_text.lower():
        response = f"Да, я здесь! Чем могу помочь? 🤖"
    else:
        response = f"Вы написали: '{user_text}'\nПопробуйте команду /help для списка команд"
    
    await update.message.reply_text(response)

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Логирование ошибок"""
    logger.error(f"Ошибка при обработке обновления {update}: {context.error}")

def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # ✅ Теперь echo определена и работает
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo
    ))
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    port = int(os.environ.get('PORT', 8443))
    
    # Для Railway используем webhook или polling
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # На Railway используем webhook
        webhook_url = os.environ.get('RAILWAY_STATIC_URL')
        if webhook_url:
            application.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=TOKEN,
                webhook_url=f"{webhook_url}/{TOKEN}"
            )
        else:
            # Если нет URL, используем polling
            application.run_polling()
    else:
        # В локальном окружении используем polling
        print("🚀 Бот запущен в режиме polling...")
        application.run_polling()

if __name__ == '__main__':
    main()