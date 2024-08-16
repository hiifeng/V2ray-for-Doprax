from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, CommandHandler
from config import ADMIN_CHAT_ID, CHOOSING, PAYMENT, ADDING_CONFIG, ADDING_CONFIG_DETAILS, CONFIRMING,BUYING_CONFIG
from user_management import add_user
from order_management import get_user_orders
from config_management import get_all_configs, add_config
from transaction_management import get_all_transactions, add_transaction,update_receipt_status
from database import execute_db

# Telegram bot functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    await add_user(username, chat_id)

    keyboard = [
        [InlineKeyboardButton("Add Config", callback_data='add_config')],
        [InlineKeyboardButton("List Orders", callback_data='list_orders')],
        [InlineKeyboardButton("Charge User Balance", callback_data='charge_balance')],
        [InlineKeyboardButton("List Transactions", callback_data='list_transactions')],
        [InlineKeyboardButton("Switch to User Mode", callback_data='switch_to_user')]
    ] if update.effective_chat.id == ADMIN_CHAT_ID else [
        [InlineKeyboardButton("Buy Config", callback_data='buy_config')],
        [InlineKeyboardButton("My Orders", callback_data='my_orders')],
        [InlineKeyboardButton("Deposit", callback_data='deposit')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Please choose an option:", reply_markup=reply_markup)
    return CHOOSING

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        context.user_data['amount'] = amount  # ذخیره مبلغ در context

        admin_card_number = "6237-1111-2222-3333"
        await update.message.reply_text(
            f"Please deposit {amount:.2f} to the following bank account:\n\n"
            f"Card Number: {admin_card_number}\n"
            f"After making the payment, please send the receipt."
        )
        return CONFIRMING
    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a valid number.")
        return PAYMENT

async def save_receipt_to_db(username: str, chat_id: int, photo_file_id: str, amount: float):
    await execute_db(
        "INSERT INTO receipts (username, chat_id, photo_file_id, status, amount) VALUES (?, ?, ?, ?, ?)",
        (username, chat_id, photo_file_id, 'pending', amount)
    )
    
    result = await execute_db("SELECT last_insert_rowid()", fetchone=True)
    receipt_id = result[0] if result else None
    print(f"Saved Receipt ID: {receipt_id}")  # برای دیباگ
    return receipt_id, photo_file_id



async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        username = update.effective_user.username
        chat_id = update.effective_chat.id

        try:
            # فرض کنید که مقدار amount از یک فیلد دیگر بدست می‌آید
            amount = float(context.user_data.get("amount", 0))  # تبدیل مقدار به float
            
            # ذخیره رسید در پایگاه داده و دریافت ID آن
            receipt_id = await execute_db(
                "INSERT INTO receipts (username, chat_id, photo_file_id, status, amount) VALUES (?, ?, ?, ?, ?)",
                (username, chat_id, photo_file_id, 'pending', amount)
            )

            # دریافت ID آخرین رسید درج‌شده
            receipt_id_result = await execute_db("SELECT last_insert_rowid()", fetchone=True)
            receipt_id = receipt_id_result[0] if receipt_id_result else None

            # ارسال عکس به ادمین با اطلاعات کاربر و رسید
            if receipt_id is not None:
                await context.bot.send_photo(
                    chat_id=ADMIN_CHAT_ID, 
                    photo=photo_file_id, 
                    caption=f"User: {username}\nAmount: {amount}\nChat ID: {chat_id}\n\nApprove or reject this receipt.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Approve", callback_data=f'approve:{receipt_id}')],
                        [InlineKeyboardButton("Reject", callback_data=f'reject:{receipt_id}')]
                    ])
                )

                await update.message.reply_text("Please wait for admin approval.")
            else:
                await update.message.reply_text("Failed to save the receipt. Please try again.")
        except ValueError as e:
            await update.message.reply_text("Invalid amount. Please enter a valid number.")
    else:
        await update.message.reply_text("Please send a photo of the receipt.")
    return ConversationHandler.END

