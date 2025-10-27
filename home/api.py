from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Cart, Like, Product

def user_product_like_api(request, product_id):
    if request.user.is_authenticated:
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            result = Like.objects.filter(user=request.user, product=p).exists()
            return JsonResponse({'liked': result}, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'liked': False, 'error': 'Product not found'}, safe=False)
    return JsonResponse({'liked': False}, safe=False)

def user_like_add_api(request, product_id):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            like, created = Like.objects.get_or_create(user=request.user, product=p)
            if created:
                return JsonResponse({'status': 'liked'}, safe=False)
            else:
                like.delete()
                return JsonResponse({'status': 'unliked'}, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, safe=False)
    return JsonResponse({'status': 'unauthenticated'}, safe=False)

def cart_api(request, product_id):
    if request.user.is_authenticated:
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            result = Cart.objects.filter(user=request.user, product=p).exists()
            return JsonResponse({'added': result}, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'added': False, 'error': 'Product not found'}, safe=False)
    return JsonResponse({'added': 'false'}, safe=False)

def add_to_cart_api(request, product_id):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            p = Product.objects.get(id=product_id, is_active=True)
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=p)
            if created:
                return JsonResponse({'status': 'added', 'cart_item_id': cart_item.id}, safe=False)
            else:
                cart_item.delete()
                return JsonResponse({'status': 'removed'}, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, safe=False)
    return JsonResponse({'status': 'unauthenticated'}, safe=False)

def cart_count_api(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'cart_count': count}, safe=False)
    return JsonResponse({'cart_count': 0}, safe=False)

def likes_count_api(request):
    if request.user.is_authenticated:
        count = Like.objects.filter(user=request.user).count()
        return JsonResponse({'likes_count': count}, safe=False)
    return JsonResponse({'likes_count': 0}, safe=False)

# CART MANAGEMENT API'LAR

def remove_from_cart_api(request, cart_id):
    """Cart dan mahsulot o'chirish API"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, safe=False)
    
    try:
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
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, safe=False)
    
    try:
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
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)

def decrease_cart_quantity_api(request, cart_id):
    """Cart miqdorini kamaytirish API"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, safe=False)
    
    try:
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
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)

def clear_cart_api(request):
    """Barcha cartni tozalash API"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, safe=False)
    
    try:
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
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)