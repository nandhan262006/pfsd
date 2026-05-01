from django.db import models
from accounts.models import CustomUser, ProfessionalProfile

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

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Service(models.Model):
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_hours = models.IntegerField(default=1)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.professional.full_name}"


class Booking(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking #{self.pk} — {self.user.username} → {self.service.title}"

    @property
    def can_review(self):
        """True if booking is completed and no review has been left yet."""
        if self.status != 'completed':
            return False
        return not hasattr(self, 'review')
