from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from .models import *
from datetime import datetime, timedelta
import json 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from .models import Court, Venue
from .forms import CourtForm, VenueForm, BookingForm, BookingCourtForm, CustomUserUpdateForm
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import subprocess
import shutil
from django.urls import reverse
from django.db.models import Count, Sum
from dateutil.parser import parse as parse_date
from django.forms.models import model_to_dict

# Mostly Static Pages
def load_home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def history(request):
    return render(request, 'history.html')

#============================================================================

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

#============================================================================

# Booking Related
@login_required
def bookingPage(request, pk):
    venueGet = Venue.objects.get(id=pk)
    courtsGet = Court.objects.filter(venueID=venueGet, bookingToggle=True)
    courts = list(courtsGet.values())
    holidaysGet = Holiday.objects.filter(venueID=venueGet)
    holidays = list(holidaysGet.values())
    venue_dict = model_to_dict(venueGet)
    context = {'courts': courts, "venue": venue_dict, "holidays": holidays}
    print(context)
    return render(request, 'booking.html', context)

def dateSelected(request, date):
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    bookings = BookingCourt.objects.filter(startTime__date=date_obj)
    booking_data = list(bookings.values()) 
    print(booking_data)
    
    return JsonResponse({'bookings': booking_data})

def populateTimeline(request):
    if request.method == 'GET':
        try:
            date = request.GET.get('date')
            venue = request.GET.get('venue')
            if date and venue:
                courts = list(Court.objects.filter(venueID=venue))
                bookings = BookingCourt.objects.filter(startTime__date=date, court__in=courts, booking__status__in=['PENDING', 'COMPLETED']).order_by('court', 'startTime')
                events = []
                if bookings:
                    # Initialize the first booking
                    prev = bookings[0]

                    for b in bookings[1:]:
                        if b.court == prev.court and b.startTime <= prev.endTime:
                            # Merge the bookings if they intersect
                            prev.startTime = min(prev.startTime, b.startTime)
                            prev.endTime = max(prev.endTime, b.endTime)
                        else:
                            # If they do not intersect, add the previous booking to events and start a new one
                            events.append(prev)
                            prev = b

                    # Add the last booking
                    events.append(prev)
                    serialized_events = []
                    for event in events:
                        serialized_event = {
                            'id': event.id,
                            'startTime': event.startTime.isoformat(),
                            'endTime': event.endTime.isoformat(),
                            'courtID': event.court.id,
                        }
                        serialized_events.append(serialized_event)
                return JsonResponse({'status': 'success', 'events': serialized_events}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Date or venue parameter is missing'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def createBooking(request):
    print("Received")
    if request.method == 'POST':
        try:
            events_data = json.loads(request.POST.get('events', '[]'))
            # Process the events_data as needed
            print(events_data)  # For debugging purposes
            
            user = request.user
            
            # Create a new Booking instance
            booking = Booking.objects.create(
                userID=user,
                price=0.0,
                status='PENDING'
            )

            booking_courts = []
            total_fee = 0

            for event in events_data:
                resourceID = event['resourceId']
                court = Court.objects.get(id=resourceID[0])
                start_time = parse_date(event['start'])
                end_time = parse_date(event['end']) if event['end'] else None

                # Calculate duration and fee for the court
                duration_hours = (end_time - start_time).total_seconds() / 3600
                court_fee = duration_hours * float(court.rate)
                total_fee += court_fee

                # Create BookingCourt instance
                booking_court = BookingCourt(
                    booking=booking,
                    court=court,
                    startTime=start_time,
                    endTime=end_time
                )
                booking_courts.append(booking_court)

            # Bulk create all BookingCourt instances
            BookingCourt.objects.bulk_create(booking_courts)

            # Update the Booking with total price
            booking.price = total_fee
            booking.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    


def createBooking_sameh(request):
    print("Received")
    if request.method == 'POST':
        try:
            events_data = json.loads(request.POST.get('events', '[]'))
            # Process the events_data as needed
            print(events_data)  # For debugging purposes
            
            user = request.user
            
            # Create a new Booking instance
            booking = Booking.objects.create(
                userID=user,
                price = 0.0,
                status='PENDING'
            )

            booking_courts = []
            total_fee = 0

            for event in events_data:
                resourceID = event['resourceId']
                court = Court.objects.get(id=resourceID[0])
                start_time = datetime.fromisoformat(event['start'])
                end_time = datetime.fromisoformat(event['end']) if event['end'] else None

                # Calculate duration and fee for the court
                duration_hours = (end_time - start_time).total_seconds() / 3600
                court_fee = duration_hours * float(court.rate)
                total_fee += court_fee

                # Create BookingCourt instance
                booking_court = BookingCourt(
                    booking=booking,
                    court=court,
                    startTime=start_time,
                    endTime=end_time
                )
                booking_courts.append(booking_court)

            # Bulk create all BookingCourt instances
            BookingCourt.objects.bulk_create(booking_courts)

            # Update the Booking with total price
            booking.price = total_fee
            booking.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

#============================================================================

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
    return render(request, 'adminpanel/bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def create_booking(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        booking_court_form = BookingCourtForm(request.POST)
        if booking_form.is_valid() and booking_court_form.is_valid():
            booking = booking_form.save()
            booking_court = booking_court_form.save(commit=False)
            booking_court.booking = booking
            booking_court.save()
            return redirect('admin_bookings')
    else:
        booking_form = BookingForm()
        booking_court_form = BookingCourtForm()
    return render(request, 'adminpanel/booking_form.html', {'form': booking_form, 'booking_court_form': booking_court_form})

@login_required
@user_passes_test(is_admin)
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, bookingID=booking_id)
    booking_court = BookingCourt.objects.filter(booking=booking).first()
    if request.method == 'POST':
        booking_form = BookingForm(request.POST, instance=booking)
        booking_court_form = BookingCourtForm(request.POST, instance=booking_court)
        if booking_form.is_valid() and booking_court_form.is_valid():
            booking_form.save()
            booking_court_form.save()
            return redirect('admin_bookings')
    else:
        booking_form = BookingForm(instance=booking)
        booking_court_form = BookingCourtForm(instance=booking_court)
    return render(request, 'adminpanel/booking_form.html', {'form': booking_form, 'booking_court_form': booking_court_form})



@login_required
@user_passes_test(is_admin)
@require_POST
def toggle_court_booking_status(request, court_id):
    try:
        court = Court.objects.get(pk=court_id)
        court.bookingToggle = not court.bookingToggle
        court.save()
        return JsonResponse({'success': True, 'bookingToggle': court.bookingToggle})
    except Court.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Court does not exist'})

@login_required
@user_passes_test(is_admin)
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, bookingID=booking_id)
    booking.delete()
    return redirect('admin_bookings')

