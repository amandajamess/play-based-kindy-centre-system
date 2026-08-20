from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Unified Signal to Automatically Create UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# User Profile Model with Role Support
class UserProfile(models.Model):
    # Define user types as choices
    USER_TYPES = [
        ('parent', 'Parent'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.user.username


# Toddler Model (Unchanged)
class Toddler(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255, blank=True, unique=True)  # Auto-generated
    ic_number = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    address = models.TextField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    registration_date = models.DateField(auto_now_add=True)

    # Parent Information
    parent_name = models.CharField(max_length=255, blank=True, null=False)

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


# Schedule Model 
class Schedule(models.Model):
    toddler = models.ForeignKey(Toddler, on_delete=models.CASCADE)
    date = models.DateField()  # Proper date handling
    start_time = models.TimeField()  # Proper time handling
    end_time = models.TimeField()  # Proper time handling
    activity_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Schedule for {self.toddler.full_name} on {self.date}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('fpx', 'FPX (Online Banking)'),
        ('card', 'Credit/Debit Card'),
    ]
    toddler = models.ForeignKey(Toddler, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)  # FPX bank field
    card_info = models.CharField(max_length=100, blank=True, null=True)  # Card info field

    def clean(self):
        errors = {}

        # Ensure toddler is provided
        if not self.toddler:
            errors['toddler'] = "This field is required."

        # Validate based on payment method
        if self.payment_method == 'fpx':
            if not self.bank:
                errors['bank'] = "Bank selection is required for FPX payment method."
            self.card_info = None  # Ensure card_info is not stored incorrectly
        
        elif self.payment_method == 'card':
            if not self.card_info:
                errors['card_info'] = "Card information is required for Card payment method."
            self.bank = None  # Ensure bank is not stored incorrectly
        
        else:
            errors['payment_method'] = "Invalid payment method."

        # Raise validation error if any
        if errors:
            raise ValidationError(errors)


class Feedback(models.Model):
    toddler = models.ForeignKey(Toddler, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=20, choices=[ ('Teacher', 'Teacher')])
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)  # Field for admin's reply
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.toddler.full_name} to {self.recipient}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    
    toddler = models.ForeignKey(Toddler, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.toddler.full_name} - {self.date} - {self.status}"


def get_default_user_profile():
    return UserProfile.objects.filter(user_type__in=['teacher', 'parent']).first()



class PerformanceRating(models.Model):
    ACTIVITY_CHOICES = [
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor"),
    ]
 
    toddler = models.ForeignKey(Toddler, on_delete=models.CASCADE)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # Ensure rating stays between 1 and 5
 
    date = models.DateField(auto_now_add=True)  # Automatically add date when rating is created
 
    def __str__(self):
        return f"{self.toddler.full_name} - {self.activity} - {self.rating} Stars"
 