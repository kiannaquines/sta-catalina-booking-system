from django.urls import path
from driver.views import *

urlpatterns = [
    path('', DriverPage.as_view(), name="driver_page"),
]