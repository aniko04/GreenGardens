"""
CKEditor storage integration for WebP conversion.

This module provides a custom storage backend for CKEditor uploads
that automatically converts images to WebP format.
"""

from .storage import WebPStorage


class CKEditorWebPStorage(WebPStorage):
    """
    Custom storage backend for CKEditor that converts images to WebP.

    This extends the WebPStorage class to ensure that images uploaded
    through CKEditor's rich text editor are also converted to WebP format.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_valid_name(self, name):
        """
        Override to ensure proper WebP filename handling for CKEditor uploads.

        Args:
            name (str): The original filename

        Returns:
            str: Valid filename for storage
        """
        # Let parent class handle the validation
        valid_name = super().get_valid_name(name)

        return valid_name
