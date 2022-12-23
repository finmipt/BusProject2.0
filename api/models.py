from django.db import models


class Route(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    agency_id = models.CharField(max_length=255)
    route_short_name = models.CharField(max_length=255)
    route_long_name = models.CharField(max_length=255)
    route_type = models.CharField(max_length=255)
    route_color = models.CharField(max_length=255)
    competent_authority = models.CharField(max_length=255)
    route_desc = models.TextField(null=True, blank=True)


class Trip(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    trip_headsign = models.CharField(max_length=255)
    trip_long_name = models.CharField(max_length=255)
    direction_code = models.CharField(max_length=255)
    shape_id = models.CharField(max_length=255)


class Stop(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    stop_code = models.CharField(max_length=255)
    stop_name = models.CharField(max_length=255)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, null=True, blank=True)
    stop_area = models.CharField(max_length=255)
    stop_desc = models.TextField(null=True, blank=True)
    lest_x = models.FloatField()
    lest_y = models.FloatField()
    zone_name = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=255, null=True, blank=True)


class StopTime(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stop_times')
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='stop_times')
    stop_sequence = models.PositiveIntegerField(null=True, blank=True)
    pickup_type = models.PositiveSmallIntegerField(null=True, blank=True)
    drop_off_type = models.PositiveSmallIntegerField(null=True, blank=True)
