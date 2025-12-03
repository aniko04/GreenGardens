#!/usr/bin/env python
"""
Bu script bazadagi sluglarni tekshiradi va 'klassik-uslub' ni qidiradi.
"""

import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import ServiceCategory, OurService


def debug_slug():
    """'klassik-uslub' slug'ini qidiradi"""
    search_slug = 'klassik-uslub'
    
    print("=" * 60)
    print(f"'{search_slug}' slug'ini qidirish:")
    print("=" * 60)
    
    # ServiceCategory'da qidirish
    print("\n1. ServiceCategory'da qidirish:")
    categories = ServiceCategory.objects.filter(slug__icontains='klassik')
    if categories.exists():
        for cat in categories:
            print(f"   ID: {cat.id}, Name: '{cat.name}', Slug: '{cat.slug}'")
    else:
        print("   Topilmadi")
    
    # OurService'da qidirish
    print("\n2. OurService'da qidirish:")
    services = OurService.objects.filter(slug__icontains='klassik')
    if services.exists():
        for svc in services:
            print(f"   ID: {svc.id}, Title: '{svc.title}', Slug: '{svc.slug}', Active: {svc.is_active}")
    else:
        print("   Topilmadi")
    
    # Barcha kategoriyalarni ko'rsatish
    print("\n" + "=" * 60)
    print("Barcha ServiceCategory'lar:")
    print("=" * 60)
    for cat in ServiceCategory.objects.all():
        print(f"ID: {cat.id}, Name: '{cat.name}', Slug: '{cat.slug}'")
    
    # Barcha servislarni ko'rsatish
    print("\n" + "=" * 60)
    print("Barcha OurService'lar (faol):")
    print("=" * 60)
    for svc in OurService.objects.filter(is_active=True):
        print(f"ID: {svc.id}, Title: '{svc.title}', Slug: '{svc.slug}'")
        if svc.category.exists():
            print(f"   Categories: {[c.name for c in svc.category.all()]}")


if __name__ == '__main__':
    debug_slug()

