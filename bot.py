from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


import base64

with open("token.enc", "rb") as f:
    encoded = f.read()

TOKEN = base64.b64decode(encoded).decode()

print("Bot token loaded ✔")







def clean_text(text):
    return text.replace("\n", " ").strip()

def split_sentences(text):
    return text.split(".")

def summarize(text):
    sentences =split_sentences(clean_text(text))
    return "\n".join(sentences[:3])  # أول 3 جمل

def generate_questions(text):
    sentences = split_sentences(clean_text(text))
    questions = []

    for s in sentences:
        s = s.strip()
        if len(s) > 20:
            questions.append("❓ ماذا تعني: " + s)

    return "\n".join(questions[:5])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 أهلاً بك في المساعد الأكاديمي\n"
        "📄 أرسل نص أو PDF وسأقوم بتحليله تلقائياً"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    summary = summarize(text)
    questions = generate_questions(text)

    reply = f"📌 التلخيص:\n{summary}\n\n❓ الأسئلة:\n{questions}"

    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()