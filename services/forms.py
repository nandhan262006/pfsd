from django import forms
from .models import Service, Booking


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'duration_hours', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Service title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe your service...'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Any special instructions...'}),
        }
