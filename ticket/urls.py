from django.urls import path 
from . import views 

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create-ticket'), 
    path('update-ticket/<int:pk>/', views.update_ticket, name='update-ticket'), 
    path('delete-ticket/<int:pk>/', views.delete_ticket, name='delete-ticket'), 
    path('ticket-details/<int:pk>/', views.ticket_details, name='ticket-details'), 
    path('ticket-queue/', views.ticket_queue, name='ticket-queue'), 
    path('change-priority/<int:pk>/', views.change_priority, name='change-priority'), 
    path('my-tickets/', views.my_tickets, name='my-tickets'), 
    path('engineer-tickets/', views.engineer_tickets, name='engineer-tickets'), 
    path('add-ticket-note/<int:pk>/', views.add_ticket_note, name='add-ticket-note'), 
    path('resolve-ticket/<int:pk>/', views.resolve_ticket, name='resolve-ticket'), 
    path('assign-ticket/<int:pk>/', views.assign_ticket, name='assign-ticket'), 
    path('reopen-ticket/<int:pk>/', views.reopen_ticket, name='reopen-ticket'), 
    path('ticket-feedback/<int:pk>/', views.ticket_feedback, name='ticket-feedback'), 
    path('search-ticket/', views.search_ticket, name='search-ticket'), 
    path('attach-file/<int:pk>/', views.attach_file, name='attach-file')
]