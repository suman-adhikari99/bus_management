from .models import Appointment
from django.db import models
import django_filters
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = {
            'date': ['exact', 'year', 'year__gt', 'year__lt', 'range'],
            'bus_no': ['exact', ],

        }

    @classmethod
    def filter_for_lookup(cls, f, lookup_type):

        if isinstance(f, models.DateField) and lookup_type == 'range':
            return django_filters.DateRangeFilter, {}

        return super().filter_for_lookup(f, lookup_type)
