from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser, ProfessionalProfile
from .forms import UserRegisterForm, ProfessionalProfileForm, UserEditForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserRegisterForm(request.POST or None)
    prof_form = ProfessionalProfileForm(request.POST or None)

    if request.method == 'POST':
        role = request.POST.get('role', 'user')
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.save()

            if role == 'professional' and prof_form.is_valid():
                profile = prof_form.save(commit=False)
                profile.user = user
                profile.save()
            elif role == 'professional' and not prof_form.is_valid():
                # Re-render with errors
                return render(request, 'accounts/register.html', {
                    'form': form, 'prof_form': prof_form
                })

            login(request, user)
            messages.success(request, f'Welcome to ProConnect, {user.first_name or user.username}! Your account has been created.')
            return redirect('home')

    return render(request, 'accounts/register.html', {
        'form': form,
        'prof_form': prof_form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    prof_profile = None
    if user.is_professional:
        try:
            prof_profile = user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            pass
    return render(request, 'accounts/profile.html', {
        'user': user,
        'prof_profile': prof_profile,
    })


@login_required
def profile_edit_view(request):
    user = request.user
    prof_profile = None
    if user.is_professional:
        try:
            prof_profile = user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            prof_profile = None

    user_form = UserEditForm(request.POST or None, request.FILES or None, instance=user)
    prof_form = ProfessionalProfileForm(request.POST or None, instance=prof_profile) if user.is_professional else None

    if request.method == 'POST':
        user_valid = user_form.is_valid()
        prof_valid = (not user.is_professional) or (prof_form and prof_form.is_valid())

        if user_valid and prof_valid:
            user_form.save()
            if user.is_professional and prof_form:
                if prof_profile:
                    prof_form.save()
                else:
                    p = prof_form.save(commit=False)
                    p.user = user
                    p.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'prof_form': prof_form,
    })


def professional_public_profile(request, pk):
    prof = get_object_or_404(ProfessionalProfile, pk=pk)
    reviews = prof.reviews.select_related('reviewer').order_by('-created_at')
    services = prof.services.all()
    return render(request, 'accounts/professional_profile.html', {
        'prof': prof,
        'reviews': reviews,
        'services': services,
        'star_range': range(1, 6),
    })
