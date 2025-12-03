#!/usr/bin/env python
"""
Bu script bazadagi sluglarni tekshiradi va muammolarni ko'rsatadi.
"""

import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import ServiceCategory, OurService


def check_slugs():
    """Barcha kategoriya va servislarning sluglarini tekshiradi"""
    print("=" * 60)
    print("ServiceCategory sluglarini tekshirish:")
    print("=" * 60)
    
    categories = ServiceCategory.objects.all()
    problems = []
    
    for category in categories:
        print(f"\nID: {category.id}")
        print(f"Name: {category.name}")
        print(f"Slug: '{category.slug}'")
        
        if not category.slug or category.slug.strip() == '':
            problems.append(f"ServiceCategory ID {category.id} ({category.name}): Slug bo'sh!")
            print("  ❌ MUAMMO: Slug bo'sh!")
        elif ' ' in category.slug:
            problems.append(f"ServiceCategory ID {category.id} ({category.name}): Slug'da bo'sh joy bor!")
            print("  ❌ MUAMMO: Slug'da bo'sh joy bor!")
        else:
            print("  ✅ Slug to'g'ri")
    
    print("\n" + "=" * 60)
    print("OurService sluglarini tekshirish:")
    print("=" * 60)
    
    services = OurService.objects.filter(is_active=True)
    
    for service in services:
        print(f"\nID: {service.id}")
        print(f"Title: {service.title}")
        print(f"Slug: '{service.slug}'")
        
        if not service.slug or service.slug.strip() == '':
            problems.append(f"OurService ID {service.id} ({service.title}): Slug bo'sh!")
            print("  ❌ MUAMMO: Slug bo'sh!")
        elif ' ' in service.slug:
            problems.append(f"OurService ID {service.id} ({service.title}): Slug'da bo'sh joy bor!")
            print("  ❌ MUAMMO: Slug'da bo'sh joy bor!")
        else:
            print("  ✅ Slug to'g'ri")
    
    print("\n" + "=" * 60)
    print("XULOSA:")
    print("=" * 60)
    
    if problems:
        print(f"\n❌ {len(problems)} ta muammo topildi:")
        for problem in problems:
            print(f"  - {problem}")
        print("\n💡 Yechim: python update_slugs.py skriptini ishga tushiring")
    else:
        print("\n✅ Barcha sluglar to'g'ri!")


if __name__ == '__main__':
    check_slugs()

