from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import ProfessionalProfile
from .models import Service, Booking
from .forms import ServiceForm, BookingForm


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


def home_view(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()

    featured = ProfessionalProfile.objects.filter(is_verified=True, availability=True).order_by('-avg_rating')[:6]

    if query or location:
        filtered = ProfessionalProfile.objects.filter(is_verified=True)
        if query:
            filtered = filtered.filter(
                Q(category__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
        if location:
            filtered = filtered.filter(location__icontains=location)
        return render(request, 'services/browse.html', {
            'professionals': filtered,
            'categories': CATEGORY_CHOICES,
            'query': query,
            'location': location,
        })

    return render(request, 'home.html', {
        'featured': featured,
        'categories': CATEGORY_CHOICES,
    })


def browse_view(request):
    professionals = ProfessionalProfile.objects.filter(is_verified=True)

    category = request.GET.get('category', '')
    min_rating = request.GET.get('min_rating', '')
    available_only = request.GET.get('available', '')
    location = request.GET.get('location', '').strip()

    if category:
        professionals = professionals.filter(category=category)
    if min_rating:
        professionals = professionals.filter(avg_rating__gte=float(min_rating))
    if available_only:
        professionals = professionals.filter(availability=True)
    if location:
        professionals = professionals.filter(location__icontains=location)

    professionals = professionals.order_by('-avg_rating')

    return render(request, 'services/browse.html', {
        'professionals': professionals,
        'categories': CATEGORY_CHOICES,
        'selected_category': category,
        'selected_rating': min_rating,
        'available_only': available_only,
        'location': location,
    })


def service_detail_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})


@login_required
def book_service_view(request, service_id):
    if request.user.is_professional:
        messages.error(request, 'Professionals cannot book services.')
        return redirect('browse')

    service = get_object_or_404(Service, pk=service_id)
    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.service = service
        booking.status = 'pending'
        booking.save()
        messages.success(request, f'Booking confirmed! Your booking for "{service.title}" is pending approval.')
        return redirect('my_bookings')

    return render(request, 'services/booking_form.html', {
        'form': form,
        'service': service,
    })


@login_required
def my_bookings_view(request):
    if request.user.is_professional:
        return redirect('professional_bookings')

    bookings = Booking.objects.filter(user=request.user).select_related(
        'service', 'service__professional', 'service__professional__user'
    ).order_by('-created_at')

    return render(request, 'services/my_bookings.html', {'bookings': bookings})


@login_required
def professional_bookings_view(request):
    if not request.user.is_professional:
        messages.error(request, 'Access denied.')
        return redirect('home')

    try:
        prof = request.user.professional_profile
    except ProfessionalProfile.DoesNotExist:
        messages.error(request, 'Please complete your professional profile first.')
        return redirect('profile_edit')

    bookings = Booking.objects.filter(
        service__professional=prof
    ).select_related('user', 'service').order_by('-created_at')

    return render(request, 'services/professional_bookings.html', {'bookings': bookings})


@login_required
def update_booking_status_view(request, pk):
    if not request.user.is_professional:
        messages.error(request, 'Access denied.')
        return redirect('home')

    booking = get_object_or_404(Booking, pk=pk, service__professional__user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed = ['confirmed', 'completed', 'cancelled']
        if new_status in allowed:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking #{booking.pk} marked as {new_status}.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('professional_bookings')


@login_required
def add_service_view(request):
    if not request.user.is_professional:
        messages.error(request, 'Only professionals can add services.')
        return redirect('home')

    try:
        prof = request.user.professional_profile
    except ProfessionalProfile.DoesNotExist:
        messages.error(request, 'Please complete your professional profile first.')
        return redirect('profile_edit')

    form = ServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        service = form.save(commit=False)
        service.professional = prof
        service.save()
        messages.success(request, 'Service added successfully!')
        return redirect('profile')

    return render(request, 'services/add_service.html', {'form': form})


@login_required
def delete_service_view(request, pk):
    if not request.user.is_professional:
        return redirect('home')
    service = get_object_or_404(Service, pk=pk, professional__user=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
    return redirect('profile')
