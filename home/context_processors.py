

def infos(request):
    from home.models import MainInfo    
    main_infos = MainInfo.objects.first()
    return {'info': main_infos}

def social_links(request):
    from home.models import SocialLink
    social_links = SocialLink.objects.filter(is_active=True)
    return {'social_links': social_links}

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
        return {
            'cart_item_count': 0,
            'cart_items_total': 0
        }

def likes_context(request):
    """Likes ma'lumotlarini barcha sahifalarda mavjud qilish"""
    if request.user.is_authenticated:
        from home.models import Like
        likes_count = Like.objects.filter(user=request.user).count()
        return {
            'likes_count': likes_count
        }
    else:
        return {
            'likes_count': 0
        }