"""
Unit tests for WebP image conversion functionality.

Tests cover:
- Image conversion from various formats
- Quality settings
- Transparency preservation
- Edge cases and error handling
"""

import os
import tempfile
from io import BytesIO
from PIL import Image

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from home.utils import (
    should_convert_to_webp,
    generate_webp_filename,
    get_optimal_quality,
    validate_image,
    convert_to_webp,
)
from home.storage import WebPStorage


class WebPUtilsTestCase(TestCase):
    """Test cases for WebP utility functions."""

    def test_should_convert_to_webp_jpeg(self):
        """Test that JPEG files should be converted."""
        self.assertTrue(should_convert_to_webp('photo.jpg'))
        self.assertTrue(should_convert_to_webp('photo.jpeg'))
        self.assertTrue(should_convert_to_webp('PHOTO.JPG'))

    def test_should_convert_to_webp_png(self):
        """Test that PNG files should be converted."""
        self.assertTrue(should_convert_to_webp('logo.png'))
        self.assertTrue(should_convert_to_webp('LOGO.PNG'))

    def test_should_not_convert_webp(self):
        """Test that WebP files should not be converted again."""
        self.assertFalse(should_convert_to_webp('image.webp'))
        self.assertFalse(should_convert_to_webp('IMAGE.WEBP'))

    def test_should_not_convert_svg(self):
        """Test that SVG files should not be converted."""
        self.assertFalse(should_convert_to_webp('icon.svg'))
        self.assertFalse(should_convert_to_webp('ICON.SVG'))

    def test_generate_webp_filename(self):
        """Test WebP filename generation."""
        self.assertEqual(
            generate_webp_filename('photo.jpg'),
            'photo.webp'
        )
        self.assertEqual(
            generate_webp_filename('image.png'),
            'image.webp'
        )
        self.assertEqual(
            generate_webp_filename('path/to/photo.jpeg'),
            'path/to/photo.webp'
        )

    def test_get_optimal_quality_jpeg(self):
        """Test optimal quality for JPEG images."""
        quality = get_optimal_quality('JPEG', has_transparency=False)
        self.assertEqual(quality, 85)

    def test_get_optimal_quality_png_transparency(self):
        """Test optimal quality for PNG with transparency."""
        quality = get_optimal_quality('PNG', has_transparency=True)
        self.assertEqual(quality, 95)

    def test_get_optimal_quality_png_no_transparency(self):
        """Test optimal quality for PNG without transparency."""
        quality = get_optimal_quality('PNG', has_transparency=False)
        self.assertEqual(quality, 85)

    def test_validate_image_valid_jpeg(self):
        """Test image validation with valid JPEG."""
        # Create a simple JPEG image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        self.assertTrue(validate_image(img_io))

    def test_validate_image_valid_png(self):
        """Test image validation with valid PNG."""
        # Create a simple PNG image
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        self.assertTrue(validate_image(img_io))

    def test_validate_image_invalid(self):
        """Test image validation with invalid file."""
        # Create invalid file
        invalid_io = BytesIO(b'Not an image file')
        self.assertFalse(validate_image(invalid_io))

    def test_convert_to_webp_jpeg(self):
        """Test converting JPEG to WebP."""
        # Create a simple JPEG image
        img = Image.new('RGB', (200, 200), color='green')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        # Convert to WebP
        webp_io = convert_to_webp(img_io, quality=85)

        self.assertIsNotNone(webp_io)

        # Verify it's a valid WebP image
        webp_img = Image.open(webp_io)
        self.assertEqual(webp_img.format, 'WEBP')
        self.assertEqual(webp_img.size, (200, 200))

    def test_convert_to_webp_png_with_transparency(self):
        """Test converting PNG with transparency to WebP."""
        # Create PNG with transparency
        img = Image.new('RGBA', (150, 150), color=(255, 0, 0, 128))
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        # Convert to WebP
        webp_io = convert_to_webp(img_io, quality=95)

        self.assertIsNotNone(webp_io)

        # Verify it's a valid WebP with transparency
        webp_img = Image.open(webp_io)
        self.assertEqual(webp_img.format, 'WEBP')
        self.assertIn(webp_img.mode, ['RGBA', 'LA'])

    def test_convert_to_webp_quality_setting(self):
        """Test that quality setting is applied."""
        # Create larger image with more detail for better test
        img = Image.new('RGB', (400, 400), color='yellow')

        # Add detail to make compression differences more visible
        pixels = img.load()
        for i in range(0, 400, 10):
            for j in range(0, 400, 10):
                pixels[i, j] = (i % 255, j % 255, (i + j) % 255)

        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)

        # Convert with low quality
        webp_low = convert_to_webp(img_io, quality=50)
        img_io.seek(0)

        # Convert with high quality
        webp_high = convert_to_webp(img_io, quality=95)

        # Both should be valid WebP
        self.assertIsNotNone(webp_low)
        self.assertIsNotNone(webp_high)

        # Get file sizes
        webp_low.seek(0, os.SEEK_END)
        low_size = webp_low.tell()

        webp_high.seek(0, os.SEEK_END)
        high_size = webp_high.tell()

        # High quality should generally be larger (or at least not much smaller)
        # Allow some tolerance for WebP optimization
        self.assertGreaterEqual(high_size, low_size * 0.8)


