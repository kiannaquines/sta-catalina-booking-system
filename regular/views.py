from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from app.models import *
from django.urls import reverse
from regular.forms import  ReservationForm, ReservationProductForm
from django.contrib import messages
from app.mixins import CustomLoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q


class RegularView(CustomLoginRequiredMixin, View):
    template_name = "regular_index.html"

    def get(self, request):
        context = {}

        reservations_with_products = []
        
        reservations = ReservationModel.objects.filter(
            Q(reserved_by=request.user),
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


class CancelledRegularView(CustomLoginRequiredMixin, View):
    template_name = "cancelled_reservation.html"

    def get(self, request):
        context = {}
        context["reservations"] = ReservationModel.objects.filter(
            reserved_by=request.user,
            reservation_status=ReservationModel.RESERVATION_STATUS[2][0],
        )
        return render(request, self.template_name, context)


class ReservedBookingView(CustomLoginRequiredMixin, View):
    template_name = "regular_add.html"
    success_url = reverse_lazy("regular_page")

    def get_context_data(self, personal_info_form=None, farm_profile_form=None):
        return {
            'name': 'Create Reservation',
            'subtitle': 'Create a new reservation here',
            'button': 'Create Reservation',
            'reservation_form': personal_info_form or ReservationForm(),
            'product_form': farm_profile_form or ReservationProductForm(),
        }

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        personal_info_form = ReservationForm(request.POST)
        farm_profile_form = ReservationProductForm(request.POST)

        if personal_info_form.is_valid() and farm_profile_form.is_valid():
            reservation = personal_info_form.save(commit=False)
            reservation.reserved_by = request.user
            reservation.save()

            product_index = 0
            while 'product_name' in request.POST:
                if product_index == 0:
                    product_name = request.POST.get('product_name')
                    quantity = request.POST.get('quantity')
                    delivery_quantity_type = request.POST.get('delivery_quantity_type')
                else:
                    product_name = request.POST.get(f'product_name_{product_index}')
                    quantity = request.POST.get(f'quantity_{product_index}')
                    delivery_quantity_type = request.POST.get(f'delivery_quantity_type_{product_index}')
                
                if not product_name:
                    break

                ReservationProduct.objects.create(
                    product_name=product_name,
                    quantity=quantity,
                    delivery_quantity_type=delivery_quantity_type,
                    tied_with_reservation_of=reservation
                )

                product_index += 1

            messages.success(
                request,
                "You have successfully added a new reservation. You will get a notification when a driver is assigned.",
                extra_tags="success",
            )
            return redirect(self.success_url)
        else:
            for field, errors in personal_info_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags="danger")

            for field, errors in farm_profile_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags="danger")

            return render(request, self.template_name, self.get_context_data(personal_info_form, farm_profile_form))


class UpdateReservation(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "reservation_id"
    template_name = "regular_update.html"
    model = ReservationModel
    form_class = ReservationForm
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

            if ReservationModel.objects.filter(
                id=reservation_id,
                reserved_by=request.user,
                reservation_status=ReservationModel.RESERVATION_STATUS[1][0],
            ).first():
                messages.error(
                    self.request,
                    "You cannot cancel a confirmed reservation.",
                    extra_tags="danger",
                )
                return HttpResponseRedirect(reverse("regular_page"))

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
