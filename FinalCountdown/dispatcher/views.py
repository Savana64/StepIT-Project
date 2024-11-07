from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils import timezone
from .models import Bus, Driver, Reservation

class BusListView(View):
    def get(self, request):
        buses = Bus.objects.filter(ready=True)
        return render(request, 'dispatcher/bus_list.html', {'buses': buses})

class DriverCeduleView(View):
    def get(self,request):
        drivers = Driver.objects.all()
        return render(request, 'dispatcher/driver_cedule.html', {'drivers': drivers})

class ReserveCreateView(View):
    def post(self, request, bus_id):
        bus = get_object_or_404(Bus, pk=bus_id)
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, pk=driver_id)
        if not bus.ready:
            return render(request, 'dispatcher/error.html', {'message': 'Bus v servise.'})
        if not driver.daily_break():
            return render(request, 'dispatcher/error.html', {'message': 'Řidič potřebuje spát.'})
        if driver.needs_rest():
            return render(request,'dispatcher/error.html', {'message': 'Řidič potřebuje volno.'})
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=12)
        reservation = Reservation.objects.create(bus=bus, driver=driver, start_time=start_time, end_time=end_time) 
        driver.last_rest_start = end_time + timedelta(hours=11)
        driver.last_drive_date = start_time + timedelta(days=6)
        driver.save()
        return render(request, 'dispatcher/reservation_success.html', {'reservation': reservation})
    
def index(request):
    latest_question_list = Reservation.objects.order_by('start_time') [:10]   

def error(request):
    return render(request, 'dispatcher/error.html')

# Create your views here.
