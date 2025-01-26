from django.urls import path
from . import views


urlpatterns = [
    path('', views.tickets, name='tickets'),
    path('add/', views.add_ticket, name='add_ticket'),
    path('<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('session_types/', views.session_types, name='session_types'),
    path('session_types/add/', views.add_session_type, name='add_session_type'),
    path('session_types/<int:session_type_id>/edit/', views.edit_session_type, name='edit_session_type'),
    path('session_types/<int:session_type_id>/delete/', views.delete_session_type, name='delete_session_type'),
    path('session_types/<int:session_type_id>/', views.session_type_detail, name='session_type_detail'),

    path('sessions/', views.sessions, name='sessions'),
    path('sessions/add/', views.add_session, name='add_session'),
    path('sessions/<int:session_id>/edit/', views.edit_session, name='edit_session'),
    path('sessions/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
]
