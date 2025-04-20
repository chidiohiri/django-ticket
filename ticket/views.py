from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Ticket, TicketAttachment, TicketNote
from . import form as fm 
from payment.models import Wallet
from .filters import CustomerTicketFilter, TicketQueueFilter, EngineerTicketFilter

User = get_user_model()

# create ticket and charge customer wallet
@login_required
def create_ticket(request):
    if not request.user.is_customer:
        messages.warning(request, 'Permission denied. Only customers can create tickets')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = fm.CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            
            # get user's wallet 
            wallet  = Wallet.objects.get(user=request.user)
            if not wallet.balance >= var.amount_paid:
                messages.warning(request, 'Insufficent funds in wallet. Please top up.')
                return redirect('initialize-payment')
            wallet.balance = wallet.balance - var.amount_paid
            
            var.save()
            wallet.save()

            if var.priority == 'Critical':
                send_mail(
                'ACTION REQUIRED: Critical ticket received', 
                f'Please immediately review the critical ticket before as it impacts performace. Ticket info: {var.title}', 
                'noreply@email.com', 
                ['admin@email.com'], 
                fail_silently=False
                )

            send_mail(
                'TICKET RECEIVED CONFIRMATION', 
                f'Hi {var.created_by.first_name}, we have received your ticket and we would be in touch soon. You were charged {var.amount_paid} NGN (from your wallet) for this ticket', 
                'noreply@email.com', 
                [var.created_by.email], 
                fail_silently=False
            )
            
            messages.success(request, 'Ticket created. We will get in touch with you shortly')
            return redirect('my-tickets')
        else:
            messages.warning(request, 'Something went wrong. Please check form inputs')
            return redirect('create-ticket')
    else:
        form = fm.CreateTicketForm()
        context = {'form':form}
    return render(request, 'ticket/create_ticket.html', context)

# update ticket, if not resolved
@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to edit this ticket')
        return redirect('dashboard')

    if ticket.is_resolved:
        messages.warning(request, 'You cannot update ticket because it is marked as resolved')
        return redirect('ticket-details', ticket.pk)
    
    if request.method == 'POST':
        form = fm.UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket information has been updated and saved')
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('update-ticket', ticket.pk)
    else:
        form = fm.UpdateTicketForm(instance=ticket)
        context = {'form':form, 'ticket':ticket}
    
    return render(request, 'ticket/update_ticket.html', context)

# delete ticket, if pending 
@login_required
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to delete this ticket')
        return redirect('dashboard')

    if not ticket.status == 'Pending':
        messages.warning(request, 'You cannot delete ticket. It has pass the pending state')
        return redirect('ticket-details', ticket.pk)
    
    ticket.delete()
    messages.success(request, 'Ticket has been successfully deleted')
    return redirect('all-tickets')

# ticket details 
@login_required
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    notes = ticket.ticketnote_set.all().order_by('-created_on')
    uploads = ticket.attachments.all()

    # paginator
    paginator = Paginator(notes, 7)  # Show 7 notes per page
    page_number = request.GET.get('page')
    ticket_notes = paginator.get_page(page_number)

    context = {'ticket':ticket, 'ticket_notes':ticket_notes, 'uploads':uploads}
    return render(request, 'ticket/ticket_details.html', context)

