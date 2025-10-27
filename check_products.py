import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import Product

# Check products
total_products = Product.objects.count()
print(f'Total products: {total_products}')

print('\nSample products:')
for product in Product.objects.all()[:5]:
    print(f'- {product.name} (${product.price})')