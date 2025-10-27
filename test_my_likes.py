#!/usr/bin/env python
"""
Simple test script to check if my_likes functionality works
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append('/Users/aniko/python/django/GreenGardens')
django.setup()

from django.contrib.auth.models import User
from home.models import Product, Like

def test_my_likes_functionality():
    print("Testing My Likes functionality...")
    
    # Check if we have products
    products_count = Product.objects.filter(is_active=True).count()
    print(f"Total active products: {products_count}")
    
    # Check if we have users
    users_count = User.objects.count()
    print(f"Total users: {users_count}")
    
    # Check likes
    likes_count = Like.objects.count()
    print(f"Total likes: {likes_count}")
    
    if likes_count > 0:
        # Show some liked products
        liked_products = Product.objects.filter(like__isnull=False).distinct()[:5]
        print(f"Products with likes: {liked_products.count()}")
        for product in liked_products:
            print(f"  - {product.name}")
    
    print("My Likes functionality test completed!")

if __name__ == '__main__':
    test_my_likes_functionality()