@login_required
@user_passes_test(is_admin)
@require_POST
def update_booking_status(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        new_status = request.POST.get('status')
        if new_status in ['PENDING', 'CONFIRMED', 'CANCELLED']:
            booking.status = new_status
            booking.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Booking.DoesNotExist:
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
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'adminpanel/user_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(User, userID=user_id)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'adminpanel/user_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, userID=user_id)
    user.delete()
    return redirect('admin_users')

@login_required
@user_passes_test(is_admin)
@require_POST
def update_user_account_type(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        new_account_type = request.POST.get('accountType')
        if new_account_type in dict(User.accountChoices).keys():
            user.accountType = new_account_type
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid account type'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'})

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
@require_POST
def toggle_venue_booking_status(request, venue_id):
    try:
        venue = Venue.objects.get(pk=venue_id)
        venue.bookingToggle = not venue.bookingToggle
        venue.save()
        return JsonResponse({'success': True, 'bookingToggle': venue.bookingToggle})
    except Venue.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Venue does not exist'})


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


@login_required
@user_passes_test(is_admin)
def admin_backup(request):
    db_path = settings.DATABASES['default']['NAME']
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backup_file = os.path.join(backup_dir, f'{os.path.basename(db_path)}_backup.sqlite3')

    os.makedirs(backup_dir, exist_ok=True)

    try:
        shutil.copy(db_path, backup_file)
        with open(backup_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(backup_file)}'
            # Redirect to the base_admin with a success parameter
            response['Refresh'] = f'0; url={reverse("base_admin")}?backup_success=1'
            return response
    except Exception as e:
        # Redirect to the base_admin with a failure parameter
        return HttpResponseRedirect(f'{reverse("base_admin")}?backup_success=0')

@login_required
@user_passes_test(is_admin)
def backup_notification(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'adminpanel/backup_notification.html', {'previous_url': previous_url})
    



@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # User statistics
    total_users = User.objects.count()
    new_users_last_week = User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=7)).count()
    active_users = User.objects.filter(is_active=True).count()

    # Booking statistics
    total_bookings = Booking.objects.count()
    new_bookings_last_week = Booking.objects.filter(bookTime__gte=datetime.now()-timedelta(days=7)).count()
    booking_status_distribution = list(Booking.objects.values('status').annotate(count=Count('status')))

    # Court usage
    most_booked_courts = list(Court.objects.annotate(bookings_count=Count('bookingcourt')).order_by('-bookings_count')[:5].values('courtName', 'bookings_count'))
    booking_courts = BookingCourt.objects.select_related('court').all()
    booking_hours_per_court = {}
    for booking_court in booking_courts:
        court_name = booking_court.court.courtName
        duration = (booking_court.endTime - booking_court.startTime).total_seconds() / 3600
        if court_name in booking_hours_per_court:
            booking_hours_per_court[court_name] += duration
        else:
            booking_hours_per_court[court_name] = duration

    peak_booking_times = {}
    for booking_court in booking_courts:
        hour = booking_court.startTime.hour
        if hour in peak_booking_times:
            peak_booking_times[hour] += 1
        else:
            peak_booking_times[hour] = 1

    # Financial metrics
    total_revenue = Booking.objects.aggregate(total_revenue=Sum('price'))['total_revenue']
    revenue_last_week = Booking.objects.filter(bookTime__gte=datetime.now()-timedelta(days=7)).aggregate(revenue=Sum('price'))['revenue']
    average_booking_price = Booking.objects.aggregate(average_price=Sum('price')/Count('bookingID'))['average_price']

    context = {
        'total_users': total_users,
        'new_users_last_week': new_users_last_week,
        'active_users': active_users,
        'total_bookings': total_bookings,
        'new_bookings_last_week': new_bookings_last_week,
        'booking_status_distribution': json.dumps(booking_status_distribution),
        'most_booked_courts': json.dumps(most_booked_courts),
        'booking_hours_per_court': json.dumps(booking_hours_per_court),
        'peak_booking_times': json.dumps(peak_booking_times),
        'total_revenue': total_revenue,
        'revenue_last_week': revenue_last_week,
        'average_booking_price': average_booking_price,
    }

    return render(request, 'adminpanel/dashboard.html', context)


# User Pages
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(userID=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def my_profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('my_profile')
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, 'my_profile.html', {'form': form})