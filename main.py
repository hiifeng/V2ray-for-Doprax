from telegram.ext import Application, ConversationHandler, CommandHandler,CallbackQueryHandler,MessageHandler, filters
from bot_handlers import start, handle_receipt_decision, handle_receipt, button_handler, handle_payment, handle_add_config, handle_add_config_details
from database import init_db
from config import BOT_TOKEN, CHOOSING, PAYMENT, ADDING_CONFIG, ADDING_CONFIG_DETAILS

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CallbackQueryHandler(button_handler)],
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment)],
            ADDING_CONFIG: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_config)],
            ADDING_CONFIG_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_config_details)]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_receipt_decision, pattern='^(approve:|reject:)'))
    application.add_handler(MessageHandler(filters.PHOTO, handle_receipt))

    init_db()
    application.run_polling()

if __name__ == '__main__':
    main()
