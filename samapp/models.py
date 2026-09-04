from django.db import models


class Car(models.Model):
	class Condition(models.TextChoices):
		NEW = 'new', 'New'
		USED = 'used', 'Used'

	class Availability(models.TextChoices):
		AVAILABLE = 'available', 'Available'
		RESERVED = 'reserved', 'Reserved'
		SOLD = 'sold', 'Sold'

	make = models.CharField(max_length=80)
	model = models.CharField(max_length=80)
	year = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=12, decimal_places=2)
	mileage = models.PositiveIntegerField(default=0, help_text='Mileage in kilometres')
	condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.USED)
	body_type = models.CharField(max_length=40, blank=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='cars/', blank=True, null=True)
	image_url = models.URLField(blank=True)
	availability = models.CharField(max_length=12, choices=Availability.choices, default=Availability.AVAILABLE)
	featured = models.BooleanField(default=False)
	is_import = models.BooleanField(default=False, help_text='Show this vehicle in the Import cars collection.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-featured', '-created_at')
		indexes = [
			models.Index(fields=('make', 'model')),
			models.Index(fields=('price', 'availability')),
		]

	def __str__(self):
		return f'{self.year} {self.make} {self.model}'

	@property
	def display_image(self):
		if self.image:
			return self.image.url
		return self.image_url


class ContactMessage(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=30, blank=True)
	subject = models.CharField(max_length=200, blank=True)
	message = models.TextField()
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f'{self.name} - {self.subject or "General enquiry"}'


class Booking(models.Model):
	car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='bookings')
	name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=30, blank=True)
	preferred_date = models.DateField(null=True, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f'{self.name} - {self.car}'
