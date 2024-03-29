# Generated by Django 3.2.16 on 2022-12-18 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('agency_id', models.CharField(max_length=255)),
                ('route_short_name', models.CharField(max_length=255)),
                ('route_long_name', models.CharField(max_length=255)),
                ('route_type', models.CharField(max_length=255)),
                ('route_color', models.CharField(max_length=255)),
                ('competent_authority', models.CharField(max_length=255)),
                ('route_desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('stop_code', models.CharField(max_length=255)),
                ('stop_name', models.CharField(max_length=255)),
                ('stop_lat', models.FloatField()),
                ('stop_lon', models.FloatField()),
                ('zone_id', models.CharField(max_length=255)),
                ('alias', models.CharField(blank=True, max_length=255, null=True)),
                ('stop_area', models.CharField(max_length=255)),
                ('stop_desc', models.TextField(blank=True, null=True)),
                ('lest_x', models.FloatField()),
                ('lest_y', models.FloatField()),
                ('zone_name', models.CharField(blank=True, max_length=255, null=True)),
                ('authority', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('trip_headsign', models.CharField(max_length=255)),
                ('trip_long_name', models.CharField(max_length=255)),
                ('direction_code', models.CharField(max_length=255)),
                ('shape_id', models.CharField(max_length=255)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='api.route')),
            ],
        ),
        migrations.CreateModel(
            name='StopTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('stop_sequence', models.PositiveIntegerField(blank=True, null=True)),
                ('pickup_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('drop_off_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stop_times', to='api.stop')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stop_times', to='api.trip')),
            ],
        ),
    ]
