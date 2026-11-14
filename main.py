import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك مورس 🎵\nدزلي اسم اغنية وانا اجيبها الك")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"جاري البحث عن : {text} ... 🎧")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': 'song.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{text}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get('title', text)
            file = "song.mp3"
            await update.message.reply_audio(audio=open(file, 'rb'), title=title, caption=f"🎵 {title}")
            os.remove(file)
    except Exception as e:
        await update.message.reply_text("ما لكيت الاغنية، جرب اسم ثاني 😔")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()

if __name__ == "__main__":
    main()
