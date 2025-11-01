from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Cart, Like, Product

def user_product_like_api(request, product_id):
    try:
        p = Product.objects.get(id=product_id, is_active=True)
        
        if request.user.is_authenticated:
            result = Like.objects.filter(user=request.user, product=p).exists()
        else:
            # Session-based like check for anonymous users
            session_likes = request.session.get('likes', [])
            result = int(product_id) in session_likes
        
        return JsonResponse({'liked': result}, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'liked': False, 'error': 'Product not found'}, safe=False)

def user_like_add_api(request, product_id):
    if request.method == 'POST':
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            
            if request.user.is_authenticated:
                # Authenticated user - database like
                like, created = Like.objects.get_or_create(user=request.user, product=p)
                if created:
                    user_likes_count = Like.objects.filter(user=request.user).count()
                    print(f"DEBUG: User {request.user.id} LIKED product {product_id}. User likes count: {user_likes_count}")
                    return JsonResponse({
                        'status': 'liked', 
                        'message': 'Mahsulot likega qo\'shildi!',
                        'total_likes': user_likes_count
                    }, safe=False)
                else:
                    like.delete()
                    user_likes_count = Like.objects.filter(user=request.user).count()
                    print(f"DEBUG: User {request.user.id} UNLIKED product {product_id}. User likes count: {user_likes_count}")
                    return JsonResponse({
                        'status': 'unliked', 
                        'message': 'Mahsulot likedan o\'chirildi!',
                        'total_likes': user_likes_count
                    }, safe=False)
            else:
                # Anonymous user - session-based like
                session_likes = request.session.get('likes', [])
                product_id_int = int(product_id)
                
                if product_id_int in session_likes:
                    # Unlike - remove from session
                    session_likes.remove(product_id_int)
                    request.session['likes'] = session_likes
                    request.session.modified = True
                    print(f"DEBUG: Anonymous user UNLIKED product {product_id}. Session likes count: {len(session_likes)}")
                    return JsonResponse({
                        'status': 'unliked',
                        'message': 'Mahsulot likedan o\'chirildi!',
                        'total_likes': len(session_likes)
                    }, safe=False)
                else:
                    # Like - add to session
                    session_likes.append(product_id_int)
                    request.session['likes'] = session_likes
                    request.session.modified = True
                    print(f"DEBUG: Anonymous user LIKED product {product_id}. Session likes count: {len(session_likes)}")
                    return JsonResponse({
                        'status': 'liked',
                        'message': 'Mahsulot likega qo\'shildi!',
                        'total_likes': len(session_likes)
                    }, safe=False)
                    
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'POST method required'}, safe=False)

def cart_api(request, product_id):
    try:
        p = Product.objects.get(id=product_id, is_active=True)
        
        if request.user.is_authenticated:
            result = Cart.objects.filter(user=request.user, product=p).exists()
        else:
            # Session-based cart check for anonymous users
            session_cart = request.session.get('cart', {})
            result = str(product_id) in session_cart
        
        return JsonResponse({'added': result}, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'added': False, 'error': 'Product not found'}, safe=False)

def add_to_cart_api(request, product_id):
    if request.method == 'POST':
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            
            if request.user.is_authenticated:
                # Authenticated user - database cart
                cart_item, created = Cart.objects.get_or_create(user=request.user, product=p)
                if created:
                    return JsonResponse({'status': 'added', 'cart_item_id': cart_item.id}, safe=False)
                else:
                    cart_item.delete()
                    return JsonResponse({'status': 'removed'}, safe=False)
            else:
                # Anonymous user - session-based cart
                session_cart = request.session.get('cart', {})
                product_id_str = str(product_id)
                
                if product_id_str in session_cart:
                    # Remove from cart
                    del session_cart[product_id_str]
                    request.session['cart'] = session_cart
                    request.session.modified = True
                    print(f"DEBUG: Anonymous user REMOVED product {product_id} from cart. Session cart count: {len(session_cart)}")
                    return JsonResponse({'status': 'removed'}, safe=False)
                else:
                    # Add to cart with quantity 1
                    session_cart[product_id_str] = {'quantity': 1}
                    request.session['cart'] = session_cart
                    request.session.modified = True
                    print(f"DEBUG: Anonymous user ADDED product {product_id} to cart. Session cart count: {len(session_cart)}")
                    return JsonResponse({'status': 'added'}, safe=False)
                    
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'POST method required'}, safe=False)

