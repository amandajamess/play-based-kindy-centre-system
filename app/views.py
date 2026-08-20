from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import UserProfile, Toddler, PerformanceRating  # Import models
from .forms import BootstrapSignUpForm
from .models import Payment, Toddler, UserProfile, Schedule, Attendance
from django.utils import timezone
from app.models import Toddler
from .forms import PaymentAdminForm, AttendanceForm, PerformanceRatingForm, ScheduleForm
from .models import Payment
from app.models import Feedback, Payment, Toddler
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json 


# Home view
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        # Redirect admin users to the admin dashboard
        if user_profile and user_profile.user_type == 'admin':
            return redirect('admin_dashboard')

        # Redirect teacher users to the teacher dashboard with similar structure
        elif user_profile and user_profile.user_type == 'teacher':
            section = request.GET.get('section', 'dashboard')

            context = {
                'title': 'Teacher Dashboard',
                'section': section,
                'teacher_name': request.user.first_name,
                'year': datetime.now().year,
            }
            return render(request, 'app/teacher_dashboard.html', context)

        # Redirect parent users to the parent dashboard
        elif user_profile and user_profile.user_type == 'parent':
            return redirect('parent_dashboard')

        # Redirect other users to the menu page
        else:
            return redirect('menu')  

    # Render home page for unauthenticated users
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


