from django.core.management.base import BaseCommand
from faker import Faker
from decimal import Decimal
import random
from home.models import Product, ProductImage

class Command(BaseCommand):
    help = 'Seed the database with fake products'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=20, help='Number of products to create')

    def handle(self, *args, **options):
        fake = Faker()
        number = options['number']

        self.stdout.write(f'Creating {number} fake products...')

        # Plant/garden related product names and descriptions
        plant_names = [
            'Rose Bush', 'Tulip Bulbs', 'Lavender Plant', 'Sunflower Seeds', 'Tomato Seedlings',
            'Herb Garden Kit', 'Bamboo Plant', 'Succulent Collection', 'Oak Tree Sapling', 
            'Flower Bed Mix', 'Vegetable Seeds Pack', 'Orchid Plant', 'Cactus Garden',
            'Grass Seed', 'Climbing Ivy', 'Fruit Tree Bundle', 'Fern Collection',
            'Garden Tools Set', 'Watering Can', 'Plant Fertilizer'
        ]

        descriptions = [
            'Perfect for creating beautiful garden landscapes',
            'High-quality plants for your home garden',
            'Easy to grow and maintain plants',
            'Ideal for beginners and experienced gardeners',
            'Organic and pesticide-free plants',
            'Weather-resistant and durable plants',
            'Beautiful flowering plants for all seasons',
            'Low maintenance plants perfect for busy lifestyles',
            'Premium quality seeds and plants',
            'Professional grade gardening supplies'
        ]

        statuses = ['Available', 'Out of Stock', 'Coming Soon', 'Limited Stock']

        for i in range(number):
            # Create a product
            product = Product.objects.create(
                name=fake.random_element(plant_names) + f" - {fake.word().title()}",
                mini_description=fake.random_element(descriptions),
                price=Decimal(str(round(random.uniform(5.99, 299.99), 2))),
                old_price=Decimal(str(round(random.uniform(300.00, 499.99), 2))) if random.choice([True, False]) else None,
                quantity=random.randint(0, 100),
                description=fake.text(max_nb_chars=500),
                specifications=fake.text(max_nb_chars=300),
                status=fake.random_element(statuses),
                is_active=True,
                is_top=random.choice([True, False])
            )

            # Create some product images (optional)
            if random.choice([True, False]):
                for _ in range(random.randint(1, 3)):
                    product_image = ProductImage.objects.create()
                    product.images.add(product_image)

            self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {number} products!')
        )