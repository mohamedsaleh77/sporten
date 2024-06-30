from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Mostly Static Pages
    path('', views.load_home, name='load_home'),
    path('about/', views.about, name='about'),
    path("history/", views.history, name="history"),
    
    # Login & Logout
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    
    # Booking and Calendar Handling
    path('booking/<int:pk>/', views.bookingPage, name='booking'),
    path('populate_timeline/', views.populateTimeline, name='populateTimeline'),
    path('select_date/<str:date>/', views.dateSelected, name="dateSelected"),
    path('create_booking/', views.createBooking, name='createBooking'),
    #path('fetch_events/', views.fetchEvents, name='fetchEvents'),
    
    #Admin Panel and Functionality
    path('adminpanel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('adminpanel/users/', views.admin_users, name='admin_users'),
    path('adminpanel/roles/', views.admin_roles, name='admin_roles'),
    path('adminpanel/settings/', views.admin_settings, name='admin_settings'),
    path('adminpanel/', views.admin_dashboard, name='base_admin'),
    path('adminpanel/', RedirectView.as_view(url='/adminpanel/dashboard/', permanent=False), name='adminpanel_redirect'),
    path('adminpanel/toggle_user_active_status/<str:user_id>/', views.toggle_user_active_status, name='toggle_user_active_status'),
    path('adminpanel/courts/', views.admin_courts, name='admin_courts'),
    path('adminpanel/venues/', views.admin_venues, name='admin_venues'),
    path('adminpanel/courts/create/', views.create_court, name='create_court'),
    path('adminpanel/venues/create/', views.create_venue, name='create_venue'),
    path('adminpanel/courts/update/<int:court_id>/', views.update_court, name='update_court'),
    path('adminpanel/venues/update/<int:venue_id>/', views.update_venue, name='update_venue'),
    path('adminpanel/courts/delete/<int:court_id>/', views.delete_court, name='delete_court'),
    path('adminpanel/venues/delete/<int:venue_id>/', views.delete_venue, name='delete_venue'), 
    path('adminpanel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('adminpanel/bookings/create/', views.create_booking, name='create_booking'),
    path('adminpanel/bookings/update/<uuid:booking_id>/', views.update_booking, name='update_booking'),
    path('adminpanel/bookings/delete/<uuid:booking_id>/', views.delete_booking, name='delete_booking'),
    path('adminpanel/update_booking_status/<uuid:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('adminpanel/courts/toggle_booking_status/<int:court_id>/', views.toggle_court_booking_status, name='toggle_court_booking_status'),
    path('adminpanel/venues/toggle_booking_status/<int:venue_id>/', views.toggle_venue_booking_status, name='toggle_venue_booking_status'),
    path('adminpanel/backup/', views.admin_backup, name='admin_backup'),
    path('adminpanel/backup/notification/', views.backup_notification, name='backup_notification'),
    

    path('adminpanel/users/create/', views.create_user, name='create_user'),
    path('adminpanel/users/update/<uuid:user_id>/', views.update_user, name='update_user'),
    path('adminpanel/users/delete/<uuid:user_id>/', views.delete_user, name='delete_user'),
    path('adminpanel/users/update_account_type/<uuid:user_id>/', views.update_user_account_type, name='update_user_account_type'),

    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my_bookings/update/<uuid:booking_id>/', views.user_update_booking, name='user_update_booking'),
    path('my_profile/', views.my_profile, name='my_profile'),

    
    path('adminpanel/events/', views.admin_events, name='events'),
    path('adminpanel/events/add/', views.add_event, name='add_event'),
    path('adminpanel/events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('adminpanel/events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('adminpanel/events/toggle_show_status/<int:event_id>/', views.toggle_event_show_status, name='toggle_event_show_status'),



] 

