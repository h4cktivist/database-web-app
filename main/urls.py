from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('customers/<int:id>/', views.customer_detail, name='customer_detail'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:id>/delete/', views.delete_customer, name='delete_customer'),

    path('halls/', views.halls, name='halls'),
    path('halls/<int:id>/', views.hall_detail, name='hall_detail'),
    path('halls/add/', views.add_hall, name='add_hall'),
    path('halls/<int:id>/edit/', views.edit_hall, name='edit_hall'),
    path('halls/<int:id>/delete/', views.delete_hall, name='delete_hall'),

    path('movies/', views.movies, name='movies'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),

    path('positions/', views.positions, name='positions'),
    path('positions/add/', views.add_position, name='add_position'),
    path('positions/<int:position_id>/edit/', views.edit_position, name='edit_position'),
    path('positions/<int:position_id>/delete/', views.delete_position, name='delete_position'),
    path('positions/<int:position_id>/', views.position_detail, name='position_detail'),

    path('session_types/', views.session_types, name='session_types'),
    path('session_types/add/', views.add_session_type, name='add_session_type'),
    path('session_types/<int:session_type_id>/edit/', views.edit_session_type, name='edit_session_type'),
    path('session_types/<int:session_type_id>/delete/', views.delete_session_type, name='delete_session_type'),
    path('session_types/<int:session_type_id>/', views.session_type_detail, name='session_type_detail'),

    path('staff/', views.staff, name='staff'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),

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

    path('report/', views.report, name='report'),
]
