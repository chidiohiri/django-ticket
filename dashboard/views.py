from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ticket.models import Ticket
from django.db.models.functions import TruncMonth
from django.db.models import Count

@login_required
def dashboard(request):
    if request.user.is_customer:
        return render(request, 'dashboard/customer_dashboard.html')
    elif request.user.is_support_engineer:
        return render(request, 'dashboard/engineer_dashboard.html')
    
