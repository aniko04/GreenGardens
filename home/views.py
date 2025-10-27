from django.http import HttpResponseNotFound, JsonResponse
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from home.models import *

# Create your views here.
def home(request):
    # Test messages
    messages.success(request, "Xush kelibsiz! Bu muvaffaqiyat xabari.")
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('tel')
        service = request.POST.get('service')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service if service != "Choose Services" else None,  # tanlanmagan bo‘lsa None
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")   
    
    sliders = Mainslider.objects.filter(is_active=True)
    intro = IntroOurCompany.objects.filter(is_active=True).first()
    features = MainFeature.objects.filter(is_active=True)
    ourservices = OurService.objects.filter(is_active=True, is_top=True)
    ourworkprocess = OurWorkProcess.objects.filter(is_active=True)
    ourtestimonials = OurTestimonial.objects.filter(is_active=True)
    ourprojects = OurProject.objects.filter(is_active=True, is_top=True)
    ourfacts = OurFact.objects.filter(is_active=True)
    ourbenefits = OurBenefit.objects.filter(is_active=True)
    ourblogs = OurBlog.objects.filter(is_active=True)
    context = {'sliders': sliders, 
               'intro': intro, 
               'features': features, 
               'ourservices': ourservices, 
               'ourworkprocess': ourworkprocess,
               'ourtestimonials': ourtestimonials,
               'ourprojects': ourprojects,
               'ourfacts': ourfacts,
               'ourbenefits': ourbenefits,
               'ourblogs': ourblogs
               }
    return render(request, 'home.html', context)
def about(request):
    intro = IntroOurCompany.objects.filter(is_active=True).last()
    features = MainFeature.objects.filter(is_active=True)
    ourfacts = OurFact.objects.filter(is_active=True)
    ourbenefits = OurBenefit.objects.filter(is_active=True)
    ourtestimonials = OurTestimonial.objects.filter(is_active=True)
    ourexperts = OurExpert.objects.filter(is_active=True)
   


    context = {'intro': intro,
               'features': features,
               'ourfacts': ourfacts,
                'ourbenefits': ourbenefits,
                'ourtestimonials': ourtestimonials,
                'ourexperts': ourexperts
               }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('tel')
        service = request.POST.get('service')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service if service != "Choose Services" else None,  # tanlanmagan bo‘lsa None
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        #return redirect('contact')  # contact url nomi bilan qayta yo‘naltirish
        return render(request, 'contact.html')

    return render(request, 'contact.html')

def services(request):
    ourservices = OurService.objects.filter(is_active=True)
    context = {'ourservices': ourservices}
    return render(request, 'services.html', context)

def service_details(request, id):
    ourservices = get_object_or_404(OurService, id=id, is_active=True)
    allservices = OurService.objects.filter(is_active=True).exclude(id=ourservices.id)
    faqs = FAQ.objects.filter(is_active=True)


    if not ourservices:
        messages.error(request, "Requested service not found!")
    
    context = {
        'allservices': allservices,
        'ourservices': ourservices,
        'faqs': faqs
    }
    return render(request, 'service-details.html', context)

def projects(request):
    ourprojects = OurProject.objects.filter(is_active=True)
    context = {'ourprojects': ourprojects}
    return render(request, 'project.html', context)

def project_details(request, id):
    ourprojects = get_object_or_404(OurProject, id=id, is_active=True)
    allprojects = OurProject.objects.filter(is_active=True,is_top=True).exclude(id=ourprojects.id)

    if not ourprojects:
        messages.error(request, "Requested project not found!")
    
    context = {
        'allprojects': allprojects,
        'ourprojects': ourprojects,
    }
    return render(request, 'project-details.html', context)

def products(request):
    # Get sorting parameter
    sort_by = request.GET.get('sort', '')
    
    # Base queryset
    products = Product.objects.filter(is_active=True)
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'newest':
        products = products.order_by('-id')  # Assuming newer products have higher IDs
    elif sort_by == 'views_high':
        products = products.order_by('-views')  # Ko'p ko'rilgan mahsulotlar avval
    elif sort_by == 'views_low':
        products = products.order_by('views')  # Kam ko'rilgan mahsulotlar avval
    else:
        products = products.order_by('name')  # Default sorting by name
    
    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,  
        'page_obj': page_obj,
        'selected_sort': sort_by,
    }

    return render(request, 'products.html', context)

def product_details(request, id):
    products = get_object_or_404(Product, id=id, is_active=True)
    item = Cart.objects.filter(product=products, user=request.user).first()
    print("=================================")
    if item:
        print(item.quantity)
    else:
        print("No cart item found for this product")
    print("=================================")

    # Ko'rishlar sonini oshirish
    products.views += 1
    products.save()
    
    allproducts = Product.objects.filter(is_active=True, is_top=True).exclude(id=products.id)
    print("-----------------------------")
    for image in products.images.all():
        print(image.image.url)
    print("-----------------------------")
    if not products:
        messages.error(request, "Requested product not found!")
    
    context = {
        'products': products,
        'allproducts': allproducts,
        'item': item
    }
    return render(request, 'product-details.html', context)

def team(request):
    ourexperts = OurExpert.objects.filter(is_active=True)
    context = {'ourexperts': ourexperts}
    return render(request, 'team.html', context)

