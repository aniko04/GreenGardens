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
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Q
from home.models import *

# Create your views here.
def home(request):
    # Test messages
    # messages.success(request, "Xush kelibsiz! Bu muvaffaqiyat xabari.")
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

    ourworkprocess = OurWorkProcess.objects.filter(is_active=True)
    ourtestimonials = OurTestimonial.objects.filter(is_active=True)
    ourprojects = OurProject.objects.filter(is_active=True, is_top=True)
    ourfacts = OurFact.objects.filter(is_active=True)
    ourbenefits = OurBenefit.objects.filter(is_active=True)
    ourblogs = OurBlog.objects.filter(is_active=True)
    context = {'sliders': sliders, 
               'intro': intro, 
               'features': features, 
               'ourworkprocess': ourworkprocess,
               'ourtestimonials': ourtestimonials,
               'ourprojects': ourprojects,
               'ourfacts': ourfacts,
               'ourbenefits': ourbenefits,
               'ourblogs': ourblogs
               }
    return render(request, 'home.html', context)
def about(request):
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
            service=service if service != "Choose Services" else None,  # tanlanmagan bo'lsa None
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")   
    
    intro = IntroOurCompany.objects.filter(is_active=True).first()
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
    return render(request, 'services.html')

def service_details(request, id):
    service = get_object_or_404(OurService, id=id, is_active=True)
    # Ochilgan servicega tegishli categoriyalarni olish
    service_categories = service.category.all()
    # Agar servicega category bog'langan bo'lsa, birinchi categoryni olish
    if service_categories.exists():
        current_category = service_categories.first()
    else:
        current_category = None
    
    # Faqat joriy service bilan bog'langan kategoriyalarni sidebar uchun
    categories = service.category.all()
    
    return render(request, 'service-details.html', {
        'service': service,
        'categories': categories,
        'category': current_category,
    })

