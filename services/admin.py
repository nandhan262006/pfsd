from django.contrib import admin
from .models import Service, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'professional', 'category', 'price', 'duration_hours', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'professional__user__username']
    ordering = ['-created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'service', 'booking_date', 'booking_time', 'status', 'created_at']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'service__title']
    list_editable = ['status']
    ordering = ['-created_at']
