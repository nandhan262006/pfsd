from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProfessionalProfile


@admin.action(description='Verify selected professional profiles')
def verify_professionals(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.action(description='Unverify selected professional profiles')
def unverify_professionals(modeladmin, request, queryset):
    queryset.update(is_verified=False)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'date_joined', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('ProConnect Profile', {'fields': ('role', 'phone', 'bio', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ProConnect Profile', {'fields': ('role', 'phone')}),
    )


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'category', 'location', 'hourly_rate', 'experience_years', 'is_verified', 'availability', 'avg_rating']
    list_filter = ['category', 'is_verified', 'availability']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'location']
    list_editable = ['is_verified', 'availability']
    actions = [verify_professionals, unverify_professionals]

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Name'
