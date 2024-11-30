from django.urls import path
from regular.views import *

urlpatterns = [
    path('', RegularView.as_view(), name="regular_page"),
    path('reservation/add/', ReservedBookingView.as_view(), name="regular_page_reserve"),
]