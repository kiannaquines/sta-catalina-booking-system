from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from app.models import *
from django.urls import reverse
from regular.forms import MyReservationForm
from django.contrib import messages
from app.mixins import CustomLoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q


class RegularView(CustomLoginRequiredMixin, View):
    template_name = "regular_index.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            Q(reserved_by=request.user),
            Q(reservation_status=ReservationModel.RESERVATION_STATUS[1][0])
            | Q(reservation_status=ReservationModel.RESERVATION_STATUS[0][0]),
        )
        return render(request, self.template_name, context)


class CancelledRegularView(CustomLoginRequiredMixin, View):
    template_name = "cancelled_reservation.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            reserved_by=request.user,
            reservation_status=ReservationModel.RESERVATION_STATUS[2][0],
        )
        return render(request, self.template_name, context)


class ReservedBookingView(CustomLoginRequiredMixin, CreateView):
    template_name = "regular_add.html"
    model = ReservationModel
    form_class = MyReservationForm
    success_url = reverse_lazy("regular_page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.reserved_by = self.request.user
        messages.success(
            self.request,
            "You have successfully added a new reservation, you will get a notification when staff assigned a driver to your reservation.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags="danger")
        return super().form_invalid(form)


class UpdateReservation(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "reservation_id"
    template_name = "regular_update.html"
    model = ReservationModel
    form_class = MyReservationForm
    success_url = reverse_lazy("regular_page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.reserved_by = self.request.user
        messages.success(
            self.request,
            "You have successfully updated your reservation.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags="danger")
        return super().form_invalid(form)


class DeleteReservationView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "reservation_id"
    template_name = "regular_delete.html"
    model = ReservationModel
    success_url = reverse_lazy("regular_page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            "You have successfully remove your reservation.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags="danger")
        return super().form_invalid(form)


class CancelReservationView(CustomLoginRequiredMixin, View):
    def get(self, request, reservation_id):
        reservation = ReservationModel.objects.filter(
            id=reservation_id, reserved_by=request.user
        )
        if reservation:
            reservation.update(
                reservation_status=ReservationModel.RESERVATION_STATUS[2][0]
            )
            messages.success(
                self.request,
                "You have successfully cancelled your reservation.",
                extra_tags="success",
            )
        else:
            messages.error(
                self.request,
                "You cannot cancel this reservation as it does not belong to you.",
                extra_tags="danger",
            )
        return HttpResponseRedirect(reverse("regular_page"))
