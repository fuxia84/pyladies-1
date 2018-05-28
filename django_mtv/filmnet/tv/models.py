from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField()

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=50)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    adults_only = models.BooleanField()

    def __str__(self):
        return self.name