def cart_count_api(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        # Barcha mahsulotlar miqdorini hisoblaymiz
        total_quantity = sum(item.quantity for item in cart_items)
        return JsonResponse({'cart_count': total_quantity}, safe=False)
    else:
        # Session-based cart for anonymous users
        session_cart = request.session.get('cart', {})
        total_quantity = 0
        for item_data in session_cart.values():
            if isinstance(item_data, dict):
                total_quantity += item_data.get('quantity', 1)
            else:
                # Eski format - oddiy integer
                total_quantity += item_data
        return JsonResponse({'cart_count': total_quantity}, safe=False)

def likes_count_api(request):
    if request.user.is_authenticated:
        # Faqat current user ning likes soni
        user_likes_count = Like.objects.filter(user=request.user).count()
        print(f"DEBUG: User {request.user.id} likes: {user_likes_count}")
        return JsonResponse({
            'likes_count': user_likes_count
        }, safe=False)
    else:
        # Session-based likes for anonymous users
        session_likes = request.session.get('likes', [])
        likes_count = len(session_likes)
        print(f"DEBUG: Anonymous user session likes: {likes_count}")
        return JsonResponse({
            'likes_count': likes_count
        }, safe=False)

# CART MANAGEMENT API'LAR

def remove_from_cart_api(request, cart_id):
    """Cart dan mahsulot o'chirish API"""
    try:
        if request.user.is_authenticated:
            # Authenticated user - database cart
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            product_name = cart_item.product.name
            cart_item.delete()
            
            # Yangilangan cart ma'lumotlarini olish
            cart_items = Cart.objects.filter(user=request.user)
            total_items = sum(item.quantity for item in cart_items)
            total_price = sum(item.get_total_price() for item in cart_items)
            
            return JsonResponse({
                'status': 'removed',
                'message': f"'{product_name}' mahsuloti cartdan o'chirildi",
                'cart_total_items': total_items,
                'cart_total_price': float(total_price)
            }, safe=False)
        else:
            # Anonymous user - session-based cart
            session_cart = request.session.get('cart', {})
            cart_id_str = str(cart_id)
            
            if cart_id_str in session_cart:
                # Get product name before removing
                try:
                    product = Product.objects.get(id=cart_id)
                    product_name = product.name
                except Product.DoesNotExist:
                    product_name = "Mahsulot"
                
                del session_cart[cart_id_str]
                request.session['cart'] = session_cart
                request.session.modified = True
                
                # Calculate updated totals
                total_items = sum(item.get('quantity', 1) for item in session_cart.values() if isinstance(item, dict))
                total_price = 0
                for product_id, item_data in session_cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                        total_price += product.price * quantity
                    except Product.DoesNotExist:
                        continue
                
                return JsonResponse({
                    'status': 'removed',
                    'message': f"'{product_name}' mahsuloti cartdan o'chirildi",
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
            else:
                return JsonResponse({'status': 'error', 'message': 'Mahsulot topilmadi'}, safe=False)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)

def update_cart_quantity_api(request, cart_id):
    """Cart miqdorini yangilash API"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, safe=False)
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                
                # Yangilangan ma'lumotlarni olish
                cart_items = Cart.objects.filter(user=request.user)
                total_items = sum(item.quantity for item in cart_items)
                total_price = sum(item.get_total_price() for item in cart_items)
                
                return JsonResponse({
                    'status': 'updated',
                    'message': 'Miqdor yangilandi',
                    'item_quantity': cart_item.quantity,
                    'item_total': float(cart_item.get_total_price()),
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
            else:
                # Miqdor 0 yoki manfiy bo'lsa o'chirish
                product_name = cart_item.product.name
                cart_item.delete()
                
                cart_items = Cart.objects.filter(user=request.user)
                total_items = sum(item.quantity for item in cart_items)
                total_price = sum(item.get_total_price() for item in cart_items)
                
                return JsonResponse({
                    'status': 'removed',
                    'message': f"'{product_name}' mahsuloti cartdan o'chirildi",
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)
    
    return JsonResponse({'status': 'error', 'message': 'POST method required'}, safe=False)

def increase_cart_quantity_api(request, cart_id):
    """Cart miqdorini oshirish API"""
    try:
        if request.user.is_authenticated:
            # Authenticated user - database cart
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()
            
            # Yangilangan ma'lumotlarni olish
            cart_items = Cart.objects.filter(user=request.user)
            total_items = sum(item.quantity for item in cart_items)
            total_price = sum(item.get_total_price() for item in cart_items)
            
            return JsonResponse({
                'status': 'increased',
                'message': 'Miqdor oshirildi',
                'item_quantity': cart_item.quantity,
                'item_total': float(cart_item.get_total_price()),
                'cart_total_items': total_items,
                'cart_total_price': float(total_price)
            }, safe=False)
        else:
            # Anonymous user - session-based cart
            session_cart = request.session.get('cart', {})
            cart_id_str = str(cart_id)
            
            if cart_id_str in session_cart:
                # Get current quantity
                item_data = session_cart[cart_id_str]
                if isinstance(item_data, dict):
                    current_quantity = item_data.get('quantity', 1)
                    session_cart[cart_id_str]['quantity'] = current_quantity + 1
                else:
                    # Convert old format to new format
                    session_cart[cart_id_str] = {'quantity': item_data + 1}
                
                request.session['cart'] = session_cart
                request.session.modified = True
                
                # Get product and calculate totals
                product = Product.objects.get(id=cart_id)
                new_quantity = session_cart[cart_id_str]['quantity'] if isinstance(session_cart[cart_id_str], dict) else session_cart[cart_id_str]
                item_total = product.price * new_quantity
                
                # Calculate updated totals
                total_items = 0
                total_price = 0
                for product_id, item_data in session_cart.items():
                    try:
                        p = Product.objects.get(id=product_id)
                        quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                        total_items += quantity
                        total_price += p.price * quantity
                    except Product.DoesNotExist:
                        continue
                
                return JsonResponse({
                    'status': 'increased',
                    'message': 'Miqdor oshirildi',
                    'item_quantity': new_quantity,
                    'item_total': float(item_total),
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
            else:
                return JsonResponse({'status': 'error', 'message': 'Mahsulot topilmadi'}, safe=False)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)

def decrease_cart_quantity_api(request, cart_id):
    """Cart miqdorini kamaytirish API"""
    try:
        if request.user.is_authenticated:
            # Authenticated user - database cart
            cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                
                # Yangilangan ma'lumotlarni olish
                cart_items = Cart.objects.filter(user=request.user)
                total_items = sum(item.quantity for item in cart_items)
                total_price = sum(item.get_total_price() for item in cart_items)
                
                return JsonResponse({
                    'status': 'decreased',
                    'message': 'Miqdor kamaytirildi',
                    'item_quantity': cart_item.quantity,
                    'item_total': float(cart_item.get_total_price()),
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
            else:
                # Miqdor 1 dan kam bo'lsa o'chirish
                product_name = cart_item.product.name
                cart_item.delete()
                
                cart_items = Cart.objects.filter(user=request.user)
                total_items = sum(item.quantity for item in cart_items)
                total_price = sum(item.get_total_price() for item in cart_items)
                
                return JsonResponse({
                    'status': 'removed',
                    'message': f"'{product_name}' mahsuloti cartdan o'chirildi",
                    'cart_total_items': total_items,
                    'cart_total_price': float(total_price)
                }, safe=False)
        else:
            # Anonymous user - session-based cart
            session_cart = request.session.get('cart', {})
            cart_id_str = str(cart_id)
            
            if cart_id_str in session_cart:
                # Get current quantity
                item_data = session_cart[cart_id_str]
                current_quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                
                if current_quantity > 1:
                    # Decrease quantity
                    if isinstance(item_data, dict):
                        session_cart[cart_id_str]['quantity'] = current_quantity - 1
                    else:
                        session_cart[cart_id_str] = {'quantity': current_quantity - 1}
                    
                    request.session['cart'] = session_cart
                    request.session.modified = True
                    
                    # Get product and calculate totals
                    product = Product.objects.get(id=cart_id)
                    new_quantity = session_cart[cart_id_str]['quantity'] if isinstance(session_cart[cart_id_str], dict) else session_cart[cart_id_str]
                    item_total = product.price * new_quantity
                    
                    # Calculate updated totals
                    total_items = 0
                    total_price = 0
                    for product_id, item_data in session_cart.items():
                        try:
                            p = Product.objects.get(id=product_id)
                            quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                            total_items += quantity
                            total_price += p.price * quantity
                        except Product.DoesNotExist:
                            continue
                    
                    return JsonResponse({
                        'status': 'decreased',
                        'message': 'Miqdor kamaytirildi',
                        'item_quantity': new_quantity,
                        'item_total': float(item_total),
                        'cart_total_items': total_items,
                        'cart_total_price': float(total_price)
                    }, safe=False)
                else:
                    # Miqdor 1 dan kam bo'lsa o'chirish
                    product = Product.objects.get(id=cart_id)
                    product_name = product.name
                    
                    del session_cart[cart_id_str]
                    request.session['cart'] = session_cart
                    request.session.modified = True
                    
                    # Calculate updated totals
                    total_items = 0
                    total_price = 0
                    for product_id, item_data in session_cart.items():
                        try:
                            p = Product.objects.get(id=product_id)
                            quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                            total_items += quantity
                            total_price += p.price * quantity
                        except Product.DoesNotExist:
                            continue
                    
                    return JsonResponse({
                        'status': 'removed',
                        'message': f"'{product_name}' mahsuloti cartdan o'chirildi",
                        'cart_total_items': total_items,
                        'cart_total_price': float(total_price)
                    }, safe=False)
            else:
                return JsonResponse({'status': 'error', 'message': 'Mahsulot topilmadi'}, safe=False)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)

def clear_cart_api(request):
    """Barcha cartni tozalash API"""
    try:
        if request.user.is_authenticated:
            # Authenticated user - database cart
            cart_items = Cart.objects.filter(user=request.user)
            items_count = cart_items.count()
            
            if items_count > 0:
                cart_items.delete()
                return JsonResponse({
                    'status': 'cleared',
                    'message': f'Barcha mahsulotlar ({items_count} ta) cartdan o\'chirildi!',
                    'cart_total_items': 0,
                    'cart_total_price': 0.0
                }, safe=False)
            else:
                return JsonResponse({
                    'status': 'empty',
                    'message': 'Cart allaqachon bo\'sh',
                    'cart_total_items': 0,
                    'cart_total_price': 0.0
                }, safe=False)
        else:
            # Anonymous user - session-based cart
            session_cart = request.session.get('cart', {})
            items_count = len(session_cart)
            
            if items_count > 0:
                request.session['cart'] = {}
                request.session.modified = True
                
                return JsonResponse({
                    'status': 'cleared',
                    'message': f'Barcha mahsulotlar ({items_count} ta) cartdan o\'chirildi!',
                    'cart_total_items': 0,
                    'cart_total_price': 0.0
                }, safe=False)
            else:
                return JsonResponse({
                    'status': 'empty',
                    'message': 'Cart allaqachon bo\'sh',
                    'cart_total_items': 0,
                    'cart_total_price': 0.0
                }, safe=False)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)