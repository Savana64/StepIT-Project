from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone
from .models import Bus, Driver, Reservation

class BusListView(View):
    def get(self, request):
        busses = Bus.objects.filter(ready=True)
        return render(request, 'bus_list.html', {'busses':busses})

class DriverCeduleView(View):
    def get(self,request):
        drivers = Driver.objects.all()
        return(request, 'driver_cedule.html', {'drivers': drivers})

class ReserveCreateView(View):
    def post(self, request, bus_id):
        bus = get_object_or_404(Bus, pk=bus_id)
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, pk=driver_id)
        if not bus.ready:
            return render(request, 'error.html', {'message': 'Bus v servise.'})
        if not driver.daily_break():
            return render(request, 'error.html', {'message': 'Řidič potřebuje spát.'})
        if driver.needs_rest():
            return render(request,'error.html', {'message': 'Řidič potřebuje volno.'})
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=8)
        reservation = Reservation.objects.create(bus=bus, driver=driver, start_time=start_time, end_time=end_time) 
        driver.last_rest_start = end_time + timedelta(hours=11)
        driver.last_drive_date = start_time
        driver.save()
        return render(request, 'reservation_success.html', {'reservation': reservation})

# Create your views here.
