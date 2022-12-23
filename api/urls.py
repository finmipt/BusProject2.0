from django.urls import path
from . import views

urlpatterns = [
    path('trips/', views.search_trips_five_nearest, name='search_trips'),
    path('city/<str:query>/', views.get_stop_area_tips, name='city_tips'),
    path('stop/<str:stop_area>/<str:query>/', views.get_stop_tips, name='stop_tips'),
    path('routes/<str:stop_id>', views.get_routes_by_stop, name='routes_on_stop'),
    path('idstop/<str:stop_area>/<str:stop_name>', views.get_stop_id, name='get_stop_id'),
    path('times/<str:stop_id>/<str:route_id>', views.get_arrival_times, name='get_arrivals'),
   # path('times/<str:lat>/<str:lon>', views.get_nearest_stop(), name='get_nearest_stop'),

]