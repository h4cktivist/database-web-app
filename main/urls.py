from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

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
