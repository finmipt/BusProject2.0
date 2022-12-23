import csv
import json


def convert_time(time):
    hours, minutes, seconds = time.split(':')
    if int(hours) >= 24:
        hours = str(int(hours) - 24)
    return f"{hours}:{minutes}:{seconds}"



def convert_routes():
    # Open the .txt file (csv) for the Route model
    data = []
    with open('routes.txt', 'r', encoding='utf8') as file:
        # Read the file as a CSV
        reader = csv.reader(file, delimiter=',')
        # Iterate over the rows in the CSV
        for row in reader:
            # Create a dictionary for the model instance
            route = {
                'model': 'api.Route',
                'fields': {
                    'id': row[0],
                    'agency_id': row[1],
                    'route_short_name': row[2],
                    'route_long_name': row[3],
                    'route_type': row[4],
                    'route_color': row[5],
                    'competent_authority': row[6],
                    'route_desc': row[7],
                }
            }
            # Add the dictionary to the list
            data.append(route)
    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Write the serialized data to a JSON file
    with open('routes.json', 'w') as file:
        file.write(json_data)

def convert_trips():
    data = []
    # Open the .txt file (csv) for the Trip model
    with open('trips.txt', 'r', encoding='utf8') as file:
        # Read the file as a CSV
        reader = csv.DictReader(file)

        for row in reader:
            # Create a dictionary for the model instance
            trip = {
                'model': 'api.Trip',
                'fields': {
                    'id': row['trip_id'],
                    'route_id': row['route_id'],
                    # 'service_id': row[2],
                    'trip_headsign': row['trip_headsign'],
                    'trip_long_name': row['trip_long_name'],
                    'direction_code': row['direction_code'],
                    'shape_id': row['shape_id'],

                }
            }
            # Add the dictionary to the list
            data.append(trip)
    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Write the serialized data to a JSON file
    with open('trips.json', 'w', encoding='utf8') as file:
        file.write(json_data)


def convert_stops():
    data = []
    # Open the .txt file (csv) for the Stop model
    with open('stops.txt', 'r', encoding='utf8') as file:
        # Read the file as a CSV
        reader = csv.DictReader(file)
        # Iterate over the rows in the CSV
        for row in reader:
            # Create a dictionary for the model instance
            stop = {
                'model': 'api.Stop',
                'fields': {
                    'id': row['stop_id'],
                    'stop_code': row['stop_code'],
                    'stop_name': row['stop_name'],
                    'stop_lat': row['stop_lat'],
                    'stop_lon': row['stop_lon'],
                    'zone_id': row['zone_id'],
                    'alias': row['alias'],
                    'stop_area': row['stop_area'],
                    'stop_desc': row['stop_desc'],
                    'lest_x': row['lest_x'],
                    'lest_y': row['lest_y'],
                    'zone_name': row['zone_name'],
                    'authority': row['authority'],
                }
            }

            # Add the dictionary to the list
            data.append(stop)
    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Write the serialized data to a JSON file
    with open('stops.json', 'w') as file:
        file.write(json_data)


def convert_StopTime():
    data = []
    # Open the .txt file (csv) for the StopTime model
    with open('stop_times.txt', 'r', encoding='utf8') as file:
        # Read the file as a CSV
        reader = csv.DictReader(file)
        # Iterate over the rows in the CSV
        for row in reader:
            # Create a dictionary for the model instance
            stop_time = {
                'model': 'api.StopTime',
                'fields': {
                    'trip_id': row['trip_id'],
                    'arrival_time': convert_time(row['arrival_time'],),
                    'departure_time': convert_time(row['departure_time']),
                    'stop_id': row['stop_id'],
                    'stop_sequence': row['stop_sequence'],
                    'pickup_type': row['pickup_type'],
                    'drop_off_type': row['drop_off_type'],
                }
            }

            # Add the dictionary to the list
            data.append(stop_time)

    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Write the serialized data to a JSON file
    with open('stop_times.json', 'w', encoding='utf8') as file:
        file.write(json_data)


convert_StopTime()