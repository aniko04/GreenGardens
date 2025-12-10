from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin
from .models import FAQ
from home.models import *

# Register your models here.
# Tarjima qilinadigan modellar uchun TabbedTranslationAdmin ishlatiladi
# Bu admin panelda har bir til uchun alohida tab ko'rsatadi (UZ | RU | EN)

@admin.register(MainInfo)
class MainInfoAdmin(TabbedTranslationAdmin):
    list_display = ('site_name', 'contact_email', 'phone_number', 'address', 'opening_hours', 'footer_text')

@admin.register(SocialLink)
class SocialLinkAdmin(TabbedTranslationAdmin):
    list_display = ('platform', 'icon', 'url', 'total_followers', 'is_active')

@admin.register(Mainslider)
class MainsliderAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'subtitle', 'description', 'is_active')

@admin.register(IntroOurCompany)
class IntroOurCompanyAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'subtitle', 'experience_years', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(MainFeature)
class MainFeatureAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'icon', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurService)
class OurServiceAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'slug', 'is_active', 'is_top')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug')
    list_editable = ('is_active', 'is_top')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-id',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(OurWorkProcess)
class OurWorkProcessAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'step_number', 'pagename', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description', 'pagename')
    list_editable = ('is_active',)
    ordering = ('step_number',)

@admin.register(OurTestimonial)
class OurTestimonialAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'position', 'rate', 'is_active')
    list_filter = ('is_active', 'rate')
    search_fields = ('name', 'position', 'title')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurProject)
class OurProjectAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'category', 'project_date', 'is_active','is_top')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'category', 'project_name')
    list_editable = ('is_active', 'is_top')
    date_hierarchy = 'project_date'
    ordering = ('-project_date',)

@admin.register(OurFact)
class OurFactAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'project_number', 'customer_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurBenefit)
class OurBenefitAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'client_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'benefit1', 'benefit2')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurBlog)
class OurBlogAdmin(TabbedTranslationAdmin):
    list_display = ('minititle', 'author', 'category', 'publish_date', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'author', 'category')
    list_editable = ('is_active',)
    date_hierarchy = 'publish_date'

@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(OurExpert)
class OurExpertAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'position', 'image_preview', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position')
    list_editable = ('is_active',)
    ordering = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="border-radius:50%; object-fit:cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Photo"

@admin.register(TeamApplication)
class TeamApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-submitted_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'sent_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_filter = ('sent_at',)
    ordering = ('-sent_at',)
    readonly_fields = ('name', 'email', 'phone', 'message', 'sent_at')

@admin.register(FAQ)
class FAQAdmin(TabbedTranslationAdmin):
    list_display = ('question', 'is_active')  # Jadvalda ko'rinadigan ustunlar
    list_filter = ('is_active',)              # Yon tomonda filter chiqadi
    search_fields = ('question', 'answer')    # Qidiruv funksiyasi
    list_editable = ('is_active',)


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ('name','id', 'price', 'quantity', 'status', 'is_active', 'is_top')
    list_filter = ('status', 'is_active', 'is_top')
    search_fields = ('name', 'mini_description', 'description')
    list_editable = ('is_active', 'is_top', 'status')
    ordering = ('-id',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

# Like va Cart modellari yuqorida import qilingan (home.models import *)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-id',)
    list_per_page = 25


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'created_at', 'total_price', 'discount_amount', 'discount_percent')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)
    list_per_page = 25

    # Custom read-only fields (computed values)
    def total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    total_price.short_description = "Jami narx"

    def discount_amount(self, obj):
        discount = obj.get_discount_amount()
        return f"-${discount:.2f}" if discount > 0 else "$0.00"
    discount_amount.short_description = "Chegirma miqdori"

    def discount_percent(self, obj):
        percent = obj.get_discount_percent()
        return f"{percent:.1f}%" if percent > 0 else "—"
    discount_percent.short_description = "Chegirma foizi"


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'user', 'is_online', 'created_at', 'message_count')
    list_filter = ('is_online', 'created_at')
    search_fields = ('name', 'phone', 'email', 'session_token', 'user__username')
    ordering = ('-updated_at',)
    readonly_fields = ('session_token', 'created_at', 'updated_at')
    list_per_page = 25

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Xabarlar soni"


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'message', 'created_at', 'is_read')
    can_delete = False


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'message_preview', 'is_read', 'created_at')
    list_filter = ('sender', 'is_read', 'created_at')
    search_fields = ('message', 'session__name', 'session__phone', 'session__email')
    ordering = ('-created_at',)
    readonly_fields = ('session', 'sender', 'message', 'created_at')
    list_per_page = 50

    def message_preview(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
    message_preview.short_description = "Xabar"
