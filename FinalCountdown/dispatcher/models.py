from datetime import timedelta

from django.db import models
from django.utils import timezone

class Bus(models.Model):
    name = models.CharField(max_length=100)
    seats = models.IntegerField()
    ready = models.BooleanField(default= True)
    allowed_drivers = models.ManyToManyField('Driver', blank=True, related_name='allowed_buses')
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_buses')
    
    def __str__(self) -> str:
        return f"{self.name}({self.seats} seats)"


class Driver(models.Model):
    name = models.CharField(max_length=100)
    last_rest_start = models.DateTimeField(null=True, blank=True)
    last_drive_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def needs_rest(self):
        if self.last_drive_date and timezone.now() - self.last_drive_date >= timedelta(days=6):
            return True
        return False
    
    def week_break(self):
        if self.last_rest_start and timezone.now() - self.last_rest_start >= timedelta(hours=45):
             return True
        return False
    
    def daily_break(self):
        min_break_time = timedelta(hours=11)
        if self.last_rest_start:
            if (timezone.now()-self.last_rest_start) < min_break_time:
                return False
            return True
        
    def __str__(self) -> str:
        return self.name
    
class Reservation(models.Model):
    name = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)   
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)   
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"Rezervace busu {self.bus.name} s řidičem {self.driver.name}"

# Create your models here.
