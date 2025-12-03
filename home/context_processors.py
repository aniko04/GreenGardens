

def infos(request):
    from home.models import MainInfo    
    main_infos = MainInfo.objects.first()
    return {'info': main_infos}

def social_links(request):
    from home.models import SocialLink
    social_links = SocialLink.objects.filter(is_active=True)
    return {'social_links': social_links}

def services(request):
    from .models import OurService
    ourservices = OurService.objects.filter(is_active=True)
    return {'ourservices': ourservices}

def populars(request):
    from .models import OurBlog
    populars = OurBlog.objects.filter(is_active=True).order_by('-publish_date')[:3]
    return {'populars': populars}

def cart_context(request):
    """Cart ma'lumotlarini barcha sahifalarda mavjud qilish"""
    if request.user.is_authenticated:
        from home.models import Cart
        cart_items = Cart.objects.filter(user=request.user)
        cart_item_count = sum(item.quantity for item in cart_items)
        return {
            'cart_item_count': cart_item_count,
            'cart_items_total': cart_items.count()
        }
    else:
        # Session-based cart for anonymous users
        session_cart = request.session.get('cart', {})
        cart_item_count = 0
        for item_data in session_cart.values():
            if isinstance(item_data, dict):
                cart_item_count += item_data.get('quantity', 1)
            else:
                # Eski format - oddiy integer
                cart_item_count += item_data
        return {
            'cart_item_count': cart_item_count,
            'cart_items_total': len(session_cart)
        }

def likes_context(request):
    """Likes ma'lumotlarini barcha sahifalarda mavjud qilish"""
    if request.user.is_authenticated:
        from home.models import Like
        # Faqat foydalanuvchining o'z likesini sanash
        likes_count = Like.objects.filter(user=request.user).count()
        return {
            'likes_count': likes_count
        }
    else:
        # Session-based likes for anonymous users
        session_likes = request.session.get('likes', [])
        return {
            'likes_count': len(session_likes)
        }