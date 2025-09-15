import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Product, Category

class Command(BaseCommand):
    help = 'Load products from JSON'

    def handle(self, *args, **kwargs):
        with open('products.json', 'r') as file:
            data = json.load(file)
            for item in data:
                # --- Category ---
                base_slug = slugify(item['category'])
                slug = base_slug
                counter = 1
                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                category, _ = Category.objects.get_or_create(
                    name=item['category'],
                    defaults={'slug': slug}
                )

                # --- Product ---
                base_slug = slugify(item['name'])
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                product, created = Product.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'category': category,
                        'description': item.get('description', ''),
                        'price': item['price'],
                        'slug': slug
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added {product.name}"))
                else:
                    self.stdout.write(f"{product.name} already exists, skipped")
