from django.urls import path
from django.views.generic import TemplateView

from core.views import (
	red_blue_cars,
	register_owner_car,
	cars_by_owner_age,
	heavy_cars_on_narrow_roads,
	calculate_toll,	
	owners_with_violations,
	homepage,
)


urlpatterns = [
	path('', homepage, name='homepage'),
    path('register/', register_owner_car),

    path('cars/red-blue/', red_blue_cars),
    path('cars/owner-age/', cars_by_owner_age),
    path('cars/heavy-narrow/', heavy_cars_on_narrow_roads),
	path('cars/toll/<int:car_id>/', calculate_toll, name='calculate_toll'),

	path('test/register/', TemplateView.as_view(template_name="test_register.html")),	
	
    path('owners/violations/', owners_with_violations, name='owners_with_violations'),
]
