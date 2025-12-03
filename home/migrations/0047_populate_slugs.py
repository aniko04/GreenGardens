# Generated manually to populate slugs for existing records

from django.db import migrations
from django.utils.text import slugify
import re


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


def populate_service_category_slugs(apps, schema_editor):
    ServiceCategory = apps.get_model('home', 'ServiceCategory')
    for category in ServiceCategory.objects.all():
        if not category.slug:
            base_slug = uzbek_slugify(category.name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            existing = ServiceCategory.objects.filter(slug=slug).exclude(id=category.id)
            while existing.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                existing = ServiceCategory.objects.filter(slug=slug).exclude(id=category.id)
            category.slug = slug
            category.save()


def populate_service_slugs(apps, schema_editor):
    OurService = apps.get_model('home', 'OurService')
    for service in OurService.objects.all():
        if not service.slug:
            base_slug = uzbek_slugify(service.title)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            existing = OurService.objects.filter(slug=slug).exclude(id=service.id)
            while existing.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                existing = OurService.objects.filter(slug=slug).exclude(id=service.id)
            service.slug = slug
            service.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_add_slug_fields'),
    ]

    operations = [
        migrations.RunPython(populate_service_category_slugs, migrations.RunPython.noop),
        migrations.RunPython(populate_service_slugs, migrations.RunPython.noop),
    ]

