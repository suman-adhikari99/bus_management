from datetime import date
from django import forms
from .models import Bus, Route, Appointment, Driver, User
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class TimeInput(forms.TimeInput):
    input_type = "time"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('passenger_name', 'seat_no', 'payment_method')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        new_data = {
            'class': 'form-control',

        }

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(new_data)


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_data = {
            'class': 'form-control',

        }

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(new_data)
        self.fields["exit_time"].widget = TimeInput()

    def clean(self):
        super(BusForm, self).clean()
        bus_no = str(self.cleaned_data.get('bus_no'))
        if len(bus_no) != 4:
            self._errors['bus_no'] = self.error_class([
                'bus-no should be 4 digit'])
        return self.cleaned_data


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_data = {
            'class': 'form-control',
        }
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(new_data)

    def clean(self):
        super(DriverForm, self).clean()
        email = self.cleaned_data.get('email')
        print('driver email:', email)
        driver = User.objects.filter(email=email).first()
        print('role is:', driver.role)

        if driver.role != 2:
            self._errors['email'] = self.error_class([
                'for driver role should be driver'])
        return self.cleaned_data


class LocationForm(forms.Form):
    FROM = [
        ('RATNAPARK', "RATNAPARK"),
        ('RNAC', 'RNAC'),
        ('KOTESHAWOR', 'KOTESHAWOR'),
        ('BANEPA', 'BANEPA'),
        ('SANGA', 'SANBA'),
        ('DHULIKHEL', 'DHULIKHEL'),
    ]
    TO = [('BANEPA', 'BANEPA'),
          ('SANGA', 'SANBA'),
          ('DHULIKHEL', 'DHULIKHEL'),
          ('RATNAPARK', "RATNAPARK"),
          ('RNAC', 'RNAC'),
          ('KOTESHAWOR', 'KOTESHAWOR'),
          ]
    starting_point = forms.ChoiceField(choices=FROM)
    destination = forms.ChoiceField(choices=TO)
    date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        new_data = {
            'class': 'form-control'
        }
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(new_data)
        self.fields["date"].widget = DateInput()

    def clean(self):
        cleaned_data = super(LocationForm, self).clean()
        if not cleaned_data['date']:
            cleaned_data['date'] = None
        return cleaned_data
