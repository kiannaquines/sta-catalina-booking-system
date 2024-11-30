from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    USER_TYPE = (
        ("Staff", "Staff"),
        ("Manager", "Manager"),
        ("Regular User", "Regular User"),
        ("Driver", "Driver"),
    )

    user_type = models.CharField(
        max_length=100, choices=USER_TYPE, help_text="User access type"
    )
    is_member = models.BooleanField(default=False)
    address = models.TextField(max_length=255, help_text="Address")
    phone_number = models.CharField(max_length=255, help_text="Enter phone number")

    def get_full_name(self) -> str:
        return super().get_full_name()

    def __str__(self) -> str:
        return self.get_full_name()


class TruckModel(models.Model):
    plate_number = models.CharField(
        max_length=255, unique=True, help_text="Enter truck plate number"
    )
    driver = models.ForeignKey(
        CustomUserModel,
        limit_choices_to={"user_type": "Driver"},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.driver.get_full_name()} {self.plate_number}"


class ReservationModel(models.Model):
    RESERVATION_TYPE = (
        ("Hauling", "Hauling"),
        ("Deliver", "Deliver"),
    )

    RESERVATION_STATUS = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    )

    reserved_by = models.ForeignKey(
        CustomUserModel,
        limit_choices_to={"user_type": "Regular User"},
        on_delete=models.CASCADE,
        help_text="Select a user who reserved",
    )
    product_name = models.CharField(max_length=255, help_text="Product Name")
    quantity = models.IntegerField(help_text="Product quantity (Kilo or No. Sack)")
    location = models.CharField(help_text="Your location to deliver", max_length=255, )
    is_delivered = models.BooleanField(
        default=False, help_text="Whether the product is delivered",
    )
    truck = models.ForeignKey(
        TruckModel,
        limit_choices_to={"driver__user_type": "Driver"},
        on_delete=models.CASCADE,
        help_text="Truck to deliver",
    )
    date_reserved = models.DateTimeField(auto_now_add=False, help_text="Date reserved")
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPE, help_text="Reservation type"
    )
    reservation_status = models.CharField(
        max_length=255, default="Pending", choices=RESERVATION_STATUS
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_name
