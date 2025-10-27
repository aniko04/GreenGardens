from xmlrpc import client
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MainInfo(models.Model):
    site_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    footer_text = models.TextField()
    opening_hours = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.site_name

class SocialLink(models.Model):
    platform = models.CharField(max_length=100)
    icon = models.CharField(max_length=100,null=True, blank=True)  
    url = models.URLField()
    total_followers = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.platform
    
class Mainslider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    button_1_name = models.CharField(max_length=100, null=True, blank=True)
    button_1_url = models.URLField(null=True, blank=True)
    button_2_name = models.CharField(max_length=100, null=True, blank=True)
    button_2_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class IntroOurCompany(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon1 = models.CharField(max_length=100,null=True, blank=True)
    icon_text1 = models.CharField(max_length=200, null=True, blank=True)
    icon2 = models.CharField(max_length=100,null=True, blank=True)
    icon_text2 = models.CharField(max_length=200, null=True, blank=True)
    image1 = models.ImageField(upload_to='', null=True, blank=True) 
    image2 = models.ImageField(upload_to='', null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    list1= models.TextField(null=True, blank=True)
    list2= models.TextField(null=True, blank=True)
    list3= models.TextField(null=True, blank=True)
    button_name = models.CharField(max_length=100, null=True, blank=True)
    button_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class MainFeature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=100,null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class OurService(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    pagename = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    icon = models.CharField(max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    url = models.URLField(null=True, blank=True)
    is_top = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_details', kwargs={'id': self.id})
    
class OurWorkProcess(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pagename = models.CharField(max_length=100, null=True, blank=True)
    step_number = models.IntegerField()
    page_text = models.CharField(max_length=200, null=True, blank=True)
    icon = models.CharField(max_length=100,null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class OurTestimonial(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    rate = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OurProject(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    category = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=200, null=True, blank=True)
    project_date = models.DateField(null=True, blank=True)
    button_name = models.CharField(max_length=100, null=True, blank=True)
    project_link = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class OurFact(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    project_number = models.IntegerField(default=0)
    project_content = models.CharField(max_length=200, null=True, blank=True)
    customer_number = models.IntegerField(default=0,null=True, blank=True)
    customer_content = models.CharField(max_length=200, null=True, blank=True)
    button_name = models.CharField(max_length=100, null=True, blank=True)
    button_url = models.URLField(null=True, blank=True)
    button_text = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class OurBenefit(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    is_active = models.BooleanField(default=True)
    benefit1= models.CharField(max_length=200, null=True, blank=True)
    benefit1_text= models.CharField(max_length=200, null=True, blank=True)
    benefit1_quality1 = models.CharField(max_length=100, null=True, blank=True)
    benefit1_quality2 = models.CharField(max_length=100, null=True, blank=True)
    benefit1_quality3 = models.CharField(max_length=100, null=True, blank=True)
    benefit1_quality4 = models.CharField(max_length=100, null=True, blank=True)
    benefit2= models.CharField(max_length=200, null=True, blank=True)
    benefit2_text= models.CharField(max_length=200, null=True, blank=True)
    client_count = models.IntegerField(default=0)
    client_text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

class OurBlog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    minititle = models.CharField(max_length=200, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    author = models.CharField(max_length=100, null=True, blank=True)
    publish_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class OurExpert(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    telegram_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TeamApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)  
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    

class FAQ(models.Model):

    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    mini_description = models.TextField()
    main_image = models.ImageField(upload_to='', null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    views = models.IntegerField(default=0)  # Ko'rishlar soni
    images = models.ManyToManyField('ProductImage', blank=True)
    description = RichTextField(null=True, blank=True)
    specifications = RichTextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Available')
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
