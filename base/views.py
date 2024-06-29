from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from .models import *
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from .models import Court, Venue
from .forms import CourtForm, VenueForm

# Mostly Static Pages
def load_home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# Login, Logout & Register
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return render(request, 'login_register.html')

            user = authenticate(request, username=user.email, password=password)
            if user is not None:
                login(request, user)
                return redirect('load_home')
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Please fill out all fields")
    
    return render(request, 'login_register.html')

def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('loginPage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logoutPage(request):
    logout(request)
    return redirect('load_home')

@login_required
def bookingPage(request, pk):
    venueGet = Venue.objects.get(id=pk)
    courtsGet = Court.objects.filter(venueID=venueGet)
    courts = list(courtsGet.values())
    holidaysGet = Holiday.objects.filter(venueID=venueGet)
    holidays = list(holidaysGet.values())
    context = {'courts': courts, "venue": venueGet, "holidays": holidays}
    return render(request, 'booking.html', context)

# Booking Related
def dateSelected(request, date):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    bookings = BookingCourt.objects.filter(startTime__date(date_obj))
    booking_data = list(bookings.values())
    return JsonResponse({'bookings': booking_data})

def createBooking(request):
    print('Received Request')
    if request.method == 'POST':
        # Get the JSON data from the request body
        booking_data = request.POST.get('eventsArray[0]')
        print(booking_data)
    
    return render(request, 'history.html')

# Admin Related
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_bookings(request):
    bookings = BookingCourt.objects.select_related('booking__userID', 'court__venueID').all()

    context = {
        'bookings': bookings,
    }
    return render(request, 'adminpanel/bookings.html', context)


@login_required
@user_passes_test(is_admin)
@require_POST
def update_booking_status(request, booking_id):
    try:
        booking = BookingCourt.objects.get(pk=booking_id)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled']:
            booking.status = new_status
            booking.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except BookingCourt.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Booking does not exist'})


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/users.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def toggle_user_active_status(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({'success': True, 'is_active': user.is_active})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'})

@login_required
@user_passes_test(is_admin)
def admin_roles(request):
    return render(request, 'adminpanel/roles.html')

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    return render(request, 'adminpanel/settings.html')

@login_required
@user_passes_test(is_admin)
def admin_backup(request):
    return render(request, 'adminpanel/backup.html')

@login_required
@user_passes_test(is_admin)
def admin_courts(request):
    courts = Court.objects.all()
    return render(request, 'adminpanel/courts.html', {'courts': courts})

@login_required
@user_passes_test(is_admin)
def admin_venues(request):
    venues = Venue.objects.all()
    return render(request, 'adminpanel/venues.html', {'venues': venues})

@login_required
@user_passes_test(is_admin)
def create_court(request):
    if request.method == 'POST':
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_courts')
    else:
        form = CourtForm()
    return render(request, 'adminpanel/court_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def create_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_venues')
    else:
        form = VenueForm()
    return render(request, 'adminpanel/venue_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    if request.method == 'POST':
        form = CourtForm(request.POST, instance=court)
        if form.is_valid():
            form.save()
            return redirect('admin_courts')
    else:
        form = CourtForm(instance=court)
    return render(request, 'adminpanel/court_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    court.delete()
    return redirect('admin_courts')



@login_required
@user_passes_test(is_admin)
def update_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('admin_venues')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'adminpanel/venue_form.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()
    return redirect('admin_venues')