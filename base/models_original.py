import uuid
from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class CustomAccountManager(BaseUserManager):
        def create_user(self, name, email, password, **other_fields):
            if not email:
                raise ValueError(gettext_lazy("You must provide your email"))
            
            email = self.normalize_email(email)
            user = self.model(email = email, name = name, password = password, **other_fields)
            user.set_password(password)
            user.save()
            return user
        
        
        def create_superuser(self, name, email, password, **other_fields):
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
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',  # Customizing the reverse accessor name
        blank=True,
        help_text=gettext_lazy('The groups this user belongs to. A user may belong to multiple groups.')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set',  # Customizing the reverse accessor name
        blank=True,
        help_text=gettext_lazy('Specific permissions for this user.')
    )
    userID = models.UUIDField(primary_key=True, default=uuid.uuid4())
    #username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(gettext_lazy("email address"),unique=True)
    #password = models.CharField(max_length= 255)
    phone_num = models.CharField(max_length= 255, null=True)
    accountType = models.CharField(
        max_length=10,
        choices= accountChoices,
        default='EXT',
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name
    
class Venue(models.Model):
    venueName = models.CharField(max_length= 255)
    bookingToggle = models.BooleanField()
    
    def __str__(self):
        return self.venueName
    
    
class Court(models.Model):
    courtName = models.CharField(max_length= 255)
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
    
    bookingID = models.UUIDField(primary_key=True, default=uuid.uuid4())
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    bookTime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(
        max_length=10,
        choices= statusChoices,
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
    holidayName = models.CharField(max_length= 255)
    holidayDate = models.DateField()
    venueID = models.ForeignKey('Venue', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.holidayName
    
class Event(models.Model):
    eventName = models.CharField(max_length= 255)
    imgRef = models.ImageField()
    eventDescription = models.TextField()
    showToggle = models.BooleanField()
    
    def __str__(self):
        return self.eventName
    