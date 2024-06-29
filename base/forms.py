from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import User, Court, Venue ,Booking, BookingCourt 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    accountType = forms.ChoiceField(choices=User.accountChoices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'phone_num', 'accountType', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.phone_num = self.cleaned_data['phone_num']
        user.accountType = self.cleaned_data['accountType']
        if commit:
            user.save()
        return user

class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    accountType = forms.ChoiceField(choices=User.accountChoices, widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'phone_num', 'accountType', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
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
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=Booking.statusChoices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['userID', 'price', 'status']

    def save(self, commit=True):
        booking = super().save(commit=False)
        if commit:
            booking.save()
        return booking

class BookingCourtForm(forms.ModelForm):
    court = forms.ModelChoiceField(queryset=Court.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    startTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    endTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))

    class Meta:
        model = BookingCourt
        fields = ['startTime', 'endTime', 'court']
