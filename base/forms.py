from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import User, Court, Venue ,Booking, BookingCourt 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        if commit:
            user.save()
        return user

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['courtName', 'opening', 'closing', 'rate', 'bookingToggle', 'venueID']

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venueName', 'bookingToggle']

class BookingForm(forms.ModelForm):
    userID = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    court = forms.ModelChoiceField(queryset=Court.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    startTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    endTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    
    class Meta:
        model = Booking
        fields = ['userID', 'price', 'status']

    def save(self, commit=True):
        booking = super().save(commit=False)
        if commit:
            booking.save()
        return booking

class BookingCourtForm(forms.ModelForm):
    class Meta:
        model = BookingCourt
        fields = ['startTime', 'endTime', 'court', 'booking']