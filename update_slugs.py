#!/usr/bin/env python
"""
Bu script mavjud ServiceCategory va OurService obyektlarining sluglarini yangilaydi.
Migration bajarilgandan keyin ishga tushiring.
"""

import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import ServiceCategory, OurService
import re
from django.utils.text import slugify


def uzbek_slugify(text):
    """O'zbek harflarini qo'llab-quvvatlovchi slugify funksiyasi"""
    if not text:
        return ''
    
    # O'zbek lotin harflarini almashtirish (o' -> o, g' -> g)
    text = text.replace("o'", "o").replace("O'", "o")
    text = text.replace("g'", "g").replace("G'", "g")
    text = text.replace("'", "")  # Qolgan apostroflarni olib tashlash
    
    # Kirill harflarini transliteratsiya qilish
    uzbek_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'ў': 'o', 'қ': 'q', 'ғ': 'g', 'ҳ': 'h',
    }
    
    # Matnni kichik harflarga o'tkazish
    text = text.lower()
    
    # Kirill harflarini transliteratsiya qilish
    for cyrillic, latin in uzbek_map.items():
        text = text.replace(cyrillic, latin)
    
    # Standart slugify qo'llash
    slug = slugify(text, allow_unicode=False)
    
    # Agar slug bo'sh bo'lsa, lotin harflar va raqamlarni saqlab qolish
    if not slug or slug.strip() == '':
        slug = re.sub(r'[^a-z0-9\s-]', '', text)
        slug = re.sub(r'[\s-]+', '-', slug)
        slug = slug.strip('-').lower()
    
    return slug


def update_slugs():
    """Barcha kategoriya va servislarning sluglarini yangilaydi"""
    print("ServiceCategory sluglarini yangilash...")
    categories = ServiceCategory.objects.all()
    for category in categories:
        old_slug = category.slug
        base_slug = uzbek_slugify(category.name)
        slug = base_slug
        counter = 1
        
        # Uniqueness tekshirish
        while ServiceCategory.objects.filter(slug=slug).exclude(id=category.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        category.slug = slug
        category.save()
        print(f"  {category.name}: {old_slug} -> {slug}")
    
    print("\nOurService sluglarini yangilash...")
    services = OurService.objects.all()
    for service in services:
        old_slug = service.slug
        base_slug = uzbek_slugify(service.title)
        slug = base_slug
        counter = 1
        
        # Uniqueness tekshirish
        while OurService.objects.filter(slug=slug).exclude(id=service.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        service.slug = slug
        service.save()
        print(f"  {service.title}: {old_slug} -> {slug}")
    
    print("\nBarcha sluglar yangilandi!")


if __name__ == '__main__':
    update_slugs()

