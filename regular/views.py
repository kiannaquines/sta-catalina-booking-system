from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from app.models import *
from django.urls import reverse
from regular.forms import MyReservationForm
from django.contrib import messages
from app.mixins import CustomLoginRequiredMixin
from django.urls import reverse_lazy

class RegularView(CustomLoginRequiredMixin, View):
    template_name = "regular_index.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            reserved_by=request.user
        )
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class ReservedBookingView(CustomLoginRequiredMixin, CreateView):
    template_name = 'regular_add.html'
    model = ReservationModel
    form_class = MyReservationForm
    success_url = reverse_lazy("regular_page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.reserved_by = self.request.user
        messages.success(
            self.request,
            "You have successfully added a new reservation.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error, extra_tags="danger")
        return super().form_invalid(form)


class UpdateReservation(CustomLoginRequiredMixin, UpdateView):
    pass


class DeleteReservation(CustomLoginRequiredMixin, DeleteView):
    pass


class CancelReservation(CustomLoginRequiredMixin, View):
    pass
