from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management.base import BaseCommand
from django.shortcuts import render, get_object_or_404

from core.models import Owner, Car, TollStation, Road

import math, json


def red_blue_cars(request):
    cars = Car.objects.filter(color__in=['red', 'blue'])
    data = [{"id": car.id, "color": car.color, "type": car.type} for car in cars]
    return JsonResponse(data, safe=False)


@csrf_exempt
def register_owner_car(request):
    if request.method == "POST":
        data = json.loads(request.body)
        owner = Owner.objects.create(
            name=data['name'],
            national_code=data['national_code'],
            age=data['age']
        )
        for car_data in data['cars']:
            Car.objects.create(
                owner=owner,
                type=car_data['type'],
                color=car_data['color'],
                length=car_data['length'],
                load_volume=car_data.get('load_volume')
            )
        return JsonResponse({"message": "Owner and cars registered successfully!"})


def cars_by_owner_age(request):
    cars = Car.objects.filter(owner__age__gt=70)
    data = [{"id": car.id, "owner": car.owner.name, "age": car.owner.age} for car in cars]
    return JsonResponse(data, safe=False)


def heavy_cars_on_narrow_roads(request):
    # Filter heavy cars
    heavy_cars = Car.objects.filter(type='big')
    data = []

    # Check if roads are narrow (width < 20)
    for car in heavy_cars:
        narrow_roads = Road.objects.filter(width__lt=20)  # Roads with width < 20
        for road in narrow_roads:
            data.append({
                "car_id": car.id,
                "car_owner": car.owner.name,
                "road_name": road.name,
                "road_width": road.width,
            })

    return JsonResponse(data, safe=False)


def calculate_toll(request, car_id):
    # Retrieve the car object
    car = get_object_or_404(Car, id=car_id)
    
    # Calculate toll for the car
    if car.type == 'big':  # Heavy cars
        toll = 2000 + (car.load_volume * 300)
    else:  # Light cars
        toll = 2000  # Base toll
    
    # Prepare response
    data = {
        "car_id": car.id,
        "owner": car.owner.name,
        "type": car.type,
        "color": car.color,
        "total_toll": toll,
    }
    return JsonResponse(data)


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in meters (simplified)."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def owners_with_violations(request):
    # Example logic: owners with unpaid tolls are considered violators
    violating_owners = Owner.objects.filter(total_toll_paid=0).order_by('-total_toll_paid')  # Modify this as needed

    data = []
    for owner in violating_owners:
        data.append({
            "name": owner.name,
            "national_code": owner.national_code,
            "total_toll_due": owner.total_toll_paid,
        })

    return JsonResponse(data, safe=False)


def homepage(request):
    return render(request, 'homepage.html')
