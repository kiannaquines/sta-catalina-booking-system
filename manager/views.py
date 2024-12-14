from typing import Any
from django.shortcuts import render
from django.views import View

from app.mixins import CustomLoginRequiredMixin
from app.models import ReservationModel, ReservationProduct
from django.db.models import Q

class ManagerView(CustomLoginRequiredMixin, View):
    template_name = "manager_index.html"

    def get(self, request):
        context = {}

        reservations_with_products = []
        
        reservations = ReservationModel.objects.filter(
            Q(reservation_status=ReservationModel.RESERVATION_STATUS[1][0]) |
            Q(reservation_status=ReservationModel.RESERVATION_STATUS[0][0]),
        )

        for reservation in reservations:
            products = ReservationProduct.objects.filter(tied_with_reservation_of=reservation)
            reservations_with_products.append({
                'reservation': reservation,
                'products': products
            })

        context["reservations_with_products"] = reservations_with_products

        return render(request, self.template_name, context)