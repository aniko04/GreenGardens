"""
Telegram Bot Utility Functions
"""
from django.conf import settings
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import logging

logger = logging.getLogger(__name__)


async def send_message_to_admin_async(message_text):
    """Async ravishda admin'ga xabar yuborish"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
    
    if not bot_token or not admin_chat_id:
        logger.warning("Telegram bot sozlamalari topilmadi")
        return None
    
    try:
        bot = Bot(token=bot_token)
        sent_message = await bot.send_message(
            chat_id=admin_chat_id,
            text=message_text,
            parse_mode='Markdown'
        )
        logger.info(f"Admin'ga xabar yuborildi, message_id: {sent_message.message_id}")
        return sent_message.message_id
    except TelegramError as e:
        logger.error(f"Telegram xatolik: {e}")
        return None
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        return None


def send_message_to_admin(message_text):
    """Sync wrapper - admin'ga xabar yuborish"""
    try:
        # Yangi event loop yaratish (agar yo'q bo'lsa)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Async funksiyani ishga tushirish
        if loop.is_running():
            # Agar loop ishlab tursa, None qaytaramiz (background task ishlatiladi)
            asyncio.ensure_future(send_message_to_admin_async(message_text))
            return None
        else:
            # Aks holda to'g'ridan-to'g'ri ishga tushiramiz
            message_id = loop.run_until_complete(send_message_to_admin_async(message_text))
            return message_id
    except Exception as e:
        logger.error(f"send_message_to_admin xatolik: {e}")
        return None


def format_chat_message_for_admin(session, message_text):
    """Chat xabarini admin uchun formatlash"""
    user_info = session.name or session.email or "Mehmon"
    
    formatted_message = (
        f"💬 *Yangi Chat Xabari*\n\n"
        f"👤 *Foydalanuvchi:* {user_info}\n"
    )
    
    if session.email:
        formatted_message += f"📧 *Email:* {session.email}\n"
    
    if session.user:
        formatted_message += f"🆔 *User ID:* {session.user.id}\n"
    
    formatted_message += (
        f"🔗 *Session:* `{session.session_token[:8]}...`\n\n"
        f"📝 *Xabar:*\n{message_text}\n\n"
        f"_Reply qilib javob bering_"
    )
    
    return formatted_message
