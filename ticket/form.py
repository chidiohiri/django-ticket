from django import forms 
from .models import Ticket, TicketAttachment, TicketFeedback

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket 
        fields = ['title', 'description', 'priority']

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket 
        fields = ['title', 'description']

class UpdateTicketPriority(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['priority']

class ResolveTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['resolution_summary']

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to']

class TicketFeedbackForm(forms.ModelForm):
    class Meta:
        model = TicketFeedback
        fields = ['ratings', 'comment']

class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']