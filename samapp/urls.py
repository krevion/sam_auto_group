from django.urls import path

from . import views


app_name = 'samapp'

urlpatterns = [
	path('', views.home, name='home'),
	path('cars/', views.cars, name='cars'),
	path('cars/<int:pk>/', views.car_detail, name='car_detail'),
	path('cars/<int:pk>/book/', views.book_car, name='book_car'),
	path('about/', views.about_us, name='about'),
	path('contact/', views.contact_us, name='contact'),
	path('payments/', views.payment_options, name='payments'),
	path('imports/', views.imports_only, name='imports'),
]
