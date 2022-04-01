from django.urls import path
from .views import *
app_name = 'busapp'
urlpatterns = [
    path('user/', UserAPIView.as_view(), name='userapi'),
    path('usser/<int:pk>', UserAPIView.as_view(), name='userapi_detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path("bus-list/", BusListView.as_view(), name='bus-list'),
    path("bus-list-admin/", BusListAdminView.as_view(), name='bus-list-admin'),
    path("create-bus/", CreateBusView.as_view(), name="create-bus"),
    path("create-route/", CreateRouteView.as_view(), name="create-route"),
    path("route-list/", RouteListView.as_view(), name="route-list"),
    path('create-appointment/<int:pk>',
         createAppointment, name='create-appointment'),
    path("create-driver/", CreateDriverView.as_view(), name="create-driver"),
    path("create-location/", createLocationView, name="create-location"),
    path('appointment-detail/',
         AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointment-list/', AppointmentListView.as_view(),
         name='appointment-list'),
    path('', dashboard, name='dasobard'),
    path('report', reportAccordingToBus, name='report'),
    path('appointment-view/<int:pk>', AppointmentFormView.as_view()),

]