async def handle_receipt_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    decision, receipt_id = query.data.split(":")
    receipt_id = int(receipt_id)

    print(f"id isssss ::::========>>>>>>>>>>>>>>>>>>  {receipt_id}")

    # استخراج اطلاعات از کپشن
    caption = query.message.caption
    lines = caption.split('\n')
    username = lines[0].split(': ')[1]
    amount = float(lines[1].split(': ')[1])  # تبدیل amount به مقدار عددی
    chat_id = int(lines[2].split(': ')[1])  # تبدیل chat_id به عدد صحیح


    if decision == 'approve':
        # افزایش موجودی کاربر در دیتابیس
        await execute_db("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))

        # ثبت تراکنش در دیتابیس
        await add_transaction(username, amount, "Deposit")
        await update_receipt_status("Confirm", receipt_id)

        # ارسال پیام به کاربر
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Your receipt has been approved. {amount} has been added to your account balance."
        )

        # ویرایش پیام ادمین
        await query.edit_message_caption(f"Receipt approved for {username}. Amount: {amount}")

    elif decision == 'reject':
        # ارسال پیام به کاربر
        await context.bot.send_message(
            chat_id=chat_id,
            text="Your receipt was rejected. Please try again or contact support."
        )

        # ویرایش پیام ادمین
        await query.edit_message_caption(f"Receipt rejected for {username}.")
        await update_receipt_status(receipt_id, 'Rejected')

async def handle_add_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دریافت اطلاعات پیکربندی
    context.user_data['config_name'] = update.message.text
    await update.message.reply_text("Send the config location.")
    await update.message.reply_text("Add amount")
    return ADDING_CONFIG_DETAILS

async def handle_add_config_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ذخیره جزئیات پیکربندی و اضافه کردن به پایگاه داده
    location = update.message.text
    name = context.user_data.get('config_name')
    # فرض بر این است که قیمت و لینک هم جمع‌آوری شده است
    price = 10.0  # مثال قیمت
    link = "https://example.com/config"  # مثال لینک

    await add_config(name, location, price, link)
    await update.message.reply_text(f"Config {name} added successfully.")
    return CHOOSING

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_config':
        await query.edit_message_text("Send the config name.")
        return ADDING_CONFIG
    elif query.data == 'list_orders':
        orders = await execute_db("SELECT * FROM orders")
        orders_text = "\n".join([str(order) for order in orders]) if orders else "No orders."
        await query.edit_message_text(f"Orders:\n{orders_text}")
        return CHOOSING
    elif query.data == 'charge_balance':
        await query.edit_message_text("Send the username and amount to charge, separated by a space.")
        return PAYMENT
    elif query.data == 'list_transactions':
        transactions = await get_all_transactions()
        transactions_text = "\n".join([str(tx) for tx in transactions]) if transactions else "No transactions."
        await query.edit_message_text(f"Transactions:\n{transactions_text}")
        return CHOOSING
    elif query.data == 'switch_to_user':
        await start(update, context)
        return CHOOSING
    elif query.data == 'buy_config':
        configs = await get_all_configs()
        keyboard = [[InlineKeyboardButton(config[1], callback_data=f'buy_{config[0]}')] for config in configs]
        await query.edit_message_text("Please choose a config:", reply_markup=InlineKeyboardMarkup(keyboard))
        return BUYING_CONFIG
    elif query.data == 'my_orders':
        orders = await get_user_orders(query.message.chat.username)
        orders_text = "\n".join([f"Config: {order[1]}, Date: {order[4]}" for order in orders]) if orders else "No orders."
        await query.edit_message_text(f"Your orders:\n{orders_text}")
        return CHOOSING
    elif query.data == 'deposit':
        await query.edit_message_text("Please enter the amount to deposit.")
        return PAYMENT

