from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import os

from .models import Animal, Report, AdoptionRequest, Shelter, Update
from .forms import (
    UserRegistrationForm, AnimalForm, ReportForm, 
    AdoptionRequestForm, ShelterForm, UpdateForm
)
from .ai_recognition import recognizer
from .notification_utils import (
    notify_nearby_shelters_about_report,
    notify_shelter_about_adoption_request,
    notify_shelter_about_report_update
)


def home(request):
    """Home page with featured animals and recent reports"""
    featured_animals = Animal.objects.filter(status='available')[:6]
    recent_reports = Report.objects.filter(status='open')[:6]
    
    context = {
        'featured_animals': featured_animals,
        'recent_reports': recent_reports,
    }
    return render(request, 'rescue/home.html', context)


def register(request):
    """User registration with User/NGO selection"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            
            # If NGO is selected, create shelter profile
            if user_type == 'ngo':
                from geopy.geocoders import Nominatim
                from geopy.exc import GeocoderTimedOut, GeocoderServiceError
                
                # Set first_name and last_name to empty or use shelter name for NGOs
                if not user.first_name and not user.last_name:
                    user.first_name = form.cleaned_data.get('shelter_name', '')[:30]
                    user.last_name = ''
                    user.save()
                
                shelter = Shelter.objects.create(
                    user=user,
                    name=form.cleaned_data['shelter_name'],
                    address=form.cleaned_data['shelter_address'],
                    city=form.cleaned_data['shelter_city'],
                    state=form.cleaned_data['shelter_state'],
                    zip_code=form.cleaned_data['shelter_zip_code'],
                    phone=form.cleaned_data['shelter_phone'],
                    email=user.email,
                    website=form.cleaned_data.get('shelter_website', '')
                )
                
                # Geocoding for location
                try:
                    geolocator = Nominatim(user_agent="animal_rescue")
                    location_str = f"{shelter.address}, {shelter.city}, {shelter.state} {shelter.zip_code}"
                    location = geolocator.geocode(location_str, timeout=10)
                    if location:
                        shelter.latitude = location.latitude
                        shelter.longitude = location.longitude
                        shelter.save()
                except (GeocoderTimedOut, GeocoderServiceError):
                    pass
                
                login(request, user)
                messages.success(request, 'NGO registration successful! Your shelter profile has been created.')
                return redirect('dashboard')
            else:
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'rescue/register.html', {'form': form})


def animal_list(request):
    """List all available animals with filters"""
    animals = Animal.objects.filter(status='available')
    
    # Filters
    animal_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    
    if animal_type:
        animals = animals.filter(animal_type=animal_type)
    if search:
        animals = animals.filter(
            Q(name__icontains=search) |
            Q(breed__icontains=search) |
            Q(description__icontains=search)
        )
    
    paginator = Paginator(animals, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'animal_type': animal_type,
        'search': search,
    }
    return render(request, 'rescue/animal_list.html', context)


def animal_detail(request, pk):
    """Animal detail page"""
    animal = get_object_or_404(Animal, pk=pk)
    adoption_request = None
    if request.user.is_authenticated:
        adoption_request = AdoptionRequest.objects.filter(
            animal=animal, user=request.user
        ).first()
    
    context = {
        'animal': animal,
        'adoption_request': adoption_request,
    }
    return render(request, 'rescue/animal_detail.html', context)


@login_required
def report_create(request):
    """Create a new report"""
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            
            # AI Image Recognition
            if report.photo:
                animal_type, confidence = recognizer.recognize_animal(report.photo.path)
                if animal_type:
                    report.ai_identified_type = animal_type
                    report.ai_confidence = confidence
                    # Auto-fill animal type if not set
                    if not report.animal_type:
                        report.animal_type = animal_type
            
            # Geocoding for location
            try:
                geolocator = Nominatim(user_agent="animal_rescue")
                location_str = f"{report.location}, {report.city}, {report.state} {report.zip_code}"
                location = geolocator.geocode(location_str, timeout=10)
                if location:
                    report.latitude = location.latitude
                    report.longitude = location.longitude
            except (GeocoderTimedOut, GeocoderServiceError):
                pass
            
            report.save()
            
            # Notify nearby shelters about the new report
            notify_nearby_shelters_about_report(report)
            
            messages.success(request, 'Report submitted successfully! Nearby NGOs have been notified.')
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm()
    return render(request, 'rescue/report_form.html', {'form': form, 'title': 'Report Animal'})


def report_list(request):
    """List all reports"""
    reports = Report.objects.all()
    
    # Filters
    report_type = request.GET.get('type', '')
    animal_type = request.GET.get('animal_type', '')
    city = request.GET.get('city', '')
    
    if report_type:
        reports = reports.filter(report_type=report_type)
    if animal_type:
        reports = reports.filter(animal_type=animal_type)
    if city:
        reports = reports.filter(city__icontains=city)
    
    paginator = Paginator(reports, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'report_type': report_type,
        'animal_type': animal_type,
        'city': city,
    }
    return render(request, 'rescue/report_list.html', context)


def report_detail(request, pk):
    """Report detail page"""
    report = get_object_or_404(Report, pk=pk)
    updates = report.updates.all()
    
    context = {
        'report': report,
        'updates': updates,
    }
    return render(request, 'rescue/report_detail.html', context)


@login_required
def adoption_request_create(request, animal_pk):
    """Create adoption request"""
    animal = get_object_or_404(Animal, pk=animal_pk)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.animal = animal
            adoption_request.user = request.user
            adoption_request.save()
            
            # Notify shelter about the adoption request
            notify_shelter_about_adoption_request(adoption_request)
            
            messages.success(request, 'Adoption request submitted! The shelter has been notified.')
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'rescue/adoption_request_form.html', {
        'form': form,
        'animal': animal
    })


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    # Check if user is a shelter
    is_shelter = hasattr(user, 'shelter')
    shelter = user.shelter if is_shelter else None
    
    context = {
        'is_shelter': is_shelter,
        'shelter': shelter,
    }
    
    if is_shelter:
        # Shelter dashboard
        from .models import Notification
        animals = Animal.objects.filter(shelter=shelter)
        adoption_requests = AdoptionRequest.objects.filter(
            animal__shelter=shelter
        ).order_by('-created_at')[:10]
        notifications = Notification.objects.filter(
            shelter=shelter
        ).order_by('-created_at')[:10]
        unread_count = Notification.objects.filter(
            shelter=shelter,
            is_read=False
        ).count()
        
        context.update({
            'animals': animals,
            'adoption_requests': adoption_requests,
            'notifications': notifications,
            'unread_count': unread_count,
        })
    else:
        # Regular user dashboard
        user_reports = Report.objects.filter(reported_by=user)[:10]
        user_adoption_requests = AdoptionRequest.objects.filter(user=user)[:10]
        
        context.update({
            'user_reports': user_reports,
            'user_adoption_requests': user_adoption_requests,
        })
    
    return render(request, 'rescue/dashboard.html', context)


@login_required
def shelter_create(request):
    """Create shelter profile"""
    if hasattr(request.user, 'shelter'):
        messages.info(request, 'You already have a shelter profile.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            shelter = form.save(commit=False)
            shelter.user = request.user
            
            # Geocoding
            try:
                geolocator = Nominatim(user_agent="animal_rescue")
                location_str = f"{shelter.address}, {shelter.city}, {shelter.state} {shelter.zip_code}"
                location = geolocator.geocode(location_str, timeout=10)
                if location:
                    shelter.latitude = location.latitude
                    shelter.longitude = location.longitude
            except (GeocoderTimedOut, GeocoderServiceError):
                pass
            
            shelter.save()
            messages.success(request, 'Shelter profile created!')
            return redirect('dashboard')
    else:
        form = ShelterForm()
    
    return render(request, 'rescue/shelter_form.html', {'form': form})


@login_required
def animal_create(request):
    """Create animal profile (for shelters)"""
    if not hasattr(request.user, 'shelter'):
        messages.error(request, 'You must be a shelter to add animals.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.shelter = request.user.shelter
            animal.created_by = request.user
            animal.save()
            messages.success(request, 'Animal profile created!')
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm()
    
    return render(request, 'rescue/animal_form.html', {'form': form, 'title': 'Add Animal'})


@login_required
def animal_edit(request, pk):
    """Edit animal profile"""
    animal = get_object_or_404(Animal, pk=pk)
    
    if not hasattr(request.user, 'shelter') or animal.shelter != request.user.shelter:
        messages.error(request, 'You do not have permission to edit this animal.')
        return redirect('animal_detail', pk=pk)
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal profile updated!')
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'rescue/animal_form.html', {'form': form, 'title': 'Edit Animal', 'animal': animal})


@login_required
def adoption_request_manage(request, pk):
    """Manage adoption request (approve/reject)"""
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk)
    
    if not hasattr(request.user, 'shelter') or adoption_request.animal.shelter != request.user.shelter:
        messages.error(request, 'You do not have permission to manage this request.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            adoption_request.status = 'approved'
            adoption_request.animal.status = 'pending'
            adoption_request.animal.save()
            messages.success(request, 'Adoption request approved!')
        elif action == 'reject':
            adoption_request.status = 'rejected'
            messages.info(request, 'Adoption request rejected.')
        adoption_request.save()
        return redirect('dashboard')
    
    return render(request, 'rescue/adoption_request_manage.html', {
        'adoption_request': adoption_request
    })


@login_required
def update_create(request, animal_pk=None, report_pk=None):
    """Create update for animal or report"""
    animal = None
    report = None
    
    if animal_pk:
        animal = get_object_or_404(Animal, pk=animal_pk)
        if hasattr(request.user, 'shelter') and animal.shelter != request.user.shelter:
            messages.error(request, 'You do not have permission to create updates for this animal.')
            return redirect('animal_detail', pk=animal_pk)
    
    if report_pk:
        report = get_object_or_404(Report, pk=report_pk)
    
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.animal = animal
            update.report = report
            update.created_by = request.user
            update.save()
            
            # Notify shelters about report updates
            if report:
                notify_shelter_about_report_update(update)
            
            messages.success(request, 'Update posted!')
            if animal:
                return redirect('animal_detail', pk=animal.pk)
            elif report:
                return redirect('report_detail', pk=report.pk)
    else:
        form = UpdateForm()
    
    return render(request, 'rescue/update_form.html', {
        'form': form,
        'animal': animal,
        'report': report
    })


@login_required
def notifications(request):
    """View all notifications for a shelter"""
    if not hasattr(request.user, 'shelter'):
        messages.error(request, 'You must be a shelter to view notifications.')
        return redirect('dashboard')
    
    from .models import Notification
    shelter = request.user.shelter
    notifications_list = Notification.objects.filter(shelter=shelter).order_by('-created_at')
    unread_count = Notification.objects.filter(shelter=shelter, is_read=False).count()
    
    context = {
        'notifications': notifications_list,
        'unread_count': unread_count,
    }
    return render(request, 'rescue/notifications.html', context)


@login_required
def notification_mark_read(request, notification_id):
    """Mark a notification as read"""
    from .models import Notification
    notification = get_object_or_404(Notification, pk=notification_id)
    
    if not hasattr(request.user, 'shelter') or notification.shelter != request.user.shelter:
        messages.error(request, 'You do not have permission to access this notification.')
        return redirect('dashboard')
    
    notification.is_read = True
    notification.save()
    
    return redirect('notifications')


@login_required
def notification_mark_all_read(request):
    """Mark all notifications as read"""
    if not hasattr(request.user, 'shelter'):
        messages.error(request, 'You must be a shelter.')
        return redirect('dashboard')
    
    from .models import Notification
    Notification.objects.filter(shelter=request.user.shelter, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications')


