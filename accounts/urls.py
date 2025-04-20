from django.urls import path 
from django.contrib.auth import views as auth_views 
from . import views 

urlpatterns = [
    path('register-customer/', views.register_customer, name='register-customer'),
    path('activate-account/<uidb64>/<token>/', views.activate_account, name='activate-account'), 
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('change-password/', views.change_password, name='change-password'), 
    path('update-profile/', views.update_profile, name='update-profile'),  

    # links for password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'), 
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete')
]