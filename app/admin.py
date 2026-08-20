from django.contrib import admin
from app.models import Toddler,UserProfile,Schedule
from .models import Payment
from django.utils.html import format_html
from django.urls import path
from django.http import JsonResponse
from .forms import PaymentAdminForm   # Make sure this import is correct
from django.shortcuts import render
from .models import Feedback, Attendance, PerformanceRating



# Register the Toddler model
@admin.register(Toddler)
class ToddlerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'ic_number', 'age', 'gender', 'parent_name', 'registration_date')
    search_fields = ('first_name', 'last_name','parent_name', 'ic_number')
    list_filter = ('gender', 'registration_date',)

    # Register other models if needed
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')

# Register the Schedule model
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('toddler__full_name', 'date', 'start_time', 'end_time', 'activity_name')  # Show toddler in the list
    search_fields = ('toddler__full_name', 'activity_name', 'date')  # Enable searching by toddler name
    list_filter = ('date', 'toddler__full_name')  # Enable filtering by date and toddler
    
    def toddler__full_name(self, obj):
        return obj.toddler.full_name  




@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm
    list_display = ('toddler', 'payment_method', 'amount', 'bank', 'card_info', 'reference')
    list_filter = ('payment_method',)
    search_fields = ('amount', 'reference', 'toddler__full_name')

    # Override fieldsets to conditionally show fields based on payment method
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Show bank or card_info based on the payment_method selected
        if obj and obj.payment_method == 'fpx':
            fieldsets[0][1].append('bank')  # Show bank for FPX payments
        elif obj and obj.payment_method == 'card':
            fieldsets[0][1].append('card_info')  # Show card_info for Card payments
        return fieldsets

    # Override to conditionally hide/show bank/card_info fields
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.payment_method == 'fpx':
            form.base_fields['card_info'].widget = forms.HiddenInput()  # Hide card_info if FPX
        elif obj and obj.payment_method == 'card':
            form.base_fields['bank'].widget = forms.HiddenInput()  # Hide bank if Card
        return form

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('toddler', 'recipient', 'message', 'reply', 'submitted_at')
    search_fields = ('toddler__full_name', 'recipient', 'message')
    list_filter = ('recipient', 'submitted_at')
    # Add the reply field to the form for the admin to edit
    fields = ('toddler', 'recipient', 'message', 'reply', 'submitted_at')
    readonly_fields = ('submitted_at',)  # Prevent modification of the submission date
   
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('toddler', 'date', 'status')  # Display these columns in admin panel
    list_filter = ('status', 'date')  # Add filters for status and date
    search_fields = ('toddler__full_name',)  # Allow searching by toddler name



@admin.register(PerformanceRating)
class PerformanceRatingAdmin(admin.ModelAdmin):
    list_display = ('toddler', 'activity', 'rating', 'date')  # Display these fields in the admin list view
    list_filter = ('activity', 'rating')  # Filters to quickly sort data
    search_fields = ('toddler__full_name',)  # Allow searching by toddler name
    ordering = ('-date',)  # Order by latest ratings first

