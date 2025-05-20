from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('export/', views.export_customers_csv, name='export_customers_csv'),
    path('import/', views.import_customers_csv, name='import_customers_csv'),
    path('send-mass-email/', views.send_mass_email, name='send_mass_email'),

]
