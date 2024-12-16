from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib import messages
from app.mixins import CustomLoginRequiredMixin
from app.models import ReservationModel, TruckModel
from django.db.models import Q
from django.urls import reverse_lazy

from app.forms import DriverReservationForm

class DriverUpdateDeliveryStatus(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'reservation_id'
    template_name = 'form.html'
    form_class = DriverReservationForm
    model = ReservationModel
    success_url = reverse_lazy('driver_page')

    def form_valid(self, form) -> HttpResponse:
        messages.success(
            self.request,
            "You have successfully updated the reservation status.",
            extra_tags="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        messages.error( 
            self.request,
            "There was an error while updating status.",
            extra_tags="primary",
        )
        return super().form_invalid(form)
    

class DriverPage(CustomLoginRequiredMixin, View):
    template_name = "driver_index.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            Q(truck__driver=request.user),
        )
        return render(request, self.template_name, context)


class DriverDeliveredReservationPage(CustomLoginRequiredMixin, View):
    template_name = "driver_delivered.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            Q(truck__driver=request.user),
            is_delivered=True,
        )
        return render(request, self.template_name, context)


class UpdateDeliveryStatus(CustomLoginRequiredMixin, View):
    def get(self, request, reservation_id):
        if request.method == "GET":
            if reservation_id:
                reservation = ReservationModel.objects.get(pk=reservation_id)
                if reservation:
                    if reservation.is_delivered == True:
                        messages.info(
                            request,
                            "This product has already been delivered.",
                            extra_tags="info",
                        )
                        return HttpResponseRedirect(reverse_lazy("driver_page"))

                    reservation.is_delivered = not reservation.is_delivered
                    TruckModel.objects.filter(
                        driver=request.user,
                    ).update(is_reserved=False)

                    reservation.save()
                    messages.success(
                        request,
                        "Good job, you have successfully delivered the product reservation.",
                        extra_tags="success",
                    )
                    return HttpResponseRedirect(reverse_lazy("driver_page"))


class ViewMapRoute(CustomLoginRequiredMixin, View):
    template_name = "route.html"

    def get(self, request, reservation_id):
        context = {}
        context["reservation"] = ReservationModel.objects.get(id=reservation_id)
        return render(request, self.template_name, context)
