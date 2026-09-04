from django.contrib import admin

from .models import Booking, Car, ContactMessage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ('make', 'model', 'year', 'price', 'is_import', 'availability', 'featured')
	list_filter = ('is_import', 'availability', 'condition', 'featured', 'body_type')
	search_fields = ('make', 'model', 'description')
	list_editable = ('is_import', 'featured', 'availability')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
	list_filter = ('is_read', 'created_at')
	search_fields = ('name', 'email', 'subject', 'message')
	readonly_fields = ('created_at',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('name', 'car', 'email', 'preferred_date', 'created_at')
	search_fields = ('name', 'email', 'car__make', 'car__model')
	readonly_fields = ('created_at',)
