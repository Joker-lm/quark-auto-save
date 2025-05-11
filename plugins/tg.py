# plugins/tg.py

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from quark.quark import QuarkCloud

# 配置 Telegram Bot Token 和目标文件夹 ID
TG_BOT_TOKEN = "你的_TG_BOT_TOKEN"
DEST_FOLDER_ID = "你的_目标文件夹_ID"

# 实例化 QuarkCloud
quark = QuarkCloud()
quark.login_from_config()  # 使用配置文件中的 cookie 登录

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pan.quark.cn/s/" in text:
        await update.message.reply_text("⏳ 正在处理链接，请稍候...")
        try:
            result = quark.save_link(text, parent_folder_id=DEST_FOLDER_ID)
            msg = result.get("msg", "转存成功")
            await update.message.reply_text(f"✅ {msg}")
        except Exception as e:
            await update.message.reply_text(f"❌ 转存失败：{str(e)}")
    else:
        await update.message.reply_text("请发送有效的夸克分享链接。")

def run():
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