# ticket queue, pagination, filtering
@login_required
def ticket_queue(request):
    tickets = Ticket.objects.filter(status='Pending').order_by('-created_on')

    # apply filter
    tickets_filter = TicketQueueFilter(request.GET, queryset=tickets)
    filtered_tickets = tickets_filter.qs

    # pagination
    paginator = Paginator(filtered_tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tickets':page_obj, 'filter':tickets_filter}

    return render(request, 'ticket/ticket_queue.html', context)

# change priority level, send email to admin once set to critical 
@login_required
def change_priority(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to change priority of this ticket')
        return redirect('dashboard')

    if ticket.is_resolved:
        messages.warning(request, 'Cannot change priority because ticket is resolved')
        return redirect('ticket-details', ticket.pk)

    if request.method == 'POST':
        form = fm.UpdateTicketPriority(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save()
            if var.priority == 'Critical':
                send_mail(
                'ACTION REQUIRED: Critical ticket received', 
                f'Please immediately review the critical ticket before as it impacts performace. Ticket info: {ticket.title}', 
                'noreply@email.com', 
                ['admin@email.com'], 
                fail_silently=False
                )
            messages.success(request, 'Ticket priority level has been updated')
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check form inputs')
            return redirect('ticket-details', ticket.pk)
    else:
        form = fm.UpdateTicketPriority(instance=ticket)
        context = {'form':form, 'ticket':ticket}
    
    return render(request, 'ticket/change_priority.html', context)

# my tickets, for customer, pagination, filtering, export csv 
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_on', 'status')

    # apply filter
    tickets_filter = CustomerTicketFilter(request.GET, queryset=tickets)
    filtered_tickets = tickets_filter.qs

    # pagination
    paginator = Paginator(filtered_tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tickets':page_obj, 'filter':tickets_filter}

    return render(request, 'ticket/my_tickets.html', context)

# tickets per engineer, pagination, filtering
@login_required
def engineer_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-created_on', 'status')

    # apply filter
    tickets_filter = EngineerTicketFilter(request.GET, queryset=tickets)
    filtered_tickets = tickets_filter.qs

    # pagination
    paginator = Paginator(filtered_tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tickets':page_obj, 'filter':tickets_filter}

    return render(request, 'ticket/engineer_tickets.html', context)

# add ticket notes
@login_required
def add_ticket_note(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    
    if ticket.is_resolved or ticket.status == 'Pending':
        messages.warning(request, 'You cannot add ticket note, because ticket is resolved or pending')
        return redirect('ticket-details', ticket.pk)

    if request.method == 'POST':
        note = request.POST.get('note')

        TicketNote.objects.create(
            ticket=ticket, note=note, created_by=request.user
        )

        messages.success(request, 'Note added to ticket for reference')
        return redirect('ticket-details', ticket.pk)
    

# resolve ticket, send email to customer
@login_required
def resolve_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.assigned_to == request.user:
        messages.warning(request, 'You do not have permissions to resolve this ticket')
        return redirect('dashboard')

    if request.method == 'POST':
        form = fm.ResolveTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_resolved = True
            var.status = 'Resolved'
            var.save()
            messages.success(request, 'Ticket marked as resolved and closed')

            send_mail(
                'TICKET RESOLVED', 
                f'Hi, {ticket.created_by.first_name}, Your ticket {ticket.title} has been marked as resolved. You can still reopen this ticket from your portal', 
                'noreply@email.com', 
                [ticket.created_by.email], 
                fail_silently=False
                )
            
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('resolve-ticket', ticket.pk)
    else:
        form = fm.ResolveTicketForm(instance=ticket)
        context = {'form':form, 'ticket':ticket}

    return render(request, 'ticket/resolve_ticket.html', context)

# assign ticket to engineer 
@login_required
def assign_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if request.method == 'POST':
        form = fm.AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.status = 'Active'
            var.save()

            messages.success(request, 'Ticket has been assigned to support engineer')
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check form inputs')
            return redirect('assign-ticket', ticket.pk)
    else:
        form = fm.AssignTicketForm(instance=ticket)
        form.fields['assigned_to'].queryset = User.objects.filter(is_support_engineer=True)
        context = {'form':form, 'ticket':ticket}

    return render(request, 'ticket/assign_ticket.html', context)

# customer/engineer can reopen ticket
@login_required
def reopen_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to reopen this ticket')
        return redirect('dashboard')

    if not ticket.is_resolved:
        messages.warning(request, 'Cannot reopen ticket because it has not been closed yet')
        return redirect('ticket-details', ticket.pk)
    
    ticket.status = 'Active'
    ticket.is_resolved = False
    ticket.save()

    messages.success(request, 'Ticket has been reopened.')
    return redirect('ticket-details', pk)

# customer can provide feedback on a ticket, 1 star sends email to admin
@login_required
def ticket_feedback(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to give feedback on this ticket')
        return redirect('dashboard')

    if ticket.has_feedback:
        messages.warning(request, 'Ticket already has fedback')
        return redirect('ticket-details', ticket.pk)

    if request.method == 'POST':
        form = fm.TicketFeedbackForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.ticket = ticket
            ticket.has_feedback = True
            var.save()
            ticket.save()
            messages.success(request, 'Feedback sent to Support team')
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check form inputs')
            return redirect('ticket-feedback', ticket.pk)
    else:
        form = fm.TicketFeedbackForm()
        context = {'form':form, 'ticket':ticket}
    
    return render(request, 'ticket/ticket_feedback.html', context)

# dynamic searching, only show customer tickets created by them and engineer everything 
@login_required
def search_ticket(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        results = Ticket.objects.filter(title__icontains=query)

        context = {'query':query, 'results':results}

        return render(request, 'ticket/search_ticket.html', context)
    
# super user can see all tickets from the admin panel 

# attach files to ticket 
@login_required
def attach_file(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.created_by == request.user:
        messages.warning(request, 'You do not have permissions to attach file to this ticket')
        return redirect('dashboard')

    if ticket.is_resolved:
        messages.warning(request, 'Cannot upload attachments because ticket is resolved')
        return redirect('ticket-details', ticket.pk)

    if request.method == 'POST':
        form = fm.TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.ticket = ticket
            attachment.user = request.user
            attachment.save()
            messages.success(request, 'Files have now been uploaded to the ticket')
            return redirect('ticket-details', ticket.pk)
        else:
            messages.warning(request, 'Something went wrong. Please check uploads')
            return redirect('attach-file', ticket.pk)
    else:
        form = fm.TicketAttachmentForm()
        context = {'form':form, 'ticket':ticket}

    return render(request, 'ticket/attach_file.html', context)

