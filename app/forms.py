from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Toddler, Schedule, Attendance, PerformanceRating
from .models import Payment

    

class BootstrapSignUpForm(UserCreationForm):
    """Sign-Up form with Bootstrap styling for initial user creation."""
    # Add an email field
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        required=True  # Ensure email is required
    )

    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'User name'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password1"])  # Ensure password is hashed
            user.email = self.cleaned_data["email"]  # Save the email
            user.save()
        return user
    
class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        bank = cleaned_data.get('bank')
        card_info = cleaned_data.get('card_info')

        if payment_method == 'fpx' and not bank:
            self.add_error('bank', 'Bank is required for FPX payment method.')
        if payment_method == 'card' and not card_info:
            self.add_error('card_info', 'Card information is required for Card payment method.')

        return cleaned_data
        


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['toddler', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[('Present', 'Present'), ('Absent', 'Absent')], attrs={'class': 'form-control'}),
        }

class PerformanceRatingForm(forms.ModelForm):
    toddler = forms.ModelChoiceField(queryset=Toddler.objects.all(), empty_label="-- Select Toddler --")
    activity = forms.ChoiceField(choices=PerformanceRating.ACTIVITY_CHOICES)
    rating = forms.IntegerField(widget=forms.HiddenInput())  # Hidden field for rating (will be set via JS)
 
    class Meta:
        model = PerformanceRating
        fields = ['toddler', 'activity', 'rating']    

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['toddler', 'date', 'start_time', 'end_time', 'activity_name']
  