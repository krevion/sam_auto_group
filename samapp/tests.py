from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .admin import CarAdmin, CarImageInline
from .models import Car, CarImage


class CarDetailViewTests(TestCase):
    def test_car_detail_shows_full_details_and_extra_uploaded_images(self):
        car = Car.objects.create(
            make='Toyota',
            model='Land Cruiser',
            year=2023,
            price='9500000',
            mileage=24000,
            condition=Car.Condition.USED,
            body_type='SUV',
            description='A rugged SUV with a full service history and premium interior.',
            availability=Car.Availability.AVAILABLE,
            featured=True,
        )
        car.image.save(
            'main.jpg',
            SimpleUploadedFile('main.jpg', b'fake-image-data', content_type='image/jpeg'),
            save=False,
        )
        CarImage.objects.create(car=car, image=SimpleUploadedFile('front.jpg', b'front', content_type='image/jpeg'))
        CarImage.objects.create(car=car, image=SimpleUploadedFile('rear.jpg', b'rear', content_type='image/jpeg'))

        response = self.client.get(reverse('samapp:car_detail', args=[car.pk]), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Toyota')
        self.assertContains(response, 'Land Cruiser')
        self.assertContains(response, 'A rugged SUV with a full service history and premium interior.')
        self.assertContains(response, '24,000')
        self.assertContains(response, '/media/cars/gallery/')
        self.assertContains(response, 'image 1')
        self.assertContains(response, 'image 2')


class CarAdminInventoryTests(TestCase):
    def test_car_admin_supports_gallery_images_and_price_updates(self):
        self.assertIn(CarImageInline, CarAdmin.inlines)
        self.assertIn('price', CarAdmin.list_editable)
        self.assertIn('availability', CarAdmin.list_editable)
        self.assertTrue(hasattr(CarAdmin, 'fieldsets'))
        self.assertIn('description', str(CarAdmin.fieldsets))