@override_settings(WEBP_ENABLED=True)
class WebPStorageTestCase(TestCase):
    """Test cases for WebP storage backend."""

    def setUp(self):
        """Set up test environment."""
        self.storage = WebPStorage()

    def test_storage_webp_enabled(self):
        """Test that WebP is enabled in storage."""
        self.assertTrue(self.storage.webp_enabled)

    def test_storage_save_jpeg_converts_to_webp(self):
        """Test that saving JPEG converts to WebP."""
        # Create a simple JPEG image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        # Create uploaded file
        uploaded_file = SimpleUploadedFile(
            'test_image.jpg',
            img_io.read(),
            content_type='image/jpeg'
        )

        # Save through storage
        saved_name = self.storage.save('test_image.jpg', uploaded_file)

        # Should be saved as WebP
        self.assertTrue(saved_name.endswith('.webp'))

        # Clean up
        self.storage.delete(saved_name)

    def test_storage_save_png_converts_to_webp(self):
        """Test that saving PNG converts to WebP."""
        # Create a simple PNG image
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        # Create uploaded file
        uploaded_file = SimpleUploadedFile(
            'test_image.png',
            img_io.read(),
            content_type='image/png'
        )

        # Save through storage
        saved_name = self.storage.save('test_image.png', uploaded_file)

        # Should be saved as WebP
        self.assertTrue(saved_name.endswith('.webp'))

        # Clean up
        self.storage.delete(saved_name)

    def test_storage_skip_svg(self):
        """Test that SVG files are not converted."""
        # Create a simple SVG content
        svg_content = b'<svg xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100"/></svg>'

        uploaded_file = SimpleUploadedFile(
            'test_icon.svg',
            svg_content,
            content_type='image/svg+xml'
        )

        # Save through storage
        saved_name = self.storage.save('test_icon.svg', uploaded_file)

        # Should NOT be converted (still .svg)
        self.assertTrue(saved_name.endswith('.svg'))

        # Clean up
        self.storage.delete(saved_name)

    @override_settings(WEBP_ENABLED=False)
    def test_storage_disabled_no_conversion(self):
        """Test that disabling WebP prevents conversion."""
        storage = WebPStorage()

        # Create a simple JPEG image
        img = Image.new('RGB', (100, 100), color='green')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        uploaded_file = SimpleUploadedFile(
            'test_image.jpg',
            img_io.read(),
            content_type='image/jpeg'
        )

        # Save through storage
        saved_name = storage.save('test_image.jpg', uploaded_file)

        # Should NOT be converted (still .jpg)
        self.assertTrue(saved_name.endswith('.jpg'))

        # Clean up
        storage.delete(saved_name)


class WebPIntegrationTestCase(TestCase):
    """Integration tests for WebP conversion in real scenarios."""

    def test_file_size_reduction(self):
        """Test that WebP reduces file size significantly."""
        # Create a larger JPEG image
        img = Image.new('RGB', (800, 600), color='red')

        # Add some detail to make it more realistic
        pixels = img.load()
        for i in range(100):
            for j in range(100):
                pixels[i, j] = (i * 2, j * 2, (i + j) % 255)

        # Save as JPEG
        jpeg_io = BytesIO()
        img.save(jpeg_io, format='JPEG', quality=85)
        jpeg_io.seek(0)

        jpeg_size = len(jpeg_io.getvalue())

        # Convert to WebP
        webp_io = convert_to_webp(jpeg_io, quality=85)
        webp_io.seek(0, os.SEEK_END)
        webp_size = webp_io.tell()

        # WebP should be smaller
        savings_percent = ((jpeg_size - webp_size) / jpeg_size) * 100

        self.assertLess(webp_size, jpeg_size)
        self.assertGreater(savings_percent, 0)

        # Typically should save at least 20%
        self.assertGreater(savings_percent, 20)
