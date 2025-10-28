from django.contrib import admin
from django.utils.html import format_html
from .models import FAQ
from home.models import *

# Register your models here.
@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'phone_number', 'address', 'opening_hours', 'footer_text')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'icon', 'url', 'total_followers', 'is_active')

@admin.register(Mainslider)
class MainsliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'description', 'is_active')
    from django.contrib import admin

@admin.register(IntroOurCompany)
class IntroOurCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'experience_years', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(MainFeature)
class MainFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurService)
class OurServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'pagename', 'url', 'is_active', 'is_top')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description', 'pagename')
    list_editable = ('is_active', 'is_top')
    ordering = ('-id',)

@admin.register(OurWorkProcess)
class OurWorkProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'step_number', 'pagename', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description', 'pagename')
    list_editable = ('is_active',)
    ordering = ('step_number',)

@admin.register(OurTestimonial)
class OurTestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'rate', 'is_active')
    list_filter = ('is_active', 'rate')
    search_fields = ('name', 'position', 'title')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurProject)
class OurProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_date', 'is_active','is_top')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'category', 'project_name')
    list_editable = ('is_active', 'is_top')
    date_hierarchy = 'project_date'
    ordering = ('-project_date',)

@admin.register(OurFact)
class OurFactAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_number', 'customer_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurBenefit)
class OurBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'benefit1', 'benefit2')
    list_editable = ('is_active',)
    ordering = ('-id',)

@admin.register(OurBlog)
class OurBlogAdmin(admin.ModelAdmin):
    list_display = ('minititle', 'author', 'category', 'publish_date', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'author', 'category')
    list_editable = ('is_active',)
    date_hierarchy = 'publish_date'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(OurExpert)
class OurExpertAdmin(admin.ModelAdmin):
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
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active')  # Jadvalda ko‘rinadigan ustunlar
    list_filter = ('is_active',)              # Yon tomonda filter chiqadi
    search_fields = ('question', 'answer')    # Qidiruv funksiyasi
    list_editable = ('is_active',)   


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'price', 'quantity', 'status', 'is_active', 'is_top')
    list_filter = ('status', 'is_active', 'is_top')
    search_fields = ('name', 'mini_description', 'description')
    list_editable = ('is_active', 'is_top', 'status')
    ordering = ('-id',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

from django.contrib import admin
from .models import Like, Cart

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
