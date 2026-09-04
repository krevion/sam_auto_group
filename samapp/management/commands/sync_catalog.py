import re

from django.core.management.base import BaseCommand

from samapp.models import Car
from samapp.views import STATIC_CARS, STATIC_IMPORT_CARS


class Command(BaseCommand):
    help = 'Create or update editable database records from the built-in car catalog.'

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for item, is_import in [
            *[(car, False) for car in STATIC_CARS],
            *[(car, True) for car in STATIC_IMPORT_CARS],
        ]:
            year_match = re.search(r'\b(19|20)\d{2}\b', item['title'])
            year = int(year_match.group()) if year_match else 2024
            title = re.sub(r'^\d{4}\s+', '', item['title']).strip()
            parts = title.split(maxsplit=1)
            make = parts[0]
            model = parts[1] if len(parts) > 1 else make
            defaults = {
                'year': year,
                'price': item.get('price') or 0,
                'description': item['description'],
                'image_url': '/static/' + item['image'],
                'body_type': item.get('body_type', 'SUV'),
                'is_import': is_import,
                'availability': Car.Availability.AVAILABLE,
            }
            car, was_created = Car.objects.update_or_create(
                make=make,
                model=model,
                year=year,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Catalog synced: {created} created, {updated} updated. '
            'Edit cars at /admin/ and set Availability to Sold when needed.'
        ))
