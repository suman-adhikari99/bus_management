
import datetime
from django.db.models import Count, F, Value
from django.db import models
from django.db.models import Value, IntegerField, ForeignKey, CharField
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ValidationError
from datetime import time
from tracemalloc import start
from django.http import HttpResponseRedirect
import email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, generics
from .models import User, Bus, Route, Appointment, Driver
from .forms import AppointmentForm, BusForm, RouteForm, DriverForm, LocationForm
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, LoginSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserAPIView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserLoginView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


fields = ('passenger_name', 'seat_no', 'payment_method')


class CreateBusView(LoginRequiredMixin, CreateView):
    model = Bus
    form_class = BusForm
    template_name = 'admin/create.html'
    success_url = reverse_lazy('busapp:bus-list-admin')

    def get_context_data(self, **kwargs):
        context = super(CreateBusView, self).get_context_data(**kwargs)
        context["is_super"] = self.request.user.is_superuser
        context["create_obj"] = 'Create Bus'
        return context


class CreateRouteView(LoginRequiredMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'admin/create.html'
    success_url = reverse_lazy('busapp:bus-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_obj"] = 'Create Route'
        context["is_super"] = self.request.user.is_superuser
        return context


class RouteListView(LoginRequiredMixin, ListView):

    model = Route
    template_name = 'list.html'
    paginate_by = 5
    app = 'blogapp'

    def get_context_data(self, **kwargs):
        context = super(RouteListView, self).get_context_data(**kwargs)
        context['obj_url'] = 'busapp:create-route'
        context['obj_add'] = self.model.__name__
        route = self.get_queryset().order_by('id')
        return context


class CreateDriverView(LoginRequiredMixin, CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'admin/create.html'
    success_url = reverse_lazy('busapp:bus-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_super"] = self.request.user.is_superuser
        context["create_obj"] = 'Create Driver'
        return context


class CreateAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'create.html'
    success_url = reverse_lazy('busapp:appointment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_obj"] = 'Create Route'
        return context


TO = ""
FROM = ""

dates = ''


@ login_required(login_url='/login/')
def createLocationView(request):
    if request.method == 'POST':
        global TO, FROM, dates
        form = LocationForm(request.POST)
        TO = form.data['destination']
        FROM = form.data['starting_point']
        dates = form.data['date']
        print('dates form location', dates)
        return redirect('/bus-list')

    form = LocationForm()
    context = {
        'form': form,
        'create_obj': 'create-appointment'

    }
    return render(request, 'create.html', context)


class BusListView(LoginRequiredMixin, ListView):

    model = Bus
    template_name = 'bus_list.html'
    paginate_by = 5
    app = 'blogapp'

    def get_context_data(self, **kwargs):
        global TO
        queryset = Bus.objects.filter(destination=TO)

        if queryset is None:
            self.object_list = self.model.objects.all()
        context = super(BusListView, self).get_context_data(**kwargs)
        context['obj_url'] = 'busapp:create-bus'
        context['obj_add'] = self.model.__name__
        context["is_super"] = self.request.user.is_superuser
        context['object_list'] = queryset
        return context


class BusListAdminView(LoginRequiredMixin, ListView):

    model = Bus
    template_name = 'admin/list.html'
    paginate_by = 5
    app = 'blogapp'

    def get_context_data(self, **kwargs):
        context = super(BusListAdminView, self).get_context_data(**kwargs)
        context['obj_url'] = 'busapp:create-bus'
        context['obj_ad'] = self.model.__name__
        context["is_super"] = self.request.user.is_superuser
        return context


bus_name = ''
starting_point = ''http: // 127.0.0.1: 8081/report
destination = ''
exit_time = ''
bus_no = ''
ticket_price = ''
SEAT_NO = ''


class AppointmentFormView(FormView):
    form_class = AppointmentForm
    template_name = 'create.html'
    model = Appointment

    def get_form(self,  *args, **kwargs):
        global exit_time, bus_no, bus_name, dates, starting_point, destination, passenger_name, ticket_price

        SEAT = [
            ('1', '1'), ('2', '2'), ('3', '3'), ('4',
                                                 '4'), ('5', '5'), ('6', '6'), ('7', '7'),
            ('8', '8'), ('9', '9'),  ('10', '10')]
        pk = self.kwargs.get('pk')
        bus_detail = Bus.objects.filter(bus_no=pk).first()
        bus_no = bus_detail.bus_no
        bus_name = bus_detail.bus_name
        starting_point = bus_detail.starting_point
        destination = bus_detail.destination
        exit_time = bus_detail.exit_time
        ticket_price = bus_detail.ticket_price
        if dates == '':
            return HttpResponse('skal')
        try:
            SEAT_NO = list(Appointment.objects.filter(
                bus_no=bus_no, date=dates).values_list('seat_no'))
            SEATS = [k for v in SEAT_NO for k in v]
            form = super().get_form(*args,  **kwargs)
            form.fields['seat_no'].choices = [
                (k, v) for k, v in SEAT if k not in SEATS]
            return form
        except Exception:
            x = datetime.datetime(2020, 5, 17)
            SEAT_NO = list(Appointment.objects.filter(
                bus_no=bus_no, date=x).values_list('seat_no'))
            SEATS = [k for v in SEAT_NO for k in v]
            form = super().get_form(*args,  **kwargs)
            form.fields['seat_no'].choices = [
                (k, v) for k, v in SEAT if k not in SEATS]
            return form

    def form_valid(self, form):
        form = form.save(commit=False)
        passenger_name = form.passenger_name
        print('passeger', passenger_name)
        payment_method = form.payment_method
        seat_no = form.seat_no
        try:
            appointments = Appointment.objects.create(
                passenger_name=passenger_name, bus_name=bus_name, bus_no=bus_no, seat_no=seat_no,
                payment_method=payment_method, time=exit_time, starting_point=starting_point,
                destination=destination, ticket_price=ticket_price, date=dates)
            appointments.save()
        except Exception:
            x = datetime.datetime(2020, 5, 17)
            appointments = Appointment.objects.create(
                passenger_name=passenger_name, bus_name=bus_name, bus_no=bus_no, seat_no=seat_no,
                payment_method=payment_method, time=exit_time, starting_point=starting_point,
                destination=destination, ticket_price=ticket_price, date=x)
            appointments.save()

        return redirect('/appointment-detail')


@ login_required(login_url='/login/')
def createAppointment(request, pk):
    if request.method == 'POST':
        try:
            global exit_time, bus_no, bus_name, dates, starting_point, destination, passenger_name, ticket_price
            form = AppointmentForm(request.POST)
            passenger_name = form.data['passenger_name']
            payment_method = form.data['payment_method']
            seat_no = form.data['seat_no']
            appointment = Appointment.objects.filter(
                bus_no=bus_no, seat_no=seat_no, date=dates).first()
            if appointment is not None:
                return HttpResponse('this seat is already reserved')
            appointments = Appointment.objects.create(
                passenger_name=passenger_name, bus_name=bus_name, bus_no=bus_no, seat_no=seat_no,
                payment_method=payment_method, time=exit_time, starting_point=starting_point,
                destination=destination, ticket_price=ticket_price)
            appointments.save()
            return redirect('/appointment-detail')
        except Exception as e:
            form = AppointmentForm(request.POST)
            print(e)
            return HttpResponse("your appointment is not created please try again")
    if request.method == 'GET':
        bus_detail = Bus.objects.filter(bus_no=pk).first()
        bus_name = bus_detail.bus_name
        starting_point = bus_detail.starting_point
        destination = bus_detail.destination
        bus_no = bus_detail.bus_no
        exit_time = bus_detail.exit_time
        ticket_price = bus_detail.ticket_price
        not_availabe_seat = list(Appointment.objects.filter(
            bus_no=bus_no, date=dates).values_list('seat_no'))
        form = AppointmentForm()
        context = {
            'form': form,
            'create_obj': 'create-appointment',
            'reserve': not_availabe_seat,
            'bus_no': bus_no,
            'bus_name': bus_name,
            'ticket_price': ticket_price

        }
        return render(request, 'create.html', context)


class AppointmentDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        model = Appointment
        app = 'busapp'
        object = model.objects.order_by('-id').first()
        fields = [field.name for field in model._meta.fields]
        values = [getattr(object, field_name) for field_name in fields]
        fields = [field.verbose_name for field in model._meta.fields]
        value = dict(zip(fields, values))
        is_super = request.user.is_superuser
        return render(request, "admin/detail.html", {'fields': fields, 'values': value,
                                                     'object': object, 'app': app, 'is_super': is_super})


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'admin/list.html'
    paginate_by = 5
    app = 'blogapp'

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        context['obj_url'] = 'busapp:create-bus'
        context['obj_add'] = self.model.__name__
        context["is_super"] = self.request.user.is_superuser
        return context


def dashboard(request):
    return render(request, 'dashboard.html')


def reportAccordingToBus(request):
    total_price = 0  # total income is stored here
    bus_no = []  # unique bus number are stored here
    dt = []  # date are stored
    bus = Appointment.objects.all()
    # total_price = Appointment.objects.aggregate(Sum('ticket_price'))
    for appointment in bus:
        total_price = total_price+appointment.ticket_price
        bus = appointment.bus_no
        if bus not in bus_no:
            bus_no.append(bus)
        d = appointment.date

        if d not in dt:
            dt.append(d)
    bus_no_prices = []
    date_price = []
    for appointment in bus_no:  # for price according to bus_no
        bus_obj = Appointment.objects.filter(bus_no=appointment)
        c = 0
        for app in bus_obj:
            c = c+app.ticket_price
        bus_no_prices.append(c)
    for x in dt:
        dt_obj = Appointment.objects.filter(date=x)
        d = 0
        for y in dt_obj:
            d = d+y.ticket_price
        date_price.append(d)
    bus_income = dict(zip(bus_no, bus_no_prices))
    date_income = dict(zip(dt, date_price))
    context = {
        'total_income': total_price,
        'bus_income': bus_income,
        'date': dt,
        'date_income': date_income
    }

    return render(request, 'report.html', context)
