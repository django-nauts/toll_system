from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100)
    national_code = models.BigIntegerField(unique=True)
    age = models.PositiveIntegerField()
    total_toll_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	
class Car(models.Model):
    owner = models.ForeignKey(Owner, related_name='cars', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('small', 'Small'), ('big', 'Big')])
    color = models.CharField(max_length=20)
    length = models.FloatField()
    load_volume = models.FloatField(null=True, blank=True)

	
class Road(models.Model):
    name = models.CharField(max_length=100, default="Unknown Road")
    width = models.FloatField()
    geometry = models.TextField()

	
class TollStation(models.Model):
    name = models.CharField(max_length=100)
    toll_per_cross = models.PositiveIntegerField()
    location = models.TextField()
