from django.urls import path
from driver.views import *

urlpatterns = [
    path('', DriverPage.as_view(), name="driver_page"),
    path('reservation/delivered', DriverDeliveredReservationPage.as_view(), name="driver_delivered_page"),
    path('reservation/route/<int:reservation_id>', ViewMapRoute.as_view(), name="driver_route_page"),
    path('reservation/delivered/<int:reservation_id>', UpdateDeliveryStatus.as_view(), name="driver_delivered_page"),
]