import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8968706484:AAGaAg1F95754GdQLWn4ojAq3WTLw2W1nC4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Написать пост", callback_data="post")],
        [InlineKeyboardButton("Рекламный текст", callback_data="ad")],
        [InlineKeyboardButton("Идея для контента", callback_data="idea")],
        [InlineKeyboardButton("Описание товара", callback_data="product")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я бот для создания текстов.\nВыбери, что тебе нужно:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    texts = {
        "post": "Напиши тему поста, и я сделаю текст.",
        "ad": "Напиши, что рекламируем, и я сделаю рекламный текст.",
        "idea": "Напиши нишу или тему, и я дам идеи для контента.",
        "product": "Напиши название товара и его особенности."
    }
    
    context.user_data["mode"] = query.data
    await query.edit_message_text(texts.get(query.data, "Напиши свой запрос:"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    text = update.message.text
    
    if not mode:
        await update.message.reply_text("Сначала нажми /start и выбери тип текста.")
        return
    
    if mode == "post":
        result = f"🔥 Пост на тему «{text}»:\n\n{text} — это важно!\n\nПочему? Потому что...\n\nСогласны? Пишите в комментариях 👇"
    elif mode == "ad":
        result = f"🚀 Реклама:\n\nИщете {text}?\nТогда вам точно сюда!\n\nПреимущества:\n✅ Качество\n✅ Скорость\n✅ Результат\n\nПишите прямо сейчас!"
    elif mode == "idea":
        result = f"Идеи для контента по теме «{text}»:\n\n1. Как я начал...\n2. 5 ошибок новичков\n3. Мой результат за месяц\n4. Советы эксперта\n5. Вопрос к аудитории"
    else:
        result = f"Описание товара «{text}»:\n\n{text} — отличный выбор!\n\nОсобенности:\n• Высокое качество\n• Удобство\n• Выгодная цена"
    
    await update.message.reply_text(result)
    await update.message.reply_text("Хочешь ещё? Нажми /start")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
