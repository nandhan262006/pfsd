from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('professional', 'Professional'),
    ('user', 'User'),
]

CATEGORY_CHOICES = [
    ('electrician', 'Electrician'),
    ('plumber', 'Plumber'),
    ('tutor', 'Tutor'),
    ('designer', 'Designer'),
    ('cleaner', 'Cleaner'),
    ('carpenter', 'Carpenter'),
    ('painter', 'Painter'),
    ('mechanic', 'Mechanic'),
    ('photographer', 'Photographer'),
    ('other', 'Other'),
]


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_professional(self):
        return self.role == 'professional'

    @property
    def is_regular_user(self):
        return self.role == 'user'


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='professional_profile'
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=200)
    availability = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.get_category_display()}"

    def update_avg_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(professional=self)
        if reviews.exists():
            self.avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.save(update_fields=['avg_rating'])

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def star_range(self):
        return range(1, 6)
