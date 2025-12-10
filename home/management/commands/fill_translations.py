"""
Bazadagi barcha tarjima maydonlarini to'ldiruvchi management command.

Ishlatish:
    python manage.py fill_translations

Bu script mavjud ma'lumotlarni (odatda uz tilida) boshqa til maydonlariga ko'chiradi.
Agar maydon bo'sh bo'lsa, default tildagi qiymatni ko'chiradi.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname


class Command(BaseCommand):
    help = "Bazadagi barcha tarjima maydonlarini to'ldiradi (bo'sh maydonlarni default tildan ko'chiradi)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help="Mavjud qiymatlarni ham qayta yozish (default: faqat bo'sh maydonlarni to'ldiradi)",
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="O'zgarishlarni saqlamay, faqat ko'rsatish",
        )

    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']

        # Tillar ro'yxati
        languages = [lang[0] for lang in settings.LANGUAGES]
        default_lang = settings.MODELTRANSLATION_DEFAULT_LANGUAGE if hasattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE') else settings.LANGUAGE_CODE

        self.stdout.write(self.style.WARNING(f"\nDefault til: {default_lang}"))
        self.stdout.write(self.style.WARNING(f"Tillar: {languages}"))
        self.stdout.write(self.style.WARNING(f"Force rejim: {force}"))
        self.stdout.write(self.style.WARNING(f"Dry-run rejim: {dry_run}\n"))

        # Ro'yxatdan o'tgan modellarni olish
        registered_models = translator.get_registered_models()

        total_updated = 0
        total_fields = 0

        for model in registered_models:
            model_name = model.__name__
            self.stdout.write(self.style.HTTP_INFO(f"\n{'='*50}"))
            self.stdout.write(self.style.HTTP_INFO(f"Model: {model_name}"))
            self.stdout.write(self.style.HTTP_INFO(f"{'='*50}"))

            # Model uchun tarjima options olish
            opts = translator.get_options_for_model(model)
            # opts.fields tuple yoki dict bo'lishi mumkin
            if isinstance(opts.fields, dict):
                trans_fields = list(opts.fields.keys())
            else:
                trans_fields = list(opts.fields)

            if not trans_fields:
                self.stdout.write(self.style.WARNING(f"  Tarjima maydonlari yo'q"))
                continue

            self.stdout.write(f"  Tarjima maydonlari: {list(trans_fields)}")

            # Barcha obyektlarni olish
            objects = model.objects.all()
            obj_count = objects.count()

            if obj_count == 0:
                self.stdout.write(self.style.WARNING(f"  Obyektlar yo'q"))
                continue

            self.stdout.write(f"  Obyektlar soni: {obj_count}")

            model_updated = 0

            for obj in objects:
                obj_changed = False
                changes = []

                for field_name in trans_fields:
                    # Default tildagi qiymatni olish
                    default_field = build_localized_fieldname(field_name, default_lang)
                    default_value = getattr(obj, default_field, None)

                    # Agar default qiymat bo'sh bo'lsa, oddiy maydondan olish
                    if not default_value:
                        default_value = getattr(obj, field_name, None)

                    if not default_value:
                        continue

                    # Boshqa tillar uchun maydonlarni to'ldirish
                    for lang in languages:
                        if lang == default_lang:
                            continue

                        localized_field = build_localized_fieldname(field_name, lang)
                        current_value = getattr(obj, localized_field, None)

                        # Agar force yoki maydon bo'sh bo'lsa
                        if force or not current_value:
                            if current_value != default_value:
                                setattr(obj, localized_field, default_value)
                                obj_changed = True
                                total_fields += 1

                                # Qisqartirilgan qiymat (50 belgigacha)
                                short_val = str(default_value)[:50]
                                if len(str(default_value)) > 50:
                                    short_val += "..."
                                changes.append(f"    {localized_field}: '{short_val}'")

                if obj_changed:
                    model_updated += 1
                    if changes:
                        self.stdout.write(f"\n  [{obj.pk}] {str(obj)[:30]}:")
                        for change in changes:
                            self.stdout.write(self.style.SUCCESS(change))

                    if not dry_run:
                        obj.save()

            if model_updated > 0:
                self.stdout.write(self.style.SUCCESS(f"\n  Yangilangan obyektlar: {model_updated}"))
                total_updated += model_updated
            else:
                self.stdout.write(self.style.WARNING(f"\n  Yangilanish kerak emas"))

        # Yakuniy statistika
        self.stdout.write(self.style.HTTP_INFO(f"\n{'='*50}"))
        self.stdout.write(self.style.HTTP_INFO("YAKUNIY STATISTIKA"))
        self.stdout.write(self.style.HTTP_INFO(f"{'='*50}"))
        self.stdout.write(f"Jami yangilangan obyektlar: {total_updated}")
        self.stdout.write(f"Jami to'ldirilgan maydonlar: {total_fields}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY-RUN] O'zgarishlar saqlanmadi!"))
            self.stdout.write(self.style.WARNING("Haqiqiy o'zgartirish uchun --dry-run ni olib tashlang"))
        else:
            self.stdout.write(self.style.SUCCESS("\nBarcha o'zgarishlar saqlandi!"))
