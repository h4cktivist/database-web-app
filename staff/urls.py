from django.urls import path
from . import views


urlpatterns = [
    path('positions/', views.positions, name='positions'),
    path('positions/add/', views.add_position, name='add_position'),
    path('positions/<int:position_id>/edit/', views.edit_position, name='edit_position'),
    path('positions/<int:position_id>/delete/', views.delete_position, name='delete_position'),
    path('positions/<int:position_id>/', views.position_detail, name='position_detail'),

    path('', views.staff, name='staff'),
    path('add/', views.add_staff, name='add_staff'),
    path('<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),
    path('<int:staff_id>/', views.staff_detail, name='staff_detail'),
]
