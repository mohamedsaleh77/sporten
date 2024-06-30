import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomAccountManager(BaseUserManager):
    def create_user(self, name, email, password=None, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('accountType', 'ADM')
        
        return self.create_user(name, email, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    accountChoices = [
        ('EXT', 'External'),
        ('STU', 'Student'),
        ('STA', 'Staff'),
        ('ADM', 'Admin'),
    ]
    userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    phone_num = models.CharField(max_length=255, null=True)
    accountType = models.CharField(
        max_length=10,
        choices=accountChoices,
        default='EXT',
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # New field added
    
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name

class Venue(models.Model):
    venueName = models.CharField(max_length=255)
    bookingToggle = models.BooleanField()
    image = models.ImageField(upload_to='venues/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.venueName

class Court(models.Model):
    courtName = models.CharField(max_length=255)
    opening = models.TimeField()
    closing = models.TimeField()
    rate = models.DecimalField(decimal_places=2, max_digits=10)
    bookingToggle = models.BooleanField()
    venueID = models.ForeignKey("Venue", on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.courtName

class Booking(models.Model):
    statusChoices = [
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    
    bookingID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    bookTime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(
        max_length=10,
        choices=statusChoices,
        default='PENDING',
    )
    
    def __str__(self):
        return str(self.bookingID)

class BookingCourt(models.Model):
    booking = models.ForeignKey("Booking", on_delete=models.CASCADE)
    court = models.ForeignKey("Court", on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    
    def __str__(self):
        return f"{self.booking.bookingID}-{self.court.courtName}"

class Holiday(models.Model):
    holidayName = models.CharField(max_length=255)
    holidayDate = models.DateField()
    venueID = models.ForeignKey('Venue', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.holidayName

class Event(models.Model):
    eventName = models.CharField(max_length=255)
    imgRef = models.ImageField(upload_to='images/')
    eventDescription = models.TextField()
    showToggle = models.BooleanField()

class BannerImage(models.Model):
    image = models.ImageField(upload_to='banners/')
    description = models.CharField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return self.eventName
