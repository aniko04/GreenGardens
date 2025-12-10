from django.apps import AppConfig
import os
import threading
import logging

logger = logging.getLogger(__name__)

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    
    def ready(self):
        """Django to'liq yuklanganidan keyin ishga tushadi"""
        # Faqat runserver da va birinchi marta yuklanayotganda ishga tushirish
        if os.environ.get('RUN_MAIN', None) == 'true':
            self.start_telegram_bot()
    
    def start_telegram_bot(self):
        """Telegram botni background thread da ishga tushirish"""
        try:
            from django.conf import settings
            
            # Bot settings mavjudligini tekshirish
            if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
                logger.warning("TELEGRAM_BOT_TOKEN topilmadi - bot ishga tushmaydi")
                return
            
            if not hasattr(settings, 'TELEGRAM_ADMIN_CHAT_ID') or not settings.TELEGRAM_ADMIN_CHAT_ID:
                logger.warning("TELEGRAM_ADMIN_CHAT_ID topilmadi - bot ishga tushmaydi")
                return
            
            # Telegram botni alohida thread da ishga tushirish
            bot_thread = threading.Thread(target=self._run_telegram_bot, daemon=True)
            bot_thread.start()
            logger.info("🤖 Telegram bot background thread da ishga tushdi!")
            
        except Exception as e:
            logger.error(f"Telegram bot ishga tushishda xatolik: {e}")
    
    def _run_telegram_bot(self):
        """Telegram bot kodini ishga tushirish"""
        try:
            import asyncio
            from django.conf import settings
            from telegram import Update
            from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
            from home.models import ChatMessage, ChatSession
            from asgiref.sync import sync_to_async

            # Bot logic (run_telegram_bot.py dan ko'chirilgan)
            class TelegramBotRunner:
                def __init__(self):
                    self.bot_token = settings.TELEGRAM_BOT_TOKEN
                    self.admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID

                def is_admin(self, user_id):
                    return str(user_id) == str(self.admin_chat_id)

                async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user = update.effective_user
                    
                    if not self.is_admin(user.id):
                        await update.message.reply_text(
                            "⛔️ Kechirasiz, bu bot faqat admin uchun.\n\n"
                            "Savol yoki muammo bo'lsa, sayt orqali chat qoldirishingiz mumkin."
                        )
                        return
                    
                    await update.message.reply_text(
                        f"👋 Salom Admin!\n\n"
                        f"✅ Bot Django bilan birga ishlayabman!\n\n"
                        f"📬 Chat widget orqali kelgan xabarlarga *reply* qilib javob bering.\n"
                        f"Javobingiz avtomatik chat widget'ga yetkaziladi! 🌱",
                        parse_mode='Markdown'
                    )

                async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user = update.effective_user
                    
                    if not self.is_admin(user.id):
                        await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
                        return
                    
                    await update.message.reply_text(
                        "🤖 *Admin Support Bot (Django Auto-Start)*\n\n"
                        "*Qanday ishlaydi:*\n"
                        "1️⃣ Chat widget'dan xabar keladi\n"
                        "2️⃣ Sizga xabar yuboriladi\n"
                        "3️⃣ Reply qilib javob bering\n"
                        "4️⃣ Javob chat widget'ga yetadi\n\n"
                        "*Komandalar:*\n"
                        "/start - Botni tekshirish\n"
                        "/help - Yordam\n"
                        "/stats - Statistika\n\n"
                        "ℹ️ Bot Django runserver bilan avtomatik ishga tushadi!",
                        parse_mode='Markdown'
                    )

                async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user = update.effective_user
                    
                    if not self.is_admin(user.id):
                        await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
                        return
                    
                    try:
                        total_sessions = await sync_to_async(ChatSession.objects.count)()
                        total_messages = await sync_to_async(ChatMessage.objects.count)()
                        user_messages = await sync_to_async(
                            lambda: ChatMessage.objects.filter(sender='user').count()
                        )()
                        admin_messages = await sync_to_async(
                            lambda: ChatMessage.objects.filter(sender='admin').count()
                        )()
                        
                        await update.message.reply_text(
                            f"📊 *Chat Statistikasi*\n\n"
                            f"💬 Jami sessiyalar: {total_sessions}\n"
                            f"📨 Jami xabarlar: {total_messages}\n"
                            f"👤 Foydalanuvchi: {user_messages}\n"
                            f"👨‍💼 Admin: {admin_messages}\n\n"
                            f"🚀 Status: Django bilan birgalikda ishlamoqda",
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        logger.error(f"Stats xatolik: {e}")
                        await update.message.reply_text("Xatolik yuz berdi")

                async def handle_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user = update.effective_user
                    
                    if not self.is_admin(user.id):
                        await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
                        return
                    
                    if not update.message.reply_to_message:
                        await update.message.reply_text(
                            "ℹ️ Chat xabariga javob berish uchun *reply* qiling.",
                            parse_mode='Markdown'
                        )
                        return
                    
                    try:
                        replied_message_id = update.message.reply_to_message.message_id
                        
                        @sync_to_async
                        def get_original_message():
                            return ChatMessage.objects.filter(
                                telegram_message_id=replied_message_id
                            ).first()
                        
                        original_message = await get_original_message()
                        
                        if not original_message:
                            await update.message.reply_text(
                                "❌ Bu xabar chat widget'dan kelmagan.\n"
                                "Faqat chat xabarlariga reply qilishingiz mumkin."
                            )
                            return
                        
                        admin_reply_text = update.message.text
                        
                        @sync_to_async
                        def create_admin_message():
                            return ChatMessage.objects.create(
                                session=original_message.session,
                                sender='admin',
                                message=admin_reply_text
                            )
                        
                        admin_message = await create_admin_message()
                        
                        @sync_to_async
                        def get_user_info():
                            return original_message.session.name or original_message.session.phone or original_message.session.email or "Mehmon"
                        
                        user_info = await get_user_info()
                        
                        await update.message.reply_text(
                            f"✅ Javob yuborildi!\n"
                            f"Foydalanuvchi: {user_info}"
                        )
                        
                    except Exception as e:
                        logger.error(f"Reply handler xatolik: {e}")
                        await update.message.reply_text("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")

                async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    user = update.effective_user
                    
                    if not self.is_admin(user.id):
                        await update.message.reply_text(
                            "⛔️ Kechirasiz, bu bot faqat admin uchun.\n\n"
                            "Savol bo'lsa, sayt orqali chat qoldirishingiz mumkin."
                        )
                        return
                    
                    await update.message.reply_text(
                        "ℹ️ Chat xabariga javob berish uchun kelgan xabarga *reply* qiling.\n\n"
                        "Yordam: /help",
                        parse_mode='Markdown'
                    )

                async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
                    logger.error(f"Telegram bot xatolik: {context.error}")

                async def run_bot(self):
                    """Botni async rejimda ishga tushirish"""
                    application = Application.builder().token(self.bot_token).build()

                    # Handlerlarni qo'shish
                    application.add_handler(CommandHandler("start", self.start_command))
                    application.add_handler(CommandHandler("help", self.help_command))
                    application.add_handler(CommandHandler("stats", self.stats_command))

                    application.add_handler(MessageHandler(
                        filters.TEXT & filters.REPLY & ~filters.COMMAND,
                        self.handle_reply
                    ))

                    application.add_handler(MessageHandler(
                        filters.TEXT & ~filters.COMMAND & ~filters.REPLY,
                        self.handle_message
                    ))

                    application.add_error_handler(self.error_handler)

                    # Botni polling rejimida ishga tushirish (signal handler'siz)
                    logger.info("🤖 Telegram bot polling rejimida ishga tushmoqda...")
                    async with application:
                        await application.initialize()
                        await application.start()
                        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
                        # Bot to'xtatilmaguncha ishlaydi
                        while True:
                            await asyncio.sleep(1)

            # Bot instanceni yaratish va ishga tushirish
            bot_runner = TelegramBotRunner()
            # Yangi event loop yaratib, async botni ishga tushirish
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot_runner.run_bot())
            
        except Exception as e:
            logger.error(f"Telegram bot ishga tushishda xatolik: {e}")
            import traceback
            logger.error(traceback.format_exc())
