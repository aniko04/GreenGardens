"""
Tarjima qilingan JSON faylni bazaga import qiluvchi management command.

Ishlatish:
    python manage.py import_translations translations_export.json

JSON fayl formati:
[
    {
        "id": 1,
        "model": "MainInfo",
        "pk": 1,
        "field": "description",
        "uz": "O'zbek matni",
        "ru": "Русский текст",
        "en": "English text"
    },
    ...
]
"""

import json
from django.core.management.base import BaseCommand
from django.apps import apps
from modeltranslation.utils import build_localized_fieldname


class Command(BaseCommand):
    help = "Tarjima qilingan JSON faylni bazaga import qiladi"

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=str,
            help="Import qilinadigan JSON fayl yo'li",
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="O'zgarishlarni saqlamay, faqat ko'rsatish",
        )

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']

        self.stdout.write(self.style.WARNING(f"\n{'='*60}"))
        self.stdout.write(self.style.WARNING("TARJIMALARNI IMPORT QILISH"))
        self.stdout.write(self.style.WARNING(f"{'='*60}"))
        self.stdout.write(f"Fayl: {file_path}")
        self.stdout.write(f"Dry-run: {dry_run}\n")

        # JSON faylni o'qish
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fayl topilmadi: {file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON xatosi: {e}"))
            return

        self.stdout.write(f"Jami yozuvlar: {len(data)}\n")

        updated_count = 0
        skipped_count = 0
        error_count = 0

        for item in data:
            model_name = item.get('model')
            pk = item.get('pk')
            field_name = item.get('field')
            ru_text = item.get('ru', '').strip()
            en_text = item.get('en', '').strip()

            # Agar tarjima bo'sh bo'lsa, skip
            if not ru_text and not en_text:
                skipped_count += 1
                continue

            try:
                # Modelni olish
                model = apps.get_model('home', model_name)
                obj = model.objects.get(pk=pk)

                changed = False

                # Rus tilini yangilash
                if ru_text:
                    ru_field = build_localized_fieldname(field_name, 'ru')
                    setattr(obj, ru_field, ru_text)
                    changed = True
                    self.stdout.write(f"  [{model_name}:{pk}] {field_name}_ru = {ru_text[:50]}...")

                # Ingliz tilini yangilash
                if en_text:
                    en_field = build_localized_fieldname(field_name, 'en')
                    setattr(obj, en_field, en_text)
                    changed = True
                    self.stdout.write(f"  [{model_name}:{pk}] {field_name}_en = {en_text[:50]}...")

                if changed:
                    if not dry_run:
                        obj.save()
                    updated_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Xato [{model_name}:{pk}]: {str(e)[:50]}"))
                error_count += 1

        # Yakuniy statistika
        self.stdout.write(self.style.HTTP_INFO(f"\n{'='*60}"))
        self.stdout.write(self.style.HTTP_INFO("YAKUNIY STATISTIKA"))
        self.stdout.write(self.style.HTTP_INFO(f"{'='*60}"))
        self.stdout.write(f"Yangilangan: {updated_count}")
        self.stdout.write(f"O'tkazib yuborilgan (bo'sh tarjima): {skipped_count}")
        self.stdout.write(f"Xatolar: {error_count}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY-RUN] O'zgarishlar saqlanmadi!"))
        else:
            self.stdout.write(self.style.SUCCESS("\nBarcha tarjimalar saqlandi!"))
