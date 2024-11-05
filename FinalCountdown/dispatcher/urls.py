from django.urls import path
from . import views

app_name = 'výpravčí'
urlpatterns = [
    path('buses/', views.BusListView.as_view(), name='bus_list'),
    path("drivers/", views.DriverCeduleView.as_view(), name='driver_schedule'),
    path('reserve/<int:bus_id>/', views.ReserveCreateView.as_view, name='create_reservation')
]