# Admin dashboard view
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'admin', login_url='home')
def admin_dashboard(request):
    """Renders the admin dashboard with metrics, search functionality, and feedback management."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    # Get the section from the query parameter (default is 'dashboard')
    section = request.GET.get('section', None)

    # Fetching common data
    
    total_toddlers = Toddler.objects.count()
    total_males = Toddler.objects.filter(gender='Male').count()
    total_females = Toddler.objects.filter(gender='Female').count()

    # Search Toddler functionality (handled when section is 'search_toddler')
    toddlers = None
    query = request.GET.get('toddler_ic', '').strip()  # Get 'toddler_ic' query parameter
    if section == 'search_toddler' and query:  # If section is 'search_toddler' and there is a search query
        toddlers = Toddler.objects.filter(ic_number__icontains=query)  # Search toddlers by IC number

    # Handle update for a specific toddler (if section is 'update_toddler')
    toddler_to_update = None
    if section == 'update_toddler':
        toddler_id = request.GET.get('id')  # Get the ID of the toddler to update
        if toddler_id:
            toddler_to_update = get_object_or_404(Toddler, id=toddler_id)
            if request.method == 'POST':
                # If the form is submitted, update the toddler's details
                toddler_to_update.first_name = request.POST.get("first_name", toddler_to_update.first_name)
                toddler_to_update.last_name = request.POST.get("last_name", toddler_to_update.last_name)
                toddler_to_update.ic_number = request.POST.get("ic_number", toddler_to_update.ic_number)
                toddler_to_update.contact_number = request.POST.get("contact_number", toddler_to_update.contact_number)
                toddler_to_update.address = request.POST.get("address", toddler_to_update.address)
                toddler_to_update.age = request.POST.get("age", toddler_to_update.age)
                toddler_to_update.gender = request.POST.get("gender", toddler_to_update.gender)

                try:
                    toddler_to_update.age = int(toddler_to_update.age)
                    if toddler_to_update.age <= 0:
                        messages.error(request, "Age must be a positive number.")
                        return redirect('admin_dashboard')  # Stay on the dashboard if error occurs
                except ValueError:
                    messages.error(request, "Invalid age provided.")
                    return redirect('admin_dashboard')  # Stay on the dashboard if error occurs

                toddler_to_update.save()
                messages.success(request, "Toddler details updated successfully!")
                return redirect('search_toddler')  # After update, redirect to the search page

    # Feedback Management (Search & List)
    feedback_query = request.GET.get('query', '').strip()
    feedback_list = Feedback.objects.all()
    if section == 'feedback' and feedback_query:
        feedback_list = feedback_list.filter(message__icontains=feedback_query)

    # Payment List Management (Just like feedback)
    payment_list = Payment.objects.all()  # Fetching all payments (you can add filters here if necessary)
    if section == 'payment_list':  # If the section is 'payment_list', you can filter by other criteria if needed
        # You can add payment filtering logic here if required (e.g., based on date or amount)
        pass

    # Passing all necessary data to the context
    context = {
        'title': 'Admin Dashboard',
        'section': section,  # Pass current section
        'total_toddlers': total_toddlers,
        'total_males': total_males,
        'total_females': total_females,
        'toddlers': toddlers,  # Search results if available
        'year': datetime.now().year,
        'search_query': query,  # Retain the search query
        'user_profile': user_profile,  # Include user_profile in context
        'toddler_to_update': toddler_to_update,  # Pass the toddler to update (if applicable)
        'feedback_list': feedback_list,
        'payment_list': payment_list,

         
       
    }

    return render(request, 'app/admin_dashboard.html', context)

def delete_toddler(request, toddler_id):
    toddler = get_object_or_404(Toddler, id=toddler_id)
    toddler.delete()
    messages.success(request, "Toddler record deleted successfully.")
# Preserve search query if it exists
    search_query = request.GET.get('toddler_ic', '')

    return redirect(f"/admin-dashboard/?section=search_toddler&toddler_ic={search_query}")  # Redirect to search page

# Contact view
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Dr. Yeoh.',
            'year': datetime.now().year,
        }
    )

# About view
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'ABC System',
            'message': 'This application processes ...',
            'year': datetime.now().year,
        }
    )

# Menu view
@login_required
def menu(request):
    """Renders the menu page."""
    is_employee = request.user.groups.filter(name='employee').exists()

    context = {
        'title': 'Main Menu',
        'is_employee': is_employee,
        'year': datetime.now().year,
    }
    context['user'] = request.user

    return render(request, 'app/menu.html', context)

# Sign-up view
def sign_up(request):
    """Handles user sign-up and user profile creation."""
    if request.method == 'POST':
        form = BootstrapSignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Ensure atomicity
                    # Create the User
                    user = form.save()
                    user_type = form.cleaned_data['user_type']
                    
                    # Create or update UserProfile
                    profile, created = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={'user_type': user_type}
                    )
                    
                    # If profile already exists, update the user_type
                    if not created:
                        profile.user_type = user_type
                        profile.save()
                
                # Redirect to login page
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please check your details and try again.')
    else:
        form = BootstrapSignUpForm()
    
    return render(request, 'app/sign_up.html', {'form': form})

# Add Toddler view
def add_toddler(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        ic_number = request.POST.get('ic_number')
        parent_name = request.POST.get("parent_name")
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # Ensure that all required fields are filled
        if not all([first_name, last_name, ic_number, contact_number, address, age, gender]):
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        # Validate the age field
        try:
            age = int(age)
            if age <= 0:
                return JsonResponse({'success': False, 'error': 'Age must be a positive integer'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Age must be a valid number'})

        # Check if a toddler with the same IC number already exists
        if Toddler.objects.filter(ic_number=ic_number).exists():
            return JsonResponse({'success': False, 'error': 'Toddler with this IC Number already exists'})

        try:
            # Try to create the toddler entry
            toddler = Toddler.objects.create(
                first_name=first_name,
                last_name=last_name,
                parent_name=parent_name,
                ic_number=ic_number,
                contact_number=contact_number,
                address=address,
                age=age,
                gender=gender
            )
            # Return success message after adding the toddler
            return JsonResponse({'success': True, 'message': 'Toddler added successfully!'})
        except Exception as e:
            # Handle any other errors
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

# Search Toddler view
def search_toddler(request):
    toddlers = None
    query = request.GET.get('toddler_ic', '').strip()  # Get query parameter
    if query:  # If a search query is provided
        toddlers = Toddler.objects.filter(ic_number__icontains=query)  # Search toddlers by IC number
    
    return render(request, 'app/search_toddler.html', {
        'toddlers': toddlers,  # Search results if any
        'search_query': query,  # Retain the search query in the template
        'title': 'Search Toddler',
    })

# View and Edit Toddler view (optional view for direct edit)
def view_edit_toddler(request, id):
    toddler = get_object_or_404(Toddler, id=id)

    if request.method == "POST":
        # Handle the form submission to edit the toddler's information
        toddler.first_name = request.POST.get("first_name", toddler.first_name)
        toddler.last_name = request.POST.get("last_name", toddler.last_name)
        toddler.ic_number = request.POST.get("ic_number", toddler.ic_number)
        toddler.contact_number = request.POST.get("contact_number", toddler.contact_number)
        toddler.address = request.POST.get("address", toddler.address)
        toddler.age = request.POST.get("age", toddler.age)
        toddler.gender = request.POST.get("gender", toddler.gender)
        
        # Validation example: Make sure age is an integer
        try:
            toddler.age = int(toddler.age)
            if toddler.age <= 0:
                messages.error(request, "Age must be a positive number.")
                return redirect('view_edit_toddler', id=toddler.id)
        except ValueError:
            messages.error(request, "Invalid age provided.")
            return redirect('view_edit_toddler', id=toddler.id)

        # Save the updated toddler info
        toddler.save()
        messages.success(request, "Toddler details updated successfully!")
        return redirect('search_toddler')  # Redirect to search page after update

    return render(request, 'app/view_edit_toddler.html', {
        'toddler': toddler,  # Pass toddler object to the template
        'title': f"Edit {toddler.first_name} {toddler.last_name}",
    })
# Add the update_toddler function
def update_toddler(request, id):
    toddler = get_object_or_404(Toddler, id=id)

    if request.method == "POST":
        toddler.first_name = request.POST.get("first_name", toddler.first_name)
        toddler.last_name = request.POST.get("last_name", toddler.last_name)
        toddler.ic_number = request.POST.get("ic_number", toddler.ic_number)
        toddler.contact_number = request.POST.get("contact_number", toddler.contact_number)
        toddler.address = request.POST.get("address", toddler.address)
        toddler.age = request.POST.get("age", toddler.age)
        toddler.gender = request.POST.get("gender", toddler.gender)
        
        try:
            toddler.age = int(toddler.age)
            if toddler.age <= 0:
                messages.error(request, "Age must be a positive number.")
                return redirect('admin_dashboard', id=toddler.id)
        except ValueError:
            messages.error(request, "Invalid age provided.")
            return redirect('update_toddler', id=toddler.id)

        toddler.save()
        messages.success(request, "Toddler details updated successfully!")
        return redirect('admin_dashboard')  # Redirect to search after update

    return render(request, 'app/update_toddler.html', {'toddler': toddler})

def toddler_payment(request):
    # Fetch all payments that are valid (i.e., paid and not overdue)
    valid_payments = Payment.objects.filter(status='Paid', due_date__gte=timezone.now().date())
    overdue_payments = Payment.objects.filter(status='Overdue', due_date__lt=timezone.now().date())

    return render(request, 'app/admin_dashboard.html', {
        'section': 'toddler_payment',  # This identifies the active section in the template
        'valid_payments': valid_payments,
        'overdue_payments': overdue_payments,
        'title': 'Toddler Payment',
    })

def payment_details(request, toddler_id):
    toddler = get_object_or_404(Toddler, id=toddler_id)
    payments = Payment.objects.filter(toddler=toddler)

    return render(request, 'app/payment_details.html', {
        'toddler': toddler,
        'payments': payments,
        'title': f"{toddler.first_name} {toddler.last_name} Payment History"
    })




# Parent Dashboard View
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'parent', login_url='home')
def parent_dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    # Get the section from the query parameter (default is 'dashboard')
    section = request.GET.get('section', 'dashboard')

    toddlers = Toddler.objects.all()  # This will fetch all toddlers

    context = {
        'user_profile': user_profile,
        'section': section,
        'toddlers': toddlers, 
    }

    return render(request, 'app/parent_dashboard.html', context)  # Fixed indentation

def parent_register(request):
    # Query the UserProfile model to get all parents
    parent_users = UserProfile.objects.filter(user_type='parent')
    return render(request, 'app/register_toddler.html', {'parents': parent_users})


def register_toddler(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        ic_number = request.POST.get('ic_number')
        parent_name = request.POST.get("parent_name")
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # Ensure that all required fields are filled
        if not all([first_name, last_name, ic_number, contact_number, address, age, gender]):
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        # Validate the age field
        try:
            age = int(age)
            if age <= 0:
                return JsonResponse({'success': False, 'error': 'Age must be a positive integer'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Age must be a valid number'})

        # Check if a toddler with the same IC number already exists
        if Toddler.objects.filter(ic_number=ic_number).exists():
            return JsonResponse({'success': False, 'error': 'Toddler with this IC Number already exists'})

        try:
            # Try to create the toddler entry
            toddler = Toddler.objects.create(
                first_name=first_name,
                last_name=last_name,
                parent_name=parent_name,
                ic_number=ic_number,
                contact_number=contact_number,
                address=address,
                age=age,
                gender=gender
            )
            # Return success message after adding the toddler
            return JsonResponse({'success': True, 'message': 'Toddler added successfully!'})
        except Exception as e:
            # Handle any other errors
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def choose_schedule(request):
    toddlers = Toddler.objects.all()  # Fetch all toddlers

    if request.method == 'POST':
        toddler_full_name = request.POST.get('toddler_full_name')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        activity_name = request.POST.get('activity_name')

        # Check if all fields are provided
        if not all([toddler_full_name, date, start_time, end_time, activity_name]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})

        try:
            # Get the toddler object, ensuring it exists
            toddler = Toddler.objects.get(full_name=toddler_full_name)

            # Create the schedule
            schedule = Schedule.objects.create(
                toddler=toddler,
                date=date,
                start_time=start_time,
                end_time=end_time,
                activity_name=activity_name
            )

            return JsonResponse({'success': True, 'message': 'Schedule created successfully!'})

        except Toddler.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Toddler not found.'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'})

    context = {
        'toddlers': toddlers,
    }
    return render(request, 'app/choose_schedule.html', context)

def get_toddlers(request):
    # Fetch only the 'full_name' field for the frontend
    toddlers = Toddler.objects.all().values('full_name')
    return JsonResponse({'toddlers': list(toddlers)})

@login_required
def make_payment(request):
    toddlers = Toddler.objects.all()  # Fetch all toddlers for the dropdown

    if request.method == 'POST':
        # Extract fields from POST request
        toddler_full_name = request.POST.get('toddler_full_name')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        bank = request.POST.get('bank') if payment_method == 'fpx' else None
        card_type = request.POST.get('card_type') if payment_method == 'card' else None
        reference = request.POST.get('reference')

        # Ensure all required fields are provided
        if not all([toddler_full_name, amount, payment_method, reference]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})

        try:
            # Get the toddler instance
            toddler = Toddler.objects.get(full_name=toddler_full_name)

            # Create a new Payment instance
            payment = Payment.objects.create(
                toddler=toddler,
                amount=amount,
                payment_method=payment_method,
                bank=bank,
                card_info=card_type,  # Assuming 'card_info' is the field in Payment model
                reference=reference,
            )

            return JsonResponse({'success': True, 'message': 'Payment submitted successfully!'})

        except Toddler.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Toddler not found.'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'})

    return render(request, 'app/make_payment.html', {'toddlers': toddlers})

def submit_feedback(request):
    if request.method == "POST":
        # Extracting data from the form
        toddler_name = request.POST.get('toddler_full_name')
        recipient = request.POST.get('recipient')
        feedback_message = request.POST.get('feedback')

        # Fetch the toddler instance from the database
        toddler = Toddler.objects.get(full_name=toddler_name)

        # Save the feedback
        Feedback.objects.create(
            toddler=toddler,
            recipient=recipient,
            message=feedback_message
        )

        # Optional: Respond with a success message or redirect to a confirmation page
        return JsonResponse({"message": "Feedback submitted successfully!"})

    # If not POST request, render the feedback form
    toddlers = Toddler.objects.all()
    return render(request, 'feedback_form.html', {'toddlers': toddlers})


def feedback_list(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'app/feedback_list.html', {'feedback_list': feedback_list})


@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'admin', login_url='home')
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        reply_message = request.POST.get('reply_message')
        feedback.reply = reply_message  # Assuming 'reply' field exists in Feedback model
        feedback.save()
        messages.success(request, "Reply sent successfully!")
        return redirect(f"{reverse('admin_dashboard')}?section=feedback")  # Redirect to feedback section

    return render(request, 'app/reply_feedback.html', {'feedback': feedback})

def payment_list(request):
    # Fetch all payments, adjust as per your needs
    payment_list = Payment.objects.all()

    # Pass the payment list to the template
    return render(request, 'payment_list.html', {
        'payment_list': payment_list,
        'section': 'toddler_payment',  # This will ensure that the payment section is selected
    })

@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='home')
def teacher_dashboard(request):
    toddlers = Toddler.objects.all()  # Get all toddlers for the "Create Schedule" dropdown
    schedules = Schedule.objects.all()  # Get all activities for the "View Schedule" table
    form = ScheduleForm()  # Ensure form is always initialized
    success_message = None  # Add this variable to handle success messages

    # Handle the "Create Schedule" form
    if request.method == 'POST' and 'create_schedule' in request.POST:
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Schedule created successfully!"  # Set the success message
        else:
            return JsonResponse({"success": False, "message": "Error creating schedule."})  # Return error if form is invalid

    # Handle the "Search" for View Schedule
    selected_toddler = None
    if request.method == 'GET' and 'search_toddler' in request.GET:
        toddler_name = request.GET.get('toddler_name')
        selected_toddler = Toddler.objects.filter(full_name__icontains=toddler_name)

    # Handle section switching
    section = request.GET.get('section', 'dashboard')  

    # Fetch feedback **only if** in the "feedback" section
    feedback_list = Feedback.objects.all() if section == 'feedback' else None

    

    return render(request, 'app/teacher_dashboard.html', {
        'toddlers': toddlers,
        'schedules': schedules,
        'form': form,
        'selected_toddler': selected_toddler,
        'success_message': success_message,  # Pass success message to the template
        'feedback_list': feedback_list,  # Pass feedback list to the template
        'section': section,  # Ensure section is passed to the template
    })

 
def manage_schedule_activity(request):
    toddlers = Toddler.objects.all()  # Get all toddlers
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # Assign the current teacher as the creator of the schedule activity
            schedule_activity = form.save(commit=False)
            schedule_activity.created_by = request.user.userprofile  # Assuming the teacher's userprofile is linked
            schedule_activity.save()  # Save it to the Schedule model instead
            return redirect('manage_schedule_activity')  # Redirect to the same page after saving
    else:
        form = ScheduleForm()

    context = {
        'form': form,
        'toddlers': toddlers  # Pass the toddlers to the template
    }
    return render(request, 'app/teacher_dashboard.html', context)

 
def get_toddlers(request):
    toddlers = Toddler.objects.all()
    toddler_list = [{'id': toddler.id, 'full_name': toddler.full_name} for toddler in toddlers]
    return JsonResponse({'toddlers': toddler_list})
 
def view_schedule(request):
    toddler_id = request.GET.get('toddler_id')
    if not toddler_id:
        return JsonResponse({"error": "Missing toddler_id"}, status=400)

    schedules = Schedule.objects.filter(toddler_id=toddler_id).values("activity_name", "date", "start_time", "end_time")
    return JsonResponse({"schedules": list(schedules)})
 
def manage_attendance(request):
    toddlers = Toddler.objects.all()
 
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
   
    return render(request, 'app/manage_attendance.html', {'toddlers': toddlers})
 
def get_attendance_records(request):
    toddler_id = request.GET.get('toddler_id')
    print("Fetching records for Toddler ID:", toddler_id)  # Debugging
    if toddler_id:
        records = Attendance.objects.filter(toddler_id=toddler_id).values('date', 'status')
        return JsonResponse({'attendance': list(records)})
    return JsonResponse({'attendance': []})
 

def save_attendance(request):
    if request.method == "POST":
        
        toddler_id = request.POST.get("toddler")
        date = request.POST.get("date")
        status = request.POST.get("status")

        print(f"Received Data - Toddler ID: {toddler_id}, Date: {date}, Status: {status}")  # Debugging log

        if not toddler_id or not date or not status:
            return JsonResponse({"success": False, "message": "Missing required fields!"})

        try:
            toddler = Toddler.objects.get(id=toddler_id)
            attendance = Attendance.objects.create(toddler=toddler, date=date, status=status)
            print(f"Saved Attendance: {attendance.toddler.id} | {attendance.date} | {attendance.status}")  # Debug log
            return JsonResponse({"success": True, "message": "Attendance saved successfully!"})
        except Toddler.DoesNotExist:
            return JsonResponse({"success": False, "message": "Toddler not found!"})
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug log
            return JsonResponse({"success": False, "message": str(e)})
    
    return JsonResponse({"success": False, "message": "Invalid request!"})


def manage_performance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("Received JSON:", data)  # ✅ Debugging

            toddler_id = data.get("toddler_id")
            activity = data.get("activity")
            rating = int(data.get("rating", 0))

            if not toddler_id or rating not in range(1, 6):
                print("Invalid data received")
                return JsonResponse({"success": False, "message": "Invalid data received."}, status=400)

            toddler = Toddler.objects.filter(id=toddler_id).first()
            if not toddler:
                print("Toddler not found")
                return JsonResponse({"success": False, "message": "Toddler not found."}, status=404)

            # Save rating
            PerformanceRating.objects.create(toddler=toddler, activity=activity, rating=rating)

            return JsonResponse({"success": True, "message": "Performance rating submitted successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


@login_required
def create_schedule(request):
    # Fetch all toddlers
    toddlers = Toddler.objects.all()

    if request.method == 'POST':
        # Debugging: print out all POST data to check the received data
        print(request.POST)

        toddler_id = request.POST.get('toddler_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        activity_name = request.POST.get('activity_name')

        # Check if all fields are provided
        if not toddler_id or not date or not start_time or not end_time or not activity_name:
            return JsonResponse({'success': False, 'error': 'Missing data!'})
        try:
            # Get the toddler object, ensuring it exists
            toddler = Toddler.objects.get(id=toddler_id)

            # Create the schedule for the toddler
            schedule = Schedule.objects.create(
                toddler=toddler,
                date=date,
                start_time=start_time,
                end_time=end_time,
                activity_name=activity_name
            )

            return JsonResponse({'success': True, 'message': 'Schedule created successfully!'})

        except Toddler.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Toddler not found.'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'})

    context = {
        'toddlers': toddlers,
    }
    return render(request, 'app/manage_schedule_and_activity.html', context)


