from django.shortcuts import render
from django.shortcuts import get_object_or_404
from random import choice
from django.http import JsonResponse, HttpResponse
from .models import Stop, Trip, Route, StopTime
import datetime
from django.shortcuts import get_object_or_404




def search_trips_five_nearest(request):
    if request.method == 'GET':
        stop_id = request.GET.get('stop_id')
        try:
            # Get the stop with the given ID
            stop = Stop.objects.get(id=stop_id)
        except Stop.DoesNotExist:
            # Return an error response if the stop does not exist
            return JsonResponse({'error': 'Stop not found'}, status=404)

        # Get the current time
        current_time = datetime.datetime.now()

        # Get the 5 nearest trips to the stop
        trips = StopTime.objects.filter(stop=stop, departure_time__gt=current_time).order_by('departure_time')[:5]

        # Retrieve the names and the number of minutes until each trip
        routes_and_times = []
        for trip in trips:
            route = Route.objects.get(id=trip.trip.route_id)
            # Convert the departure time to a datetime object using the current date
            departure_datetime = datetime.datetime.combine(datetime.date.today(), trip.departure_time)
            # Calculate the difference between the current time and the departure time
            time_difference = departure_datetime - current_time
            # Convert the difference to minutes
            minutes_until_trip = time_difference.total_seconds() / 60
            routes_and_times.append({'route': route.route_short_name, 'minutes_until_trip': minutes_until_trip})

        # Return a success response with the names and the number of minutes until each trip
        return JsonResponse({'routes_and_times': routes_and_times})


def get_stop_area_tips(request, query=None):
    if query:
        stops_areas = Stop.objects.filter(stop_area__icontains=query)
    else:
        stops_areas = Stop.objects.all()
    stops_areas = stops_areas.values_list('stop_area', flat=True)
    stops_areas = set(stops_areas)
    stops_areas = list(stops_areas)
    # Return a success response with the list of unique stop area names
    return JsonResponse({'stop_areas': stops_areas})


def get_stop_tips(request, query, stop_area='Narva linn'):
    if query:
        stops = Stop.objects.filter(stop_name__istartswith=query, stop_area=stop_area)
    else:
        stops = Stop.objects.all(stop_area=stop_area)
    stops = stops.values_list('stop_name', flat=True)
    stops = set(stops)
    stops = list(stops)
    # Return a success response with the list of unique stop area names
    return JsonResponse({'stops': stops})


def get_routes_by_stop(request, stop_id):
    # Get the stop object

    stop_times = StopTime.objects.filter(stop_id=stop_id).prefetch_related('trip', 'trip__route')
    routes = []
    trips = []
    for stop_time in stop_times:
        found = False
        for route in routes:
            if route.id == stop_time.trip.route_id:
                found = True
                break
        if found:
            continue
        trips.append(stop_time.trip)
        routes.append(stop_time.trip.route)

    routes_info = []
    # Iterate over the routes and get the route information
    for route_obj in routes:
        routes_info.append({
            'id': route_obj.id,
            'short_name': route_obj.route_short_name,
            'long_name': route_obj.route_long_name,
            'color': route_obj.route_color
        })

    # Return the routes as a JSON response
    return JsonResponse(routes_info, safe=False)


def get_stop_id(request, stop_area, stop_name):
    stop_area = stop_area
    stop_name = stop_name
    stops = Stop.objects.filter(stop_area=stop_area, stop_name=stop_name)
    if stops.exists():
        stop = choice(stops)
        return HttpResponse(stop.id)
    else:
        return HttpResponse('Not Found', status=404)


def get_arrival_times(request, stop_id, route_id):
    # stop_id = request.GET.get('stop_id')
    # route_id = request.GET.get('route_id')

    # Get the current time
    now = datetime.datetime.now()

    # Get the stop times for the specified stop and route
    stop_times = StopTime.objects.filter(stop__id=stop_id, trip__route__id=route_id)

    # Create a list of dictionaries with the arrival times and time left until arrival
    arrival_times = []
    for stop_time in stop_times:
        arrival_datetime = datetime.datetime.combine(now, stop_time.arrival_time)
        arrival_time = stop_time.arrival_time.strftime('%H:%M:%S')
        time_left = (arrival_datetime - now).total_seconds() // 60
        arrival_times.append({
            'arrival_time': arrival_time,
            'time_left': time_left
        })

    # Return the arrival times as a JSON response
    return JsonResponse({'arrival_times': arrival_times})


