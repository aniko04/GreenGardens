"""
Telegram Bot Management Command - FAQAT ADMIN UCHUN
Usage: python manage.py run_telegram_bot
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from home.models import ChatMessage, ChatSession
from asgiref.sync import sync_to_async
import logging

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish (faqat admin uchun)'

    def is_admin(self, user_id):
        """Foydalanuvchi admin ekanligini tekshirish"""
        admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
        return str(user_id) == str(admin_chat_id)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start komandasi - /start"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔️ Kechirasiz, bu bot faqat admin uchun.\n\n"
                "Savol yoki muammo bo'lsa, sayt orqali chat qoldirishingiz mumkin."
            )
            logger.warning(f"Non-admin user {user.id} ({user.first_name}) /start bosdi")
            return
        
        await update.message.reply_text(
            f"👋 Salom Admin!\n\n"
            f"✅ Bot ishlayabman!\n\n"
            f"📬 Chat widget orqali kelgan xabarlarga *reply* qilib javob bering.\n"
            f"Javobingiz avtomatik chat widget'ga yetkaziladi! 🌱",
            parse_mode='Markdown'
        )
        logger.info(f"Admin {user.id} ({user.first_name}) /start bosdi")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help komandasi - /help"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
            return
        
        await update.message.reply_text(
            "🤖 *Admin Support Bot*\n\n"
            "*Qanday ishlaydi:*\n"
            "1️⃣ Chat widget'dan xabar keladi\n"
            "2️⃣ Sizga xabar yuboriladi\n"
            "3️⃣ Reply qilib javob bering\n"
            "4️⃣ Javob chat widget'ga yetadi\n\n"
            "*Komandalar:*\n"
            "/start - Botni ishga tushirish\n"
            "/help - Yordam\n"
            "/stats - Statistika",
            parse_mode='Markdown'
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Statistika komandasi"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
            return
        
        try:
            # Sync to async conversion
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
                f"👨‍💼 Admin: {admin_messages}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Stats xatolik: {e}")
            await update.message.reply_text("Xatolik yuz berdi")

    async def handle_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reply xabarlarni qayta ishlash - admin javobi"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("⛔️ Bu bot faqat admin uchun.")
            return
        
        # Reply bo'lgan xabarni tekshirish
        if not update.message.reply_to_message:
            await update.message.reply_text(
                "ℹ️ Chat xabariga javob berish uchun *reply* qiling.",
                parse_mode='Markdown'
            )
            return
        
        try:
            # Reply qilingan xabarni topish (sync_to_async bilan)
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
            
            # Admin javobini saqlash (sync_to_async bilan)
            admin_reply_text = update.message.text
            
            @sync_to_async
            def create_admin_message():
                return ChatMessage.objects.create(
                    session=original_message.session,
                    sender='admin',
                    message=admin_reply_text
                )
            
            admin_message = await create_admin_message()
            
            # User info olish
            @sync_to_async
            def get_user_info():
                return original_message.session.name or original_message.session.phone or original_message.session.email or "Mehmon"
            
            user_info = await get_user_info()
            
            await update.message.reply_text(
                f"✅ Javob yuborildi!\n"
                f"Foydalanuvchi: {user_info}"
            )
            
            logger.info(
                f"Admin {user.id} replied to session {original_message.session.id}: {admin_reply_text[:50]}"
            )
            
        except Exception as e:
            logger.error(f"Reply handler xatolik: {e}")
            await update.message.reply_text("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Oddiy xabarlarni qabul qilish (admin uchun)"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔️ Kechirasiz, bu bot faqat admin uchun.\n\n"
                "Savol bo'lsa, sayt orqali chat qoldirishingiz mumkin."
            )
            logger.warning(f"Non-admin user {user.id} xabar yubordi")
            return
        
        # Reply bo'lmagan oddiy xabar
        await update.message.reply_text(
            "ℹ️ Chat xabariga javob berish uchun kelgan xabarga *reply* qiling.\n\n"
            "Yordam: /help",
            parse_mode='Markdown'
        )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xatolarni qayta ishlash"""
        logger.error(f"Update {update} xatolikka sabab bo'ldi: {context.error}")

    def handle(self, *args, **options):
        """Management command handle"""
        bot_token = settings.TELEGRAM_BOT_TOKEN
        admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
        
        if not bot_token:
            self.stdout.write(self.style.ERROR(
                '❌ TELEGRAM_BOT_TOKEN topilmadi!\n'
                '.env faylida TELEGRAM_BOT_TOKEN ni sozlang.'
            ))
            return
        
        if not admin_chat_id:
            self.stdout.write(self.style.ERROR(
                '❌ TELEGRAM_ADMIN_CHAT_ID topilmadi!\n'
                '.env faylida TELEGRAM_ADMIN_CHAT_ID ni sozlang.'
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            '🤖 Telegram bot ishga tushmoqda...\n'
            f'Admin Chat ID: {admin_chat_id}'
        ))

        # Application yaratish
        application = Application.builder().token(bot_token).build()

        # Handlerlarni qo'shish
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Reply xabarlar uchun handler (birinchi bo'lishi kerak)
        application.add_handler(MessageHandler(
            filters.TEXT & filters.REPLY & ~filters.COMMAND,
            self.handle_reply
        ))
        
        # Oddiy xabarlar uchun handler
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & ~filters.REPLY,
            self.handle_message
        ))
        
        # Xatolik handlerini qo'shish
        application.add_error_handler(self.error_handler)

        # Botni ishga tushirish
        self.stdout.write(self.style.SUCCESS('✅ Bot ishga tushdi! Ctrl+C bilan to\'xtatish mumkin.'))
        application.run_polling(allowed_updates=Update.ALL_TYPES)
