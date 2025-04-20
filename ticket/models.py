from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='engineers')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15, 
        choices=(
            ('Pending', 'Pending'), 
            ('Active', 'Active'), 
            ('Resolved', 'Resolved')
        ),
        default='Pending'
    )
    priority = models.CharField(
        max_length=15, 
        choices=(
            ('Low', 'Low'), 
            ('High', 'High'), 
            ('Critical', 'Critical'),  
        ),
        default='Low'
    )
    is_resolved = models.BooleanField(default=False)
    resolution_summary = models.CharField(max_length=400, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=500)
    has_feedback = models.BooleanField(default=False)

class TicketNote(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    note = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TicketFeedback(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    ratings = models.CharField(
        max_length=15, 
        choices=(
            ('Excellent', 'Excellent'), 
            ('Average', 'Average'), 
            ('Terrible', 'Terrible')
        )
    )
    comment = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


