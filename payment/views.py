import requests
import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Wallet, Payment
from .filters import PaymentFilter

User = get_user_model()

# generate reference
def generate_reference():
    return str(uuid.uuid4()).replace('-', '')[:12]

# initialize payment
@login_required
def initialize_payment(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')

        amount = int(total_amount) * 100 # convert to kobo
        email = request.user.email
        reference = generate_reference()

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}', 
            'Content-Type': 'application/json',
        }

        data = {
            'email':email, 'amount':amount, 'reference':reference, 
            'callback_url': request.build_absolute_uri(reverse('verify-payment', args=[reference])),
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)

        response_data = response.json()

        if response_data.get('status'):
            Payment.objects.create(
                user=request.user, amount=amount/100, reference=reference, email=email
            )
            return redirect(response_data['data']['authorization_url'])
        else:
            messages.warning(request, 'Payment initialization failed. Please try again')
            return redirect('dashboard')
    
    return render(request, 'payment/initialize_payment.html')

# verify payment
@login_required
def verify_payment(request, reference):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
    }

    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)

    response_data = response.json()

    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        messages.warning(request, 'Payment not found')
        return redirect('dashboard')
    
    if response_data.get('status') and response_data.get('data', {}).get('status') == 'success':
        if not payment.verified:
            payment.verified = True
            payment.save()

            # fund wallet
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance = wallet.balance + payment.amount
            wallet.save()
            messages.success(request, 'Congratulations, your payment was successful!')
            return redirect('all-invoices')
        
    messages.warning(request, 'Payment verification failed')
    return redirect('dashboard')

# all invoices
@login_required
def all_invoices(request):
    invoices = Payment.objects.filter(verified=True, user=request.user).order_by('-timestamp')

    # apply filter 
    invoice_filter = PaymentFilter(request.GET, queryset=invoices)
    filtered_invoices = invoice_filter.qs

    # pagination
    paginator = Paginator(filtered_invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'invoices':page_obj, 'filter':invoice_filter}
    return render(request, 'payment/all_invoices.html', context)

