"""
Custom storage backend for automatic WebP conversion.

This storage backend automatically converts uploaded images to WebP format
to improve site performance and reduce bandwidth usage.
"""

import os
import logging
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings

from .utils import (
    should_convert_to_webp,
    generate_webp_filename,
    convert_to_webp,
    validate_image,
    get_image_info
)

logger = logging.getLogger(__name__)


class WebPStorage(FileSystemStorage):
    """
    Custom storage backend that automatically converts images to WebP format.

    This storage extends Django's FileSystemStorage to intercept image uploads
    and convert them to WebP format for better performance.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webp_enabled = getattr(settings, 'WEBP_ENABLED', True)
        self.webp_quality = getattr(settings, 'WEBP_QUALITY', 85)
        self.webp_quality_png = getattr(settings, 'WEBP_QUALITY_PNG', 95)
        self.preserve_originals = getattr(settings, 'WEBP_PRESERVE_ORIGINALS', False)

    def _save(self, name, content):
        """
        Override the save method to convert images to WebP before saving.

        Args:
            name (str): The filename to save
            content: File content

        Returns:
            str: The saved filename (possibly with .webp extension)
        """
        # Check if WebP conversion is enabled
        if not self.webp_enabled:
            return super()._save(name, content)

        # Check if this file should be converted to WebP
        if not should_convert_to_webp(name):
            logger.debug(f"Skipping WebP conversion for: {name}")
            return super()._save(name, content)

        # Validate that it's a real image
        if not validate_image(content):
            logger.warning(f"Invalid image file, saving without conversion: {name}")
            return super()._save(name, content)

        # Get image information
        image_info = get_image_info(content)
        if not image_info:
            logger.warning(f"Could not get image info, saving without conversion: {name}")
            return super()._save(name, content)

        # Determine quality based on image format
        if image_info.get('has_transparency'):
            quality = self.webp_quality_png
        else:
            quality = self.webp_quality

        # Convert to WebP
        webp_content = convert_to_webp(content, quality=quality)

        if webp_content is None:
            logger.error(f"WebP conversion failed for: {name}, saving original")
            return super()._save(name, content)

        # Generate WebP filename
        webp_name = generate_webp_filename(name)

        # Get original file size
        content.seek(0, os.SEEK_END)
        original_size = content.tell()
        content.seek(0)

        # Get WebP file size
        webp_content.seek(0, os.SEEK_END)
        webp_size = webp_content.tell()
        webp_content.seek(0)

        # Calculate savings
        savings_percent = ((original_size - webp_size) / original_size * 100) if original_size > 0 else 0

        logger.info(
            f"WebP conversion successful: {name} -> {webp_name} | "
            f"Original: {original_size / 1024:.2f}KB, "
            f"WebP: {webp_size / 1024:.2f}KB, "
            f"Savings: {savings_percent:.1f}%"
        )

        # Save the original file if preserve_originals is enabled
        if self.preserve_originals:
            original_path = os.path.join('originals', name)
            super()._save(original_path, content)
            logger.debug(f"Original file preserved at: {original_path}")

        # Save the WebP file directly to avoid ContentFile format issues
        # Get the full path where the file will be saved
        full_path = self.path(self.get_available_name(webp_name))

        # Ensure the directory exists
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Write WebP content directly to file
        webp_content.seek(0)
        with open(full_path, 'wb') as f:
            f.write(webp_content.read())

        # Return just the name (not full path)
        return os.path.relpath(full_path, self.location)

    def get_available_name(self, name, max_length=None):
        """
        Override to handle WebP filenames when checking for existing files.

        Args:
            name (str): The filename to check
            max_length (int, optional): Maximum length for the filename

        Returns:
            str: Available filename
        """
        # Don't modify name here - let _save() handle WebP conversion
        # This prevents double-conversion issues
        return super().get_available_name(name, max_length)

    def delete(self, name):
        """
        Override delete to also remove preserved originals if they exist.

        Args:
            name (str): The filename to delete
        """
        # Delete the main file
        super().delete(name)

        # If preserve_originals was enabled, try to delete the original too
        if self.preserve_originals:
            # Try to find corresponding original file
            base_name = os.path.splitext(os.path.basename(name))[0]

            # Check for common image extensions
            for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                original_path = os.path.join('originals', f"{base_name}{ext}")
                if self.exists(original_path):
                    try:
                        super().delete(original_path)
                        logger.debug(f"Deleted preserved original: {original_path}")
                    except Exception as e:
                        logger.warning(f"Failed to delete original {original_path}: {e}")