def team_details(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('tel')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            TeamApplication.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )

            # AJAX so'rov uchun JSON javob qaytarish
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Your job application has been submitted successfully!'
                })
            
            # Oddiy HTTP so'rov uchun
            messages.success(request, "Your job application has been submitted successfully!")
            return redirect('team_details', id=id)
            
        except Exception as e:
            # Xatolik yuz bergan holat
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'An error occurred while submitting your application. Please try again.'
                })
            
            messages.error(request, "An error occurred while submitting your application. Please try again.")
            return redirect('team_details', id=id)

    ourexperts = get_object_or_404(OurExpert, id=id, is_active=True)
    allteam = OurExpert.objects.filter(is_active=True).exclude(id=ourexperts.id)

    if not ourexperts:
        messages.error(request, "Requested team member not found!")
    
    context = {
        'allteam': allteam,
        'ourexperts': ourexperts,
    }

    return render(request, 'team-details.html', context)

def blog(request):
    ourblogs = OurBlog.objects.filter(is_active=True)
    context = {
        'ourblogs': ourblogs
    }
    return render(request, 'blog.html', context)

def cart(request):
    if request.user.is_authenticated:
        # Foydalanuvchining cart itemlarini olish
        cart_items = Cart.objects.filter(user=request.user)
        
        # Subtotal hisoblash
        subtotal = sum(item.get_total_price() for item in cart_items)
        
        # Yetkazib berish narxi
        shipping = 20
        
        # Umumiy narx
        total = subtotal + shipping
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'items_count': cart_items.count()
        }
        
        return render(request, 'cart.html', context)
    else:
        # Foydalanuvchi login qilmagan bo'lsa, bo'sh cart ko'rsatish
        context = {
            'cart_items': None,
            'subtotal': 0,
            'shipping': 20,
            'total': 20,
            'items_count': 0
        }
        return render(request, 'cart.html', context)

def my_likes(request):

    if request.user.is_authenticated:
        # Foydalanuvchining like qilgan mahsulotlarini olish
        liked_products = Product.objects.filter(
            like__user=request.user,
            is_active=True
        ).distinct()
        
        # Pagination qo'shish
        paginator = Paginator(liked_products, 12)  # Har sahifada 12 ta mahsulot
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'liked_products': page_obj,
            'page_obj': page_obj,
            'likes_count': liked_products.count()
        }
        
        return render(request, 'my-likes.html', context)
    else:
        # Foydalanuvchi login qilmagan bo'lsa, login sahifasiga yo'naltirish yoki bo'sh sahifa ko'rsatish
        messages.warning(request, "Yoqtirgan mahsulotlaringizni ko'rish uchun tizimga kiring!")
        context = {
            'liked_products': None,
            'page_obj': None,
            'likes_count': 0
        }
        return render(request, 'my-likes.html', context)
    
def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    context = {'faqs': faqs}
    return render(request, 'faq.html', context)


# --- LOGIN VIEW ---
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Email orqali foydalanuvchini topish
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

        # Username va password bilan authenticate qilish
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # tizimga kirgandan so'ng bosh sahifaga yo'naltirish
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


# --- REGISTER VIEW ---
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Username sifatida emailni ishlatamiz (siz istasangiz alohida username maydon ham qo‘shish mumkin)
        username = email.split('@')[0]

        if User.objects.filter(username=username).exists():
            messages.error(request, "This user already exists!")
            return redirect('register')

        # Yangi foydalanuvchi yaratish
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'login.html')


# --- LOGOUT VIEW ---
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def checkout(request):
    return render(request, 'checkout.html')

# --- PASSWORD RESET VIEWS ---
def password_reset_request(request):
    """Password reset request view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email)
                
                # Generate 6-digit verification code
                import random
                verification_code = str(random.randint(100000, 999999))
                
                # Create or update password reset token
                from django.utils import timezone
                from datetime import timedelta
                
                # Delete old tokens for this user
                PasswordResetToken.objects.filter(user=user).delete()
                
                # Create new token
                reset_token = PasswordResetToken.objects.create(
                    user=user,
                    email=email,
                    verification_code=verification_code,
                    expires_at=timezone.now() + timedelta(minutes=15)  # 15 daqiqa amal qiladi
                )
                
                # Send email with verification code
                subject = 'Password Reset Verification Code - GreenGardens'
                message = f"""
                Hi {user.username},

                You have requested to reset your password for GreenGardens.

                Your verification code is: {verification_code}

                This code will expire in 15 minutes.

                If you didn't request this, please ignore this email.

                Best regards,
                GreenGardens Team
                """
                
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, f"Verification code has been sent to {email}. Please check your email and enter the code.")
                    return redirect('password_reset_verify')
                except Exception as e:
                    messages.error(request, f"Error sending email: {str(e)}")
                    # For development, show the code in message
                    messages.info(request, f"Development mode - Your verification code is: {verification_code}")
                    return redirect('password_reset_verify')
                
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
        else:
            messages.error(request, "Please provide a valid email address.")
    
    return render(request, 'password-reset.html')

def password_reset_verify(request):
    """Password reset verification code view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = request.POST.get('verification_code')
        
        if email and verification_code:
            try:
                # Find valid token
                from django.utils import timezone
                reset_token = PasswordResetToken.objects.get(
                    email=email,
                    verification_code=verification_code,
                    is_used=False
                )
                
                # Check if token is expired
                if reset_token.is_expired():
                    messages.error(request, "Verification code has expired. Please request a new one.")
                    return redirect('password_reset')
                
                # Mark token as used and redirect to password reset form
                reset_token.is_used = True
                reset_token.save()
                
                # Generate URL parameters for password reset
                user = reset_token.user
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                return redirect('password_reset_confirm', uidb64=uid, token=token)
                
            except PasswordResetToken.DoesNotExist:
                messages.error(request, "Invalid verification code or email address.")
        else:
            messages.error(request, "Please provide both email and verification code.")
    
    return render(request, 'password-reset-verify.html')

def password_reset_confirm(request, uidb64, token):
    """Password reset confirmation view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        
        return render(request, 'password-reset-confirm.html', {'user': user})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('password_reset')