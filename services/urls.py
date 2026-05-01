from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('browse/', views.browse_view, name='browse'),
    path('service/<int:pk>/', views.service_detail_view, name='service_detail'),
    path('book/<int:service_id>/', views.book_service_view, name='book_service'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('professional/bookings/', views.professional_bookings_view, name='professional_bookings'),
    path('booking/<int:pk>/update-status/', views.update_booking_status_view, name='update_booking_status'),
    path('service/add/', views.add_service_view, name='add_service'),
    path('service/<int:pk>/delete/', views.delete_service_view, name='delete_service'),
]
