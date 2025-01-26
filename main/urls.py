from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

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

    path('tickets/', views.tickets, name='tickets'),
    path('tickets/add/', views.add_ticket, name='add_ticket'),
    path('tickets/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('sales/', views.sales, name='sales'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/<int:sale_id>/edit/', views.edit_sale, name='edit_sale'),
    path('sales/<int:sale_id>/delete/', views.delete_sale, name='delete_sale'),
    path('sales/<int:sale_id>/', views.sale_detail, name='sale_detail'),

    path('report/', views.sales_report, name='report'),
    path('staff-report/', views.staff_report, name='staff-report'),
    path('movies-report/', views.movies_report, name='movies-report'),

    path('get_rows/', views.get_rows),

    path('exported-reports/', views.exported_reports, name='exported-reports'),
    path('download-report/<str:filename>', views.download_report, name='download-report'),
]
