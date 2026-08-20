from django.contrib import admin
from django.urls import path
from app import views as main_views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Main app routes
    path('', main_views.home, name='home'),
    path('contact/', main_views.contact, name='contact'),
    path('about/', main_views.about, name='about'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='app/index.html'), name='logout'),  # Fixed trailing slash
    path('menu/', main_views.menu, name='menu'),
    path('index/', main_views.menu, name='index'),


    
    # Additional routes
    path('sign-up/', main_views.sign_up, name='sign_up'),
    path('admin-dashboard/', main_views.admin_dashboard, name='admin_dashboard'),
    path('add-toddler/',main_views.add_toddler, name='add_toddler'),
    path('search-toddler/', main_views.search_toddler, name='search_toddler'),
    path('view-edit-toddler/<int:id>/', main_views.view_edit_toddler, name='view_edit_toddler'),
    path('update-toddler/<int:id>/', main_views.update_toddler, name='update_toddler'),
    path('toddler-payment/', main_views.toddler_payment, name='toddler_payment'),
    path('payment-details/<int:toddler_id>/', main_views.payment_details, name='payment_details'),
    path('feedback-list/', main_views.feedback_list, name='feedback_list'),
    path('feedback/reply/<int:feedback_id>/', main_views.reply_feedback, name='reply_feedback'),
    path('payment-list/', main_views.payment_list, name='payment_list'),
    path('delete_toddler/<int:toddler_id>/', main_views.delete_toddler, name='delete_toddler'),


    #Teacher view
    path('teacher-dashboard/', main_views.teacher_dashboard, name='teacher_dashboard'),
    path('create_schedule/', main_views.create_schedule, name='create_schedule'),
    path('get_toddlers/', main_views.get_toddlers, name='get_toddlers'),
    path('view_schedule/', main_views.view_schedule, name='view_schedule'),
    path('manage-attendance/', main_views.manage_attendance, name='manage_attendance'),
    path('get_attendance_records/', main_views.get_attendance_records, name='get_attendance_records'),
    path('save_attendance/', main_views.save_attendance, name='save_attendance'),
    path('manage_performance/', main_views.manage_performance, name='manage_performance'),
   

    # Parent route
    path('parent-dashboard/', main_views.parent_dashboard, name='parent_dashboard'),
    path('register-toddler/', main_views.register_toddler, name='register_toddler'),
    path('choose-schedule/', main_views.choose_schedule, name='choose_schedule'),
    path('get-toddlers/', main_views.get_toddlers, name='get_toddlers'),
    path('make-payment/', main_views.make_payment, name='make_payment'),
    path('submit-feedback/', main_views.submit_feedback, name='submit_feedback'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
