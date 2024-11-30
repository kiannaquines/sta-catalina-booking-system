from django.urls import path
from app.views import *

urlpatterns = [
    path('', LoginView.as_view(),name="login"),
    path('register/', RegisterView.as_view(),name="register"),
    path('register/profile', ProfileFormView.as_view(),name="profile_registration"),
    path('dashboard/', DashboardView.as_view(),name="dashboard"),
    path('user/logout/', logout_me, name="logout_me"),

    # Reservation
    path('reservation/', ReservationView.as_view(),name="reservation"),
    path('reservation/confirmed', ConfirmedReservationView.as_view(),name="reservation_confirmed"),
    path('reservation/report', ReservationReportView.as_view(),name="reservation_report"),
    path('reservation/create', CreateReservationView.as_view(),name="create_reservation"),
    path('reservation/cancelled', CancelledReservationView.as_view(),name="cancelled_reservation"),
    path('reservation/update/<int:reservation_id>', UpdateReservationView.as_view(),name="update_reservation"),
    path('reservation/delete/<int:reservation_id>', DeleteReservationView.as_view(),name="delete_reservation"),
    path('reservation/export/report', generate_report,name="reservation_export_report"),

    # Truck
    path('truck/', TruckView.as_view(),name="truck"),
    path('truck/create', CreateTruck.as_view(),name="truck_create"),
    path('truck/driver', TruckDriverView.as_view(),name="truck_driver"),
    path('truck/update/<int:truck_id>', UpdateTruckView.as_view(), name="truck_update"),
    path('truck/delete/<int:truck_id>', DeleteTruckView.as_view(), name="delete_update"),

    # Users
    path('users/', UserView.as_view(), name="users"),
    path('users/create', CreateUserView.as_view(), name="user_create"),
    path('users/update/<int:user_id>', UpdateUserView.as_view(), name="user_update"),
    path('users/delete/<int:user_id>', DeleteUserView.as_view(), name="user_delete"),
]