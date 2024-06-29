from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import User, Court, Venue

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