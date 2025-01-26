from django.urls import path
from . import views


urlpatterns = [
    path('', views.halls, name='halls'),
    path('<int:id>/', views.hall_detail, name='hall_detail'),
    path('add/', views.add_hall, name='add_hall'),
    path('<int:id>/edit/', views.edit_hall, name='edit_hall'),
    path('<int:id>/delete/', views.delete_hall, name='delete_hall'),
]