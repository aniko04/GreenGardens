from xmlrpc import client
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MainInfo(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="Sayt nomi")
    contact_email = models.EmailField(verbose_name="Aloqa email")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Manzil")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    footer_text = models.TextField(verbose_name="Footer matni")
    opening_hours = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ish vaqti")

    class Meta:
        verbose_name = "Asosiy Ma'lumot"
        verbose_name_plural = "Asosiy Ma'lumotlar"

    def __str__(self):
        return self.site_name

class SocialLink(models.Model):
    platform = models.CharField(max_length=100, verbose_name="Platforma")
    icon = models.CharField(max_length=100,null=True, blank=True, verbose_name="Ikonka")  
    url = models.URLField(verbose_name="Havola")
    total_followers = models.IntegerField(default=0, verbose_name="Obunachi soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Ijtimoiy Tarmoq"
        verbose_name_plural = "Ijtimoiy Tarmoqlar"

    def __str__(self):
        return self.platform
    
class Mainslider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm")
    button_1_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="1-tugma nomi")
    button_2_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="2-tugma nomi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Asosiy Slayder"
        verbose_name_plural = "Asosiy Slayderlar"

    def __str__(self):
        return self.title
    
class IntroOurCompany(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    icon1 = models.CharField(max_length=100,null=True, blank=True, verbose_name="1-ikonka")
    icon_text1 = models.CharField(max_length=200, null=True, blank=True, verbose_name="1-ikonka matni")
    icon2 = models.CharField(max_length=100,null=True, blank=True, verbose_name="2-ikonka")
    icon_text2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="2-ikonka matni")
    image1 = models.ImageField(upload_to='', null=True, blank=True, verbose_name="1-rasm") 
    image2 = models.ImageField(upload_to='', null=True, blank=True, verbose_name="2-rasm")
    experience_years = models.IntegerField(default=0, verbose_name="Tajriba yillari")
    list1= models.TextField(null=True, blank=True, verbose_name="1-ro'yxat")
    list2= models.TextField(null=True, blank=True, verbose_name="2-ro'yxat")
    list3= models.TextField(null=True, blank=True, verbose_name="3-ro'yxat")
    button_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tugma nomi")
    button_url = models.URLField(null=True, blank=True, verbose_name="Tugma havolasi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kompaniya Haqida"
        verbose_name_plural = "Kompaniya Haqida"

    def __str__(self):
        return self.title
    
class MainFeature(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=100,null=True, blank=True, verbose_name="Ikonka")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="Havola")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Asosiy Xususiyat"
        verbose_name_plural = "Asosiy Xususiyatlar"

    def __str__(self):
        return self.title

