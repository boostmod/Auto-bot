from telegram import Update, ChatMemberUpdated
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ChatMemberHandler

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Make sure it's an integer

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Welcome {user.first_name}!\nUse /myinfo to see your info.")

# /myinfo command
async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Your Info:\nID: {user.id}\nName: {user.full_name}\nUsername: @{user.username}"
    )

# Broadcast command for admin only
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return

    # Add your subscriber list handling here
    # For example: subscribers = [id1, id2, id3]
    subscribers = []  # Replace with actual list from DB
    for user_id in subscribers:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")

# Auto approve join requests
async def approve_join(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member.status == "member":
        try:
            await context.bot.approve_chat_join_request(update.chat_member.chat.id, update.chat_member.from_user.id)
        except Exception as e:
            print(f"Error approving join request: {e}")

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myinfo", myinfo))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatMemberHandler(approve_join, ChatMemberHandler.CHAT_MEMBER))
