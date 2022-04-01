from django.db import models

# Create your models here.
import uuid
from .managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from multiselectfield import MultiSelectField

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    Driver = 2
    CUSTOMER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (Driver, 'DRIVER'),
        (CUSTOMER, 'CUSTOMER')
    )
    uid = models.UUIDField(unique=True, editable=False,
                           default=uuid.uuid4, verbose_name='Public identifier')

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=3)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


class Route(models.Model):
    ROUTE = (
        ('ARANIKO', 'ARANIKO'),
        ('PUSPALAL', 'PUSPALAL'),
        ('PASANG', 'PASANG')
    )
    route = models.CharField(max_length=400, choices=ROUTE)

    def __str__(self):
        return self.route


class Driver(models.Model):
    email = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='driver')
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Bus(models.Model):
    SEAT_NO_AND_BUS_NAME = (
        ('MAYUR', 'MAYUR'),
        ('NEPAL', 'NEPAL'),
        ('DIGO', 'DIGO'))
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
          ('KOTESHAWOR', 'KOTESHAWOR'), ]

    bus_no = models.IntegerField(unique=True)
    route_id = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name='route_id')
    bus_name = models.CharField(max_length=80, choices=SEAT_NO_AND_BUS_NAME)
    exit_time = models.TimeField()
    driver_name = models.OneToOneField(
        Driver, on_delete=models.CASCADE, related_name='driver')
    starting_point = models.CharField(max_length=10, choices=FROM)
    destination = models.CharField(max_length=10, choices=TO)
    ticket_price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.bus_no)


class Appointment(models.Model):
    PAYMENT_METHOD = [
        ('ESEWA', 'ESEWA'),
        ('KHALTI', 'KHALTI'),
        ('ON_HAND', 'ON_HAND')
    ]
    SEAT_NO = [
        ('1', '1'), ('2', '2'), ('3', '3'), ('4',
                                             '4'), ('5', '5'), ('6', '6'), ('7', '7'),
        ('8', '8'), ('9', '9'),  ('10', '10')]
    passenger_name = models.CharField(max_length=40)
    date = models.DateField()
    time = models.TimeField(blank=True)
    bus_name = models.CharField(max_length=10,  blank=True)
    starting_point = models.CharField(
        max_length=130,  blank=True)
    destination = models.CharField(max_length=130,  blank=True)
    seat_no = models.CharField(choices=SEAT_NO,
                               max_length=3)
    bus_no = models.IntegerField(blank=True)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD, default="ON_HAND")
    ticket_price = models.IntegerField()

    def __str__(self):
        return self.passenger_name


class BusSeatAllocated(models.Model):
    bus_no = models.ForeignKey(
        Bus, on_delete=models.CASCADE, related_name='bus_seat_allocated')
    seat_no = models.IntegerField()