class OurService(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    is_top = models.BooleanField(default=False, verbose_name="TOP xizmatmi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    category = models.ManyToManyField('ServiceCategory', verbose_name="Kategoriyasi", blank=True)

    class Meta:
        verbose_name = "Bizning Xizmat"
        verbose_name_plural = "Bizning Xizmatlar"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_details', kwargs={'id': self.id})

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = RichTextField(null=True, blank=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Xizmat Kategoriyasi"
        verbose_name_plural = "Xizmat Kategoriyalari"
    
    def services_count(self):
        return self.ourservice_set.count()

    def __str__(self):
        return self.name

class OurWorkProcess(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    pagename = models.CharField(max_length=100, null=True, blank=True, verbose_name="Sahifa nomi")
    step_number = models.IntegerField(verbose_name="Qadam raqami")
    page_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Sahifa matni")
    icon = models.CharField(max_length=100,null=True, blank=True, verbose_name="Ikonka")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Ish Jarayoni"
        verbose_name_plural = "Ish Jarayonlari"

    def __str__(self):
        return self.title
    
class OurTestimonial(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    name = models.CharField(max_length=200, verbose_name="Ism")
    position = models.CharField(max_length=200, null=True, blank=True, verbose_name="Lavozim")
    feedback = models.TextField(null=True, blank=True, verbose_name="Fikr-mulohaza")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm") 
    rate = models.IntegerField(default=5, verbose_name="Baho")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Mijoz Sharhi"
        verbose_name_plural = "Mijoz Sharhlari"

    def __str__(self):
        return self.name

class OurProject(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    content = RichTextField(null=True, blank=True, verbose_name="Mazmun")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm") 
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name="Kategoriya")
    project_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Loyiha nomi")
    project_date = models.DateField(null=True, blank=True, verbose_name="Loyiha sanasi")
    button_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tugma nomi")
    project_link = models.URLField(null=True, blank=True, verbose_name="Loyiha havolasi")
    url = models.URLField(null=True, blank=True, verbose_name="Havola")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_top = models.BooleanField(default=False, verbose_name="TOP loyihami")

    class Meta:
        verbose_name = "Bizning Loyiha"
        verbose_name_plural = "Bizning Loyihalar"

    def __str__(self):
        return self.title
    
class OurFact(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    project_number = models.IntegerField(default=0, verbose_name="Loyihalar soni")
    project_content = models.CharField(max_length=200, null=True, blank=True, verbose_name="Loyiha mazmuni")
    customer_number = models.IntegerField(default=0,null=True, blank=True, verbose_name="Mijozlar soni")
    customer_content = models.CharField(max_length=200, null=True, blank=True, verbose_name="Mijoz mazmuni")
    button_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tugma nomi")
    button_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tugma havolasi")
    button_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tugma matni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Bizning Statistika"
        verbose_name_plural = "Bizning Statistikalar"

    def __str__(self):
        return self.title
    
class OurBenefit(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm") 
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    benefit1= models.CharField(max_length=200, null=True, blank=True, verbose_name="1-afzallik")
    benefit1_text= models.CharField(max_length=200, null=True, blank=True, verbose_name="1-afzallik matni")
    benefit1_quality1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="1-afzallik xususiyati 1")
    benefit1_quality2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="1-afzallik xususiyati 2")
    benefit1_quality3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="1-afzallik xususiyati 3")
    benefit1_quality4 = models.CharField(max_length=100, null=True, blank=True, verbose_name="1-afzallik xususiyati 4")
    benefit2= models.CharField(max_length=200, null=True, blank=True, verbose_name="2-afzallik")
    benefit2_text= models.CharField(max_length=200, null=True, blank=True, verbose_name="2-afzallik matni")
    client_count = models.IntegerField(default=0, verbose_name="Mijozlar soni")
    client_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Mijoz matni")

    class Meta:
        verbose_name = "Bizning Afzallik"
        verbose_name_plural = "Bizning Afzalliklar"

    def __str__(self):
        return self.title

class OurBlog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    minititle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Mini sarlavha")
    content = RichTextField(null=True, blank=True, verbose_name="Mazmun")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm") 
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name="Muallif")
    publish_date = models.DateField(null=True, blank=True, verbose_name="Nashr sanasi")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategoriya")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Bloglar"

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
    
    def events_count(self):
        return self.ourblog_set.count()

    def __str__(self):
        return self.name
    
class OurExpert(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Kichik sarlavha")
    name = models.CharField(max_length=200, verbose_name="Ism")
    position = models.CharField(max_length=200, null=True, blank=True, verbose_name="Lavozim")
    bio = models.TextField(null=True, blank=True, verbose_name="Tarjimai hol")
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Rasm") 
    facebook_url = models.URLField(null=True, blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(null=True, blank=True, verbose_name="Twitter")
    telegram_url = models.URLField(null=True, blank=True, verbose_name="Telegram")
    instagram_url = models.URLField(null=True, blank=True, verbose_name="Instagram")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Bizning Mutaxassis"
        verbose_name_plural = "Bizning Mutaxassislar"

    def __str__(self):
        return self.name

class TeamApplication(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Jamoaga Ariza"
        verbose_name_plural = "Jamoaga Arizalar"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")

    class Meta:
        verbose_name = "Foydalanuvchi Profili"
        verbose_name_plural = "Foydalanuvchi Profillari"

    def __str__(self):
        return self.user.username

class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    service = models.CharField(max_length=100, null=True, blank=True, verbose_name="Xizmat")  
    message = models.TextField(verbose_name="Xabar")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Aloqa Xabari"
        verbose_name_plural = "Aloqa Xabarlari"

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    

class FAQ(models.Model):

    question = models.CharField(max_length=300, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Tez-Tez So'raladigan Savol"
        verbose_name_plural = "Tez-Tez So'raladigan Savollar"

    def __str__(self):
        return self.question
    

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nomi")
    mini_description = models.TextField(verbose_name="Qisqacha tavsif")
    main_image = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Asosiy rasm") 
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Eski narxi")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    images = models.ManyToManyField('ProductImage', blank=True, verbose_name="Rasmlar")
    description = RichTextField(null=True, blank=True, verbose_name="Tavsif")
    specifications = RichTextField(null=True, blank=True, verbose_name="Texnik xususiyatlari")
    status = models.CharField(max_length=50, default='Available', verbose_name="Holati")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_top = models.BooleanField(default=False, verbose_name="TOP mahsulotmi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_details', kwargs={'id': self.id})
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if old_price exists"""
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount)
        return 0
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Rasm")

    class Meta:
        verbose_name = "Mahsulot Rasmi"
        verbose_name_plural = "Mahsulot Rasmlari"


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Foydalanuvchi")

    class Meta:
        verbose_name = "Yoqtirish"
        verbose_name_plural = "Yoqtirishlar"

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    quantity = models.IntegerField(default=1, verbose_name="Miqdori")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Savatcha"
        verbose_name_plural = "Savatchalar"

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def get_discount_amount(self):
        """Chegirma miqdorini hisoblab beradi"""
        if self.product.old_price and self.product.old_price > 0:
            discount_per_item = self.product.old_price - self.product.price
            return discount_per_item * self.quantity
        return 0
    
    def get_discount_percent(self):
        """Chegirma foizini hisoblab beradi"""
        if self.product.old_price and self.product.old_price > 0:
            discount_percent = (self.product.price / self.product.old_price) * 100 - 100
            return abs(discount_percent)  # Musbat qiymat qaytarish
        return 0


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    verification_code = models.CharField(max_length=6, verbose_name="Tasdiqlash kodi")
    email = models.EmailField(verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    is_used = models.BooleanField(default=False, verbose_name="Ishlatilganmi")
    expires_at = models.DateTimeField(verbose_name="Muddati tugash vaqti")

    class Meta:
        verbose_name = "Parol Tiklash Tokeni"
        verbose_name_plural = "Parol Tiklash Tokenlari"

    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at


class EmailVerificationToken(models.Model):
    email = models.EmailField(verbose_name="Email")
    verification_code = models.CharField(max_length=6, verbose_name="Tasdiqlash kodi")
    user_data = models.JSONField(verbose_name="Foydalanuvchi ma'lumotlari")  # Foydalanuvchi ma'lumotlarini saqlaymiz
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    is_used = models.BooleanField(default=False, verbose_name="Ishlatilganmi")
    expires_at = models.DateTimeField(verbose_name="Muddati tugash vaqti")

    class Meta:
        verbose_name = "Email Tasdiqlash Tokeni"
        verbose_name_plural = "Email Tasdiqlash Tokenlari"

    def __str__(self):
        return f"Email verification for {self.email}"

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at


class ChatSession(models.Model):
    """Chat sessiyasi - har bir foydalanuvchi uchun alohida"""
    session_token = models.CharField(max_length=100, unique=True, verbose_name="Sessiya tokeni")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ism")
    is_online = models.BooleanField(default=False, verbose_name="Onlaynmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        verbose_name = "Chat Sessiyasi"
        verbose_name_plural = "Chat Sessiyalari"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat #{self.id} - {self.name or self.email or 'Mehmon'}"


class ChatMessage(models.Model):
    """Chat xabarlari"""
    SENDER_CHOICES = [
        ('user', 'Foydalanuvchi'),
        ('admin', 'Admin'),
        ('bot', 'Bot'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="Sessiya")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Yuboruvchi")
    message = models.TextField(verbose_name="Xabar")
    telegram_message_id = models.IntegerField(null=True, blank=True, verbose_name="Telegram xabar ID")
    is_read = models.BooleanField(default=False, verbose_name="O'qilganmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Chat Xabari"
        verbose_name_plural = "Chat Xabarlari"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"
