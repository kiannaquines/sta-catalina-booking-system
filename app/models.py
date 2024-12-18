from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    USER_TYPE = (
        ("Staff", "Staff"),
        ("Manager", "Manager"),
        ("Client", "Client"),
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
        return self.get_username()


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


class ReservationProduct(models.Model):

    TYPE = (
        ("Sack","Sack"),
        ("Kilo","Kilo"),
    )
    tied_with_reservation_of = models.ForeignKey('ReservationModel', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, help_text="Product Name")
    quantity = models.IntegerField(help_text="Quantity of products")
    delivery_quantity_type = models.CharField(max_length=50, help_text="(Kilo or No. Sack)", choices=TYPE, default="Sack")

    def __str__(self):
        return self.product_name

class ReservationModel(models.Model):
    RESERVATION_TYPE = (
        ("Hauling", "Hauling"),
        ("Deliver", "Deliver"),
    )

    RESERVATION_STATUS = (
        ("Pending", "Pending"),
        ("Confirmed by staff", "Confirmed by staff"),
        ("For Delivery", "For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )


    reserved_by = models.ForeignKey(
        CustomUserModel,
        limit_choices_to={"user_type": "Client"},
        on_delete=models.CASCADE,
        help_text="Select a user who reserved",
    )
    
    location = models.CharField(help_text="Your location to deliver", max_length=255, )
    
    is_delivered = models.BooleanField(
        default=False, help_text="Whether the product is delivered",
    )
    complete_address = models.TextField(max_length=255, help_text="Complete address of the farm", null=True, blank=True)
    truck = models.ForeignKey(
        TruckModel,
        limit_choices_to={"driver__user_type": "Driver","is_reserved": False},
        on_delete=models.CASCADE,
        help_text="Truck to deliver",
        blank=True,
        null=True
    )
    date_reserved = models.DateField(auto_now_add=False, help_text="Date reserved")
    time_reservation = models.TimeField(auto_now_add=False, null=True, blank=True, help_text="Time reservation")
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPE, help_text="Reservation type"
    )
    reservation_status = models.CharField(
        max_length=255, default="Pending", choices=RESERVATION_STATUS,
        help_text="Reservation status"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.location} | {self.reserved_by.get_username()}'
