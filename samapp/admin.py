from django.contrib import admin
from django.utils.html import format_html

from .models import Booking, Car, CarImage, ContactMessage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ('image', 'caption')
    classes = ('collapse',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
    list_display = ('make', 'model', 'year', 'price', 'availability', 'condition', 'featured', 'is_import')
    list_filter = ('availability', 'condition', 'featured', 'is_import', 'body_type')
    search_fields = ('make', 'model', 'description', 'body_type')
    list_editable = ('price', 'availability', 'featured', 'is_import')
    ordering = ('-featured', '-created_at')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    save_on_top = True
    list_per_page = 25
    fieldsets = (
        ('Vehicle basics', {
            'fields': (
                ('make', 'model', 'year'),
                ('condition', 'body_type', 'mileage'),
                'description',
            )
        }),
        ('Inventory & pricing', {
            'fields': (
                ('price', 'availability'),
                ('featured', 'is_import'),
                'image',
                'image_url',
                'image_preview',
            )
        }),
        ('Audit trail', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Current image')
    def image_preview(self, obj):
        if not obj.image:
            return 'No main image uploaded.'
        return format_html('<img src="{}" style="max-height:120px; width:auto; border-radius:8px;" />', obj.image.url)


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'caption', 'image', 'uploaded_at')
    search_fields = ('car__make', 'car__model', 'caption')
    list_filter = ('uploaded_at',)


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
