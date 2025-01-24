from django.core.management.base import BaseCommand

from core.models import Owner, Car, Road, TollStation

import json


class Command(BaseCommand):
    help = "Import data from JSON files into the database"

    def handle(self, *args, **kwargs):
        try:
            # Import owners
            with open('core/data/owners.json', 'r') as f:
                owners_data = json.load(f)

            for owner_data in owners_data:
                owner, _ = Owner.objects.get_or_create(
                    national_code=owner_data['national_code'],
                    defaults={
                        "name": owner_data['name'],
                        "age": owner_data['age'],
                        "total_toll_paid": owner_data['total_toll_paid'],
                    },
                )
                for car_data in owner_data['ownerCar']:
                    Car.objects.get_or_create(
                        id=car_data['id'],
                        defaults={
                            "owner": owner,
                            "type": car_data['type'],
                            "color": car_data['color'],
                            "length": car_data['length'],
                            "load_volume": car_data.get('load_valume'),
                        },
                    )

            self.stdout.write(self.style.SUCCESS("Owners and cars imported successfully."))

            # Import roads with duplicate handling
            with open('core/data/roads.json', 'r') as f:
                roads_data = json.load(f)

            for road_data in roads_data:
                name = road_data.get('name', "1")  # Default to "1" if name is missing
                duplicate_roads = Road.objects.filter(name=name)

                if duplicate_roads.exists():
                    print(f"Duplicate road skipped: {name}")
                else:
                    Road.objects.create(
                        name=name,
                        width=road_data['width'],
                        geometry=road_data['geom'],
                    )

            self.stdout.write(self.style.SUCCESS("Roads imported successfully."))

            # Import toll stations
            with open('core/data/tollStations.json', 'r') as f:
                toll_stations_data = json.load(f)

            for toll_data in toll_stations_data:
                TollStation.objects.get_or_create(
                    name=toll_data['name'],
                    defaults={
                        "toll_per_cross": toll_data['toll_per_cross'],
                        "location": toll_data['location'],
                    },
                )

            self.stdout.write(self.style.SUCCESS("Toll stations imported successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
