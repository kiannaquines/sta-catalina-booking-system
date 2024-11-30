from django.urls import path
from regular.views import *

urlpatterns = [
    path('', RegularView.as_view(), name="regular_page"),
    path('reservation/add/', ReservedBookingView.as_view(), name="regular_page_reserve"),
    path('reservation/update/<int:reservation_id>', UpdateReservation.as_view(), name='regular_page_reservation_update'),
    path('reservation/remove/<int:reservation_id>', DeleteReservationView.as_view(), name='regular_page_reservation_remove')
]