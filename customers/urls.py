from django.urls import path
from . import views


urlpatterns = [
    path('', views.customers, name='customers'),
    path('<int:id>/', views.customer_detail, name='customer_detail'),
    path('add/', views.add_customer, name='add_customer'),
    path('<int:id>/edit/', views.edit_customer, name='edit_customer'),
    path('<int:id>/delete/', views.delete_customer, name='delete_customer'),
]
