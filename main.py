import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from parser import parse_signal

TOKEN = "8744121497:AAFd-cI-y1BxEuA5eBxmwfXDVu7YWR1Fnz0"
MY_ID = 2146963771

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для торговли по сигналам.\n\n"
        "Просто пришли мне текст сигнала, и я его обработаю."
    )

async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID:
        return
    
    text = update.message.text
    signal = parse_signal(text)
    
    if not signal:
        await update.message.reply_text("❌ Не удалось распознать сигнал.")
        return
    
    targets_str = ", ".join([str(t) for t in signal['targets']])
    response = (
        f"📊 *Сигнал распознан:*\n\n"
        f"💎 Монета: `{signal['symbol']}`\n"
        f"📈 Направление: *{signal['direction']}*\n"
        f"⚡️ Плечо: *X{signal['leverage']}*\n"
        f"🎯 Вход: `{signal['entry']}`\n"
        f"🏁 Цели: `{targets_str}`\n"
        f"🛑 Стоп: `{signal['stop']}`\n\n"
        f"Открыть сделку?"
    )
    
    keyboard = [[
        InlineKeyboardButton("✅ Да", callback_data=f"open_{signal['symbol']}"),
        InlineKeyboardButton("❌ Нет", callback_data="skip")
    ]]
    await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "skip":
        await query.edit_message_text("❌ Пропущено.")
    elif query.data.startswith("open_"):
        symbol = query.data.replace("open_", "")
        await query.edit_message_text(f"✅ Сделка по {symbol} открыта! (симуляция)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_signal))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен...")
    app.run_polling()
