from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from . import form as fm
from payment.models import Wallet

User = get_user_model()

# generate activation link 
def generate_activation_link(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return request.build_absolute_uri(f'/accounts/activate-account/{uid}/{token}')

# register customer
def register_customer(request):
    if request.method == 'POST':
        form = fm.RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.username = var.email
            var.is_customer = True 
            var.is_active = False
            var.save()

            # create wallet 
            Wallet.objects.create(user=var)

            # send activation link 
            activation_link = generate_activation_link(var, request)
            send_mail(
                'ACTION REQUIRED: Activate your account', 
                f'Click the link below to activate your account: {activation_link}', 
                'noreply@email.com', 
                [var.email], 
                fail_silently=False
            )
            
            messages.success(request, 'Activation link sent your email')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong.')
            return redirect('register-customer')
    else:
        form = fm.RegisterUserForm()
        context = {'form':form}
    
    return render(request, 'accounts/register_customer.html', context)

# activate account 
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated.')
        return redirect('login')
    else:
        messages.warning(request, 'Invalid activation link')
        return redirect('register-customer')

# login user 
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next')  # Get the 'next' parameter

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f'Welcome! You are logged in as {user.first_name}')

            # Redirect to 'next' if available, otherwise go to dashboard
            return redirect(next_url if next_url else 'dashboard')
        else:
            messages.warning(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'accounts/login.html')


# logout user 
def logout_user(request):
    logout(request)
    messages.success(request, 'Session ended. Log in to continue')
    return redirect('login')

# change password 
@login_required
def change_password(request):
    if request.method == 'POST':
        form = fm.UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            var = form.save()
            update_session_auth_hash(request, var)
            messages.success(request, 'Your password has been updated and secured')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form inputs')
            return redirect('change-password')
    else:
        form = fm.UserPasswordChangeForm(request.user)
        context = {'form':form}
    
    return render(request, 'accounts/change_password.html', context)

# update profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = fm.UpdateUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile information updated')
            return redirect('update-profile')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('update-profile')
    else:
        form = fm.UpdateUserProfileForm(instance=request.user)
        context = {'form':form}
    
    return render(request, 'accounts/update_profile.html', context)

# reset password 
