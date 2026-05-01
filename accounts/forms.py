from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ProfessionalProfile, CATEGORY_CHOICES


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(
        choices=[('user', 'Regular User'), ('professional', 'Professional')],
        widget=forms.RadioSelect,
        initial='user'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': 'form-input'})


class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['category', 'experience_years', 'hourly_rate', 'location', 'availability']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, State'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
