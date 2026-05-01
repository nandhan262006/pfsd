from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Booking
from accounts.models import ProfessionalProfile
from .models import Review
from .forms import ReviewForm


@login_required
def add_review_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.status != 'completed':
        messages.error(request, 'You can only review completed bookings.')
        return redirect('my_bookings')

    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this booking.')
        return redirect('professional_profile', pk=booking.service.professional.pk)

    form = ReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.reviewer = request.user
        review.professional = booking.service.professional
        review.save()
        messages.success(request, 'Thank you for your review!')
        return redirect('professional_profile', pk=booking.service.professional.pk)

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'booking': booking,
    })


def review_detail_view(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})
