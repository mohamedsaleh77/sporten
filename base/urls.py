from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    # Mostly Static Pages
    path('', views.load_home, name='load_home'),
    path('about/', views.about, name='about'),
    
    # Login & Logout
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    
    # Booking and Calendar Handling
    path('booking/<int:pk>/', views.bookingPage, name='booking'),
    path('select_date/<str:date>/', views.dateSelected, name="dateSelected"),
    path('create_booking/', views.createBooking, name='createBooking'),
    
    #Admin Panel and Functionality
    path('adminpanel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('adminpanel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('adminpanel/users/', views.admin_users, name='admin_users'),
    path('adminpanel/roles/', views.admin_roles, name='admin_roles'),
    path('adminpanel/settings/', views.admin_settings, name='admin_settings'),
    path('adminpanel/backup/', views.admin_backup, name='admin_backup'),
    path('adminpanel/', RedirectView.as_view(url='/adminpanel/dashboard/', permanent=False), name='adminpanel_redirect'),
    path('adminpanel/toggle_user_active_status/<str:user_id>/', views.toggle_user_active_status, name='toggle_user_active_status'),
    path('adminpanel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('adminpanel/update_booking_status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('adminpanel/courts/', views.admin_courts, name='admin_courts'),
    path('adminpanel/venues/', views.admin_venues, name='admin_venues'),
    path('adminpanel/courts/create/', views.create_court, name='create_court'),
    path('adminpanel/venues/create/', views.create_venue, name='create_venue'),
    path('adminpanel/courts/update/<int:court_id>/', views.update_court, name='update_court'),
    path('adminpanel/venues/update/<int:venue_id>/', views.update_venue, name='update_venue'),
    path('adminpanel/courts/delete/<int:court_id>/', views.delete_court, name='delete_court'),
    path('adminpanel/venues/delete/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    

   
]