def category_services(request, id):
    category = ServiceCategory.objects.get(id=id)
    # Kategoriyaga tegishli xizmatlardan birinchisini olish
    services_in_category = OurService.objects.filter(category=category, is_active=True)
    if services_in_category.exists():
        first_service = services_in_category.first()
        return redirect('service_details', id=first_service.id)
    else:
        messages.error(request, "Bu kategoriyada xizmat topilmadi!")
        return redirect('services')

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
    
    # Check if user is authenticated before querying Cart
    if request.user.is_authenticated:
        item = Cart.objects.filter(product=products, user=request.user).first()
    else:
        item = None
    
    print("=================================")
    if item:
        print(item.quantity)
    else:
        print("No cart item found for this product")
    print("=================================")

    # Ko'rishlar sonini oshirish
    products.views += 1
    products.save()
    
    # Related products - pagination qo'shish
    allproducts_queryset = Product.objects.filter(is_active=True, is_top=True).exclude(id=products.id)
    
    # Pagination
    paginator = Paginator(allproducts_queryset, 3)  # 3 tadan chiqarish
    page_number = request.GET.get('page')
    allproducts = paginator.get_page(page_number)
    
    print("-----------------------------")
    for image in products.images.all():
        print(image.image.url)
    print("-----------------------------")
    if not products:
        messages.error(request, "Requested product not found!")
    
    context = {
        'products': products,
        'allproducts': allproducts,
        'page_obj': allproducts,
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
    # Get sorting and category parameters
    sort_by = request.GET.get('sort', '')
    category_id = request.GET.get('category', '')
    
    # Base queryset
    blogs = OurBlog.objects.filter(is_active=True)
    
    # Filter by category if selected
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    # Apply sorting
    if sort_by == 'oldest':
        blogs = blogs.order_by('publish_date', 'id')
    else:
        blogs = blogs.order_by('-publish_date', '-id')  # Default: newest first
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(blogs, 6)  # 6 blogs per page
    page_number = request.GET.get('page')
    ourblogs = paginator.get_page(page_number)
    
    context = {
        'ourblogs': ourblogs,
        'selected_sort': sort_by,
        'selected_category': category_id,
        'categories': categories,
    }
    return render(request, 'blog.html', context)

def blog_details(request, id):
    ourblogs = get_object_or_404(OurBlog, id=id, is_active=True)
    allblogs = OurBlog.objects.filter(is_active=True).exclude(id=ourblogs.id)
    categories = Category.objects.all()
    if not ourblogs:
        messages.error(request, "Requested blog not found!")
    
    context = {
        'allblogs': allblogs,
        'ourblogs': ourblogs,
        'categories': categories
    }
    return render(request, 'blog-details.html', context)

def category_events(request, id):
    ct = get_object_or_404(Category, id=id)
    
    # Get sorting parameter
    sort_by = request.GET.get('sort', '')
    
    # Base queryset for category
    blogs = OurBlog.objects.filter(category=ct, is_active=True)
    
    # Apply sorting
    if sort_by == 'oldest':
        blogs = blogs.order_by('publish_date', 'id')
    else:
        blogs = blogs.order_by('-publish_date', '-id')  # Default: newest first
    
    # Get all categories for dropdown
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(blogs, 6)  # 6 blogs per page
    page_number = request.GET.get('page')
    ourblogs = paginator.get_page(page_number)
    
    context = {
        'ourblogs': ourblogs,
        'category': ct,
        'selected_sort': sort_by,
        'selected_category': str(ct.id),
        'categories': categories,
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
        # Foydalanuvchi login qilmagan bo'lsa, sessiondan cart ma'lumotlarini olish
        session_cart = request.session.get('cart', {})
        
        # Session cart ma'lumotlarini qayta ishlash
        cart_items = []
        subtotal = 0
        
        if session_cart:
            for product_id, item_data in session_cart.items():
                try:
                    product = Product.objects.get(id=product_id, is_active=True)
                    
                    # Eski format (int) va yangi format (dict) ni qo'llab-quvvatlash
                    if isinstance(item_data, dict):
                        quantity = item_data.get('quantity', 1)
                    else:
                        # Eski format - oddiy integer
                        quantity = item_data
                    
                    total_price = product.price * quantity
                    
                    # Cart item uchun ma'lumotlar
                    cart_item = {
                        'id': product_id,  # Session uchun product_id ishlatamiz
                        'product': product,
                        'quantity': quantity,
                        'total_price': total_price
                    }
                    cart_items.append(cart_item)
                    subtotal += total_price
                except Product.DoesNotExist:
                    continue
        
        # Yetkazib berish narxi
        shipping = 20 if cart_items else 0
        
        # Umumiy narx
        total = subtotal + shipping
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'items_count': len(cart_items),
            'session_cart': session_cart
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
        # Foydalanuvchi login qilmagan bo'lsa, sessiondan like qilingan mahsulotlarni olish
        session_likes = request.session.get('likes', [])
        
        # Session like IDs orqali mahsulotlarni olish
        if session_likes:
            liked_products = Product.objects.filter(
                id__in=session_likes,
                is_active=True
            )
            
            # Pagination qo'shish
            paginator = Paginator(liked_products, 12)  # Har sahifada 12 ta mahsulot
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'liked_products': page_obj,
                'page_obj': page_obj,
                'likes_count': liked_products.count(),
                'session_likes': session_likes
            }
        else:
            context = {
                'liked_products': None,
                'page_obj': None,
                'likes_count': 0,
                'session_likes': []
            }
        
        return render(request, 'my-likes.html', context)
    
def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    context = {'faqs': faqs}
    return render(request, 'faq.html', context)

def search(request):
    query = request.GET.get('q', '').strip()
    products = []
    services = []
    
    if query:
        # Product qidirish - name, mini_description va description maydonlarida
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(mini_description__icontains=query) | 
            Q(description__icontains=query),
            is_active=True
        ).distinct()
        
        # Service qidirish - title, subtitle, description va content maydonlarida
        services = OurService.objects.filter(
            Q(pagename__icontains=query) | 
            Q(subtitle__icontains=query) | 
            Q(description__icontains=query) | 
            Q(content__icontains=query),
            is_active=True
        ).distinct()
    
    # Pagination
    products_paginator = Paginator(products, 6)
    services_paginator = Paginator(services, 6)
    
    products_page = request.GET.get('products_page')
    services_page = request.GET.get('services_page')
    
    products_obj = products_paginator.get_page(products_page)
    services_obj = services_paginator.get_page(services_page)
    
    # DEBUG: Product names-ni konsolga chop etish
    if products:
        print("DEBUG: Found products:")
        for product in products[:3]:  # Faqat birinchi 3 tani
            print(f"  - ID: {product.id}, Name: '{product.name}'")
    
    context = {
        'query': query,
        'products': products_obj,
        'services': services_obj,
        'products_count': products.count(),
        'services_count': services.count(),
        'total_results': products.count() + services.count(),
    }
    
    return render(request, 'search.html', context)


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
            # Session-dagi likes va cart ma'lumotlarini saqlash
            session_likes = request.session.get('likes', [])
            session_cart = request.session.get('cart', {})
            
            # Login qilish
            login(request, user)
            
            # Session-dagi likesni database-ga ko'chirish
            if session_likes:
                for product_id in session_likes:
                    try:
                        product = Product.objects.get(id=product_id)
                        # Agar allaqachon like qilmagan bo'lsa, qo'shish
                        Like.objects.get_or_create(user=user, product=product)
                    except Product.DoesNotExist:
                        continue
                
                # Session-dagi likesni tozalash
                request.session['likes'] = []
                request.session.modified = True
            
            # Session-dagi cartni database-ga ko'chirish
            if session_cart:
                for product_id, item_data in session_cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        # Quantity ni aniqlash (eski va yangi formatni qo'llab-quvvatlash)
                        if isinstance(item_data, dict):
                            quantity = item_data.get('quantity', 1)
                        else:
                            quantity = item_data
                        
                        # Agar allaqachon cartda bo'lsa, miqdorni qo'shish, yo'qsa yangi qo'shish
                        cart_item, created = Cart.objects.get_or_create(
                            user=user,
                            product=product,
                            defaults={'quantity': quantity}
                        )
                        if not created:
                            # Agar mavjud bo'lsa, miqdorni qo'shish
                            cart_item.quantity += quantity
                            cart_item.save()
                    except Product.DoesNotExist:
                        continue
                
                # Session-dagi cartni tozalash
                request.session['cart'] = {}
                request.session.modified = True
            
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
        confirm_password = request.POST.get('confirm_password')

        # Parollar bir xil ekanligini tekshirish
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Username sifatida emailni ishlatamiz
        username = email.split('@')[0]

        # Email allaqachon ro'yxatdan o'tganligini tekshirish
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            # Agar username mavjud bo'lsa, raqam qo'shamiz
            import random
            username = f"{username}{random.randint(100, 999)}"

        # 6 xonali tasdiqlash kodini yaratish
        import random
        verification_code = str(random.randint(100000, 999999))
        
        # Foydalanuvchi ma'lumotlarini saqlaymiz
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'phone': phone
        }
        
        # Eski tokenlarni o'chirish
        EmailVerificationToken.objects.filter(email=email).delete()
        
        # Yangi token yaratish
        from django.utils import timezone
        from datetime import timedelta
        
        verification_token = EmailVerificationToken.objects.create(
            email=email,
            verification_code=verification_code,
            user_data=user_data,
            expires_at=timezone.now() + timedelta(minutes=15)  # 15 daqiqa amal qiladi
        )
        
        # Email yuborish
        subject = 'Email Verification Code - GreenGardens'
        message = f"""
        Hi there!

        Welcome to GreenGardens! Please verify your email address to complete your registration.

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
            messages.success(request, f"Verification code has been sent to {email}. Please check your email and enter the code to complete registration.")
            return redirect('email_verification')
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")
            # Development rejimida kodni ko'rsatish
            messages.info(request, f"Development mode - Your verification code is: {verification_code}")
            return redirect('email_verification')

    return render(request, 'login.html')


# --- EMAIL VERIFICATION VIEW ---
@csrf_protect
def email_verification_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = request.POST.get('verification_code')
        
        if email and verification_code:
            try:
                # Token topish
                from django.utils import timezone
                token = EmailVerificationToken.objects.get(
                    email=email,
                    verification_code=verification_code,
                    is_used=False
                )
                
                # Token muddati tugaganligini tekshirish
                if token.is_expired():
                    messages.error(request, "Verification code has expired. Please register again.")
                    return redirect('register')
                
                # Foydalanuvchi ma'lumotlarini olish
                user_data = token.user_data
                
                # Foydalanuvchini yaratish
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                UserProfile.objects.create(user=user, phone=user_data['phone'])
                
                # Tokenni ishlatilgan deb belgilash
                token.is_used = True
                token.save()
                
                messages.success(request, "Email verification successful! Your account has been created. You can now log in.")
                return redirect('login')
                
            except EmailVerificationToken.DoesNotExist:
                messages.error(request, "Invalid verification code or email address.")
        else:
            messages.error(request, "Please provide both email and verification code.")
    
    return render(request, 'email-verification.html')


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


# ==================== CHAT VIEWS ====================
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["POST"])
def chat_init(request):
    """Chat sessiyasini boshlash"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '')
        phone = data.get('phone', '')
        email = data.get('email', '')  # Backward compatibility uchun

        # Session token yaratish
        session_token = str(uuid.uuid4())

        # Chat sessiyasini yaratish
        chat_session = ChatSession.objects.create(
            session_token=session_token,
            user=request.user if request.user.is_authenticated else None,
            phone=phone,
            email=email,
            name=name,
            is_online=True
        )

        return JsonResponse({
            'status': 'success',
            'session_token': session_token,
            'session_id': chat_session.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def chat_send_message(request):
    """Foydalanuvchidan xabar qabul qilish"""
    try:
        data = json.loads(request.body)
        session_token = data.get('session_token')
        message_text = data.get('message')

        if not session_token or not message_text:
            return JsonResponse({
                'status': 'error',
                'message': 'Session token va xabar talab qilinadi'
            }, status=400)

        # Chat sessiyasini topish
        try:
            chat_session = ChatSession.objects.get(session_token=session_token)
        except ChatSession.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Chat sessiyasi topilmadi'
            }, status=404)

        # Xabarni saqlash
        chat_message = ChatMessage.objects.create(
            session=chat_session,
            sender='user',
            message=message_text
        )

        # Auto-response faqat birinchi xabarda
        auto_response = None
        user_message_count = chat_session.messages.filter(sender='user').count()

        if user_message_count == 1:  # Faqat birinchi xabar
            auto_response = "Xabaringiz qabul qilindi! Tez orada admin javob beradi."
            ChatMessage.objects.create(
                session=chat_session,
                sender='bot',
                message=auto_response
            )

        # Telegram orqali admin'ga xabar yuborish
        try:
            from home.telegram_utils import send_message_to_admin, format_chat_message_for_admin

            telegram_message = format_chat_message_for_admin(chat_session, message_text)
            telegram_message_id = send_message_to_admin(telegram_message)

            # Telegram message ID ni saqlash (reply uchun)
            if telegram_message_id:
                chat_message.telegram_message_id = telegram_message_id
                chat_message.save()
        except Exception as e:
            # Telegram xatolik bo'lsa ham, asosiy funksiya ishlaydi
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Telegram ga xabar yuborishda xatolik: {e}")

        return JsonResponse({
            'status': 'success',
            'message_id': chat_message.id,
            'auto_response': auto_response
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def chat_get_messages(request, session_token):
    """Chat xabarlarini olish"""
    try:
        chat_session = ChatSession.objects.get(session_token=session_token)
        messages = chat_session.messages.all().values(
            'id', 'sender', 'message', 'created_at', 'is_read'
        )

        return JsonResponse({
            'status': 'success',
            'messages': list(messages)
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Chat sessiyasi topilmadi'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def chat_admin_reply(request):
    """Admin tomonidan javob yuborish (admin panel uchun)"""
    if not request.user.is_staff:
        return JsonResponse({
            'status': 'error',
            'message': 'Ruxsat yo\'q'
        }, status=403)

    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message_text = data.get('message')

        if not session_id or not message_text:
            return JsonResponse({
                'status': 'error',
                'message': 'Session ID va xabar talab qilinadi'
            }, status=400)

        # Chat sessiyasini topish
        try:
            chat_session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Chat sessiyasi topilmadi'
            }, status=404)

        # Admin javobini saqlash
        chat_message = ChatMessage.objects.create(
            session=chat_session,
            sender='admin',
            message=message_text
        )

        return JsonResponse({
            'status': 'success',
            'message_id': chat_message.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)