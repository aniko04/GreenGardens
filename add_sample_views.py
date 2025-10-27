#!/usr/bin/env python
import os
import sys
import django
import random

# Django settings ni sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import Product

def add_sample_views():
    """Mavjud mahsulotlarga tasodifiy ko'rishlar soni qo'shish"""
    products = Product.objects.filter(is_active=True)
    
    for product in products:
        # 10 dan 500 gacha tasodifiy views qo'shish
        random_views = random.randint(10, 500)
        product.views = random_views
        product.save()
        print(f"'{product.name}' ga {random_views} views qo'shildi")
    
    print(f"\nJami {products.count()} ta mahsulotga views qo'shildi!")

if __name__ == "__main__":
    add_sample_views()