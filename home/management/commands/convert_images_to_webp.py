"""
Django management command to convert existing images to WebP format.

This command scans all models with ImageField, finds existing non-WebP images,
and converts them to WebP format to improve site performance.

Usage:
    python manage.py convert_images_to_webp --dry-run
    python manage.py convert_images_to_webp --delete-originals
    python manage.py convert_images_to_webp --keep-originals
"""

import os
import logging
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps
from django.db import models
from django.core.files import File

from home.utils import (
    should_convert_to_webp,
    convert_to_webp,
    generate_webp_filename,
    validate_image
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Convert existing images to WebP format for better performance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be converted without actually converting',
        )
        parser.add_argument(
            '--delete-originals',
            action='store_true',
            help='Delete original images after conversion',
        )
        parser.add_argument(
            '--keep-originals',
            action='store_true',
            help='Keep original images in /media/originals/',
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Only convert images for a specific model (e.g., "home.Product")',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of images to convert',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        delete_originals = options['delete_originals']
        keep_originals = options['keep_originals']
        specific_model = options.get('model')
        limit = options.get('limit')

        if delete_originals and keep_originals:
            raise CommandError('Cannot use both --delete-originals and --keep-originals')

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('WebP Image Conversion Tool'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        # Get all models with ImageField
        models_to_process = self.get_models_with_imagefields(specific_model)

        if not models_to_process:
            self.stdout.write(self.style.WARNING('No models with ImageField found'))
            return

        self.stdout.write(f'\nFound {len(models_to_process)} model(s) with ImageField:\n')
        for model_class in models_to_process:
            self.stdout.write(f'  - {model_class._meta.label}')

        # Process each model
        total_converted = 0
        total_failed = 0
        total_skipped = 0
        total_size_saved = 0

        for model_class in models_to_process:
            self.stdout.write(f'\n{"-" * 70}')
            self.stdout.write(f'Processing model: {model_class._meta.label}')
            self.stdout.write('-' * 70)

            # Get all image fields for this model
            image_fields = [
                field for field in model_class._meta.get_fields()
                if isinstance(field, models.ImageField)
            ]

            # Process each instance
            instances = model_class.objects.all()
            if limit and total_converted >= limit:
                break

            for instance in instances:
                if limit and total_converted >= limit:
                    break

                for field in image_fields:
                    image_file = getattr(instance, field.name)

                    if not image_file:
                        continue

                    # Check if already WebP
                    if image_file.name.lower().endswith('.webp'):
                        continue

                    # Check if should be converted
                    if not should_convert_to_webp(image_file.name):
                        total_skipped += 1
                        continue

                    # Get full path
                    full_path = image_file.path

                    if not os.path.exists(full_path):
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ File not found: {image_file.name}')
                        )
                        total_failed += 1
                        continue

                    # Convert the image
                    result = self.convert_image(
                        instance=instance,
                        field=field,
                        image_file=image_file,
                        full_path=full_path,
                        dry_run=dry_run,
                        delete_original=delete_originals,
                        keep_original=keep_originals
                    )

                    if result['success']:
                        total_converted += 1
                        total_size_saved += result.get('size_saved', 0)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ {image_file.name} -> {result["new_name"]} '
                                f'(saved {result["savings_percent"]:.1f}%)'
                            )
                        )
                    else:
                        total_failed += 1
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Failed: {image_file.name}')
                        )

        # Print summary
        self.stdout.write(f'\n{"=" * 70}')
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Total converted: {total_converted}')
        self.stdout.write(f'Total failed: {total_failed}')
        self.stdout.write(f'Total skipped: {total_skipped}')
        self.stdout.write(
            f'Total size saved: {total_size_saved / 1024 / 1024:.2f} MB'
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nDRY RUN - No actual changes were made')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✓ Conversion completed successfully!')
            )

    def get_models_with_imagefields(self, specific_model=None):
        """Get all models that have ImageField."""
        models_with_images = []

        if specific_model:
            # Get specific model
            try:
                app_label, model_name = specific_model.split('.')
                model_class = apps.get_model(app_label, model_name)
                models_with_images.append(model_class)
            except (ValueError, LookupError) as e:
                raise CommandError(f'Invalid model: {specific_model}. Error: {e}')
        else:
            # Get all models
            for model_class in apps.get_models():
                # Check if model has any ImageField
                has_image_field = any(
                    isinstance(field, models.ImageField)
                    for field in model_class._meta.get_fields()
                    if hasattr(field, 'upload_to')
                )

                if has_image_field:
                    models_with_images.append(model_class)

        return models_with_images

    def convert_image(self, instance, field, image_file, full_path,
                      dry_run=False, delete_original=False, keep_original=False):
        """Convert a single image to WebP."""
        result = {
            'success': False,
            'new_name': None,
            'size_saved': 0,
            'savings_percent': 0
        }

        try:
            # Get original file size
            original_size = os.path.getsize(full_path)

            if dry_run:
                # Just simulate
                result['success'] = True
                result['new_name'] = generate_webp_filename(image_file.name)
                result['savings_percent'] = 65  # Estimated
                return result

            # Open and validate the image
            with open(full_path, 'rb') as f:
                if not validate_image(f):
                    logger.warning(f'Invalid image: {full_path}')
                    return result

            # Convert to WebP
            with open(full_path, 'rb') as f:
                webp_content = convert_to_webp(f)

            if webp_content is None:
                logger.error(f'Conversion failed: {full_path}')
                return result

            # Generate WebP filename
            webp_filename = generate_webp_filename(os.path.basename(image_file.name))
            webp_path = os.path.join(os.path.dirname(full_path), webp_filename)

            # Get WebP size
            webp_content.seek(0, os.SEEK_END)
            webp_size = webp_content.tell()
            webp_content.seek(0)

            # Calculate savings
            size_saved = original_size - webp_size
            savings_percent = (size_saved / original_size * 100) if original_size > 0 else 0

            # Save WebP file
            with open(webp_path, 'wb') as f:
                f.write(webp_content.read())

            # Update database field
            new_name = os.path.join(os.path.dirname(image_file.name), webp_filename)
            setattr(instance, field.name, new_name)
            instance.save(update_fields=[field.name])

            # Handle original file
            if keep_original:
                # Move to originals folder
                originals_dir = os.path.join(settings.MEDIA_ROOT, 'originals')
                os.makedirs(originals_dir, exist_ok=True)

                original_backup = os.path.join(
                    originals_dir,
                    os.path.basename(image_file.name)
                )
                os.rename(full_path, original_backup)

            elif delete_original:
                # Delete original file
                os.remove(full_path)

            # If neither flag is set, keep original file in place
            # (user may want to manually review first)

            result['success'] = True
            result['new_name'] = new_name
            result['size_saved'] = size_saved
            result['savings_percent'] = savings_percent

        except Exception as e:
            logger.error(f'Error converting {full_path}: {e}', exc_info=True)

        return result
