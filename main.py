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

Это бот со слотами от Меллстроя.

Нажимай на кнопку и ебашь в казик
    """
    await update.message.reply_text(welcome_text)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
Хули ты хэлп нажал? Непонятно объсянил нахуй?
    """
    await update.message.reply_text(help_text)

# Ответ на текстовые сообщения


# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Логирование ошибок"""
    logger.error(f"Ошибка при обработке обновления {update}: {context.error}")

def main():
    """загрузка"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Регистрируем обработчик текстовых сообщений
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