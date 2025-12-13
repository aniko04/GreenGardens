"""
Image utility functions for WebP conversion and optimization.

This module provides helper functions for converting images to WebP format,
optimizing quality settings, and validating image files.
"""

import os
import logging
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)


def should_convert_to_webp(filename):
    """
    Check if a file should be converted to WebP format.

    Args:
        filename (str): The name of the file to check

    Returns:
        bool: True if the file should be converted, False otherwise
    """
    if not filename:
        return False

    # Get file extension
    ext = os.path.splitext(filename)[1].lower()

    # Convert these formats to WebP
    convertible_formats = ['.jpg', '.jpeg', '.png', '.gif']

    # Don't convert these formats
    skip_formats = ['.webp', '.svg', '.ico', '.bmp']

    if ext in skip_formats:
        return False

    return ext in convertible_formats


def generate_webp_filename(original_filename):
    """
    Generate a WebP filename from the original filename.

    Args:
        original_filename (str): The original filename

    Returns:
        str: Filename with .webp extension
    """
    if not original_filename:
        return 'image.webp'

    # Get the base name without extension
    base_name = os.path.splitext(original_filename)[0]

    # Return with .webp extension
    return f"{base_name}.webp"


def get_optimal_quality(image_format, has_transparency=False):
    """
    Determine the optimal WebP quality based on the source image format.

    Args:
        image_format (str): The source image format (JPEG, PNG, etc.)
        has_transparency (bool): Whether the image has an alpha channel

    Returns:
        int: Optimal quality value (1-100)
    """
    # For images with transparency, use higher quality to preserve detail
    if has_transparency:
        return 95

    # JPEG images can use slightly lower quality
    if image_format in ['JPEG', 'JPG']:
        return 85

    # PNG images without transparency
    if image_format == 'PNG':
        return 85

    # Default quality for other formats
    return 85


def validate_image(file_obj):
    """
    Validate that a file is a valid image.

    Args:
        file_obj: File object to validate

    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        # Reset file pointer
        file_obj.seek(0)

        # Try to open and verify the image with Pillow
        img = Image.open(file_obj)
        img.verify()

        # Check if format is supported
        if img.format not in ['JPEG', 'PNG', 'GIF', 'BMP']:
            file_obj.seek(0)
            return False

        # Reset file pointer
        file_obj.seek(0)

        return True

    except Exception as e:
        logger.warning(f"Image validation failed: {str(e)}")
        file_obj.seek(0)
        return False


def convert_to_webp(image_file, quality=None):
    """
    Convert an image file to WebP format.

    Args:
        image_file: File object or path to the image
        quality (int, optional): WebP quality (1-100). If None, auto-detected.

    Returns:
        BytesIO: WebP image as BytesIO object, or None if conversion fails
    """
    try:
        # Open the image
        img = Image.open(image_file)

        # Store original format for quality determination
        original_format = img.format

        # Handle different image modes
        # Check if image has transparency
        has_transparency = False

        if img.mode in ('RGBA', 'LA', 'P'):
            has_transparency = True
            # Convert palette images to RGBA to preserve transparency
            if img.mode == 'P':
                # Check if palette has transparency
                if 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
                    has_transparency = False
        elif img.mode == 'CMYK':
            # Convert CMYK to RGB (WebP doesn't support CMYK)
            img = img.convert('RGB')
        elif img.mode not in ('RGB', 'RGBA'):
            # Convert other modes to RGB
            img = img.convert('RGB')

        # Determine optimal quality if not specified
        if quality is None:
            quality = get_optimal_quality(original_format, has_transparency)

        # Ensure quality is within valid range
        quality = max(1, min(100, quality))

        # Create BytesIO object to store the WebP image
        webp_io = BytesIO()

        # Save as WebP
        save_kwargs = {
            'format': 'WebP',
            'quality': quality,
            'method': 6,  # Higher quality compression method
        }

        # For images with transparency, use lossless for alpha channel
        if has_transparency:
            save_kwargs['lossless'] = False  # Still use lossy but preserve alpha

        img.save(webp_io, **save_kwargs)

        # Reset pointer to beginning
        webp_io.seek(0)

        # Log conversion info
        logger.info(
            f"Converted image to WebP: format={original_format}, "
            f"mode={img.mode}, quality={quality}, "
            f"size={img.size}, has_transparency={has_transparency}"
        )

        return webp_io

    except Exception as e:
        logger.error(f"Failed to convert image to WebP: {str(e)}", exc_info=True)
        return None


def resize_if_needed(img, max_width=4096, max_height=4096):
    """
    Resize image if it exceeds maximum dimensions.

    Args:
        img (PIL.Image): Image to resize
        max_width (int): Maximum width in pixels
        max_height (int): Maximum height in pixels

    Returns:
        PIL.Image: Resized image (or original if no resize needed)
    """
    if img.width > max_width or img.height > max_height:
        logger.info(
            f"Resizing image from {img.size} to fit within "
            f"{max_width}x{max_height}"
        )
        img.thumbnail((max_width, max_height), Image.LANCZOS)

    return img


def get_image_info(file_obj):
    """
    Get information about an image file.

    Args:
        file_obj: File object to analyze

    Returns:
        dict: Image information (format, size, mode, etc.) or None if invalid
    """
    try:
        file_obj.seek(0)
        img = Image.open(file_obj)

        info = {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
            'has_transparency': img.mode in ('RGBA', 'LA', 'P') and 'transparency' in img.info,
        }

        file_obj.seek(0)
        return info

    except Exception as e:
        logger.warning(f"Failed to get image info: {str(e)}")
        file_obj.seek(0)
        return None
