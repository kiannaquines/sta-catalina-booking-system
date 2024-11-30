from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, UpdateView, CreateView, DeleteView
from app.forms import ProfileForm, ReservationForm, SignupForm, TruckForm, UpdateUserForm, UserForm
from app.mixins import CustomLoginRequiredMixin
from app.models import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
from django.conf import settings
from datetime import datetime
from io import BytesIO
from collections import defaultdict
from django.contrib.auth import logout, authenticate, login
from app.forms import LoginForm

def logout_me(request):
    logout(request)
    messages.success(request,'You have been logged out', extra_tags='success')
    return HttpResponseRedirect(reverse_lazy('login'))

class ProfileFormView(CustomLoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request):
        context = {}
        form = ProfileForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.", extra_tags="success")

            if form.cleaned_data["user_type"] == "Regular User":
                return redirect("regular_page")
            elif form.cleaned_data["user_type"] == "Manager":
                return redirect("manager_page")
            else:
                return redirect("driver_page")
            
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {"form": form})

class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        context = {}
        login_form = LoginForm()
        context['form'] = login_form
        return render(request, self.template_name, context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    if user.user_type == "Regular User":
                        return redirect("regular_page")
                    elif user.user_type == "Manager":
                        return redirect("manager_page")
                    elif user.user_type == "Driver":
                        return redirect("driver_page")
                    else:
                        return redirect(reverse('dashboard'))
            
            messages.error(request, 'Invalid credentials or account still inactive.', extra_tags="danger")

        else:
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags="danger")

        return render(request, self.template_name, {'form': login_form})
                    
class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        context = {}
        signup_form = SignupForm()
        context['form'] = signup_form
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            context = {}
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                user.set_password(signup_form.cleaned_data['password2'])
                user.is_active = True
                user.save()

                authenticated_user = authenticate(
                    username=signup_form.cleaned_data['username'], 
                    password=signup_form.cleaned_data['password2']
                )

                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, "Registration successful, thank you!", extra_tags="success")
                    return redirect("profile_registration")
                else:
                    messages.error(request, "Authentication failed after registration. Please try logging in.", extra_tags="danger")
                    return redirect("login")
            else:
                for field, errors in signup_form.errors.items():
                    for error in errors:
                        messages.error(request, error, extra_tags="danger")

                context['form'] = signup_form
                return render(request, self.template_name, context)


class DashboardView(CustomLoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class ReservationView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/reservation_view.html"
    model = ReservationModel
    context_object_name = "reservations"


class ReservationReportView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/report_view.html"
    model = ReservationModel
    context_object_name = "reservations"


class ConfirmedReservationView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/confirmed_reservation.html"
    model = ReservationModel
    context_object_name = "reservations"

    def get_queryset(self):
        return ReservationModel.objects.filter(
            reservation_status=ReservationModel.RESERVATION_STATUS[1][0]
        )


class CancelledReservationView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/cancelled_reservation.html"
    model = ReservationModel
    context_object_name = "reservations"

    def get_queryset(self):
        return ReservationModel.objects.filter(
            reservation_status=ReservationModel.RESERVATION_STATUS[2][0]
        )


class TruckView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/truck_view.html"
    model = TruckModel
    context_object_name = "trucks"


class CreateTruck(CustomLoginRequiredMixin, CreateView):
    template_name = "create_template/truck_create.html"
    model = TruckModel
    form_class = TruckForm
    success_url = reverse_lazy("truck")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class TruckDriverView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/truck_driver_view.html"
    model = CustomUserModel
    context_object_name = "drivers"

    def get_queryset(self):
        return CustomUserModel.objects.filter(user_type=CustomUserModel.USER_TYPE[3][0])


class CreateReservationView(CustomLoginRequiredMixin, CreateView):
    template_name = "create_template/reservation_create.html"
    model = ReservationModel
    form_class = ReservationForm
    success_url = reverse_lazy("reservation")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully added new reservation, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class UpdateReservationView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "reservation_id"
    form_class = ReservationForm
    model = ReservationModel
    success_url = reverse_lazy("reservation")
    template_name = "update_template/reservation_update.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully updated reservation, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class UpdateTruckView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "truck_id"
    form_class = TruckForm
    model = TruckModel
    success_url = reverse_lazy("truck")
    template_name = "update_template/truck_update.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully updated truck information, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class DeleteReservationView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "reservation_id"
    model = ReservationModel
    success_url = reverse_lazy("reservation")
    template_name = "remove_template/reservation_remove.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully deleted reservation, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class DeleteTruckView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "truck_id"
    model = TruckModel
    success_url = reverse_lazy("truck")
    template_name = "remove_template/truck_remove.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully deleted truck information, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class CreateUserView(CustomLoginRequiredMixin, CreateView):
    model = CustomUserModel
    form_class = UserForm
    success_url = reverse_lazy("users")
    template_name = "create_template/user_create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            "You have successfully added new user, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class UserView(CustomLoginRequiredMixin, ListView):
    template_name = "views_template/user_view.html"
    model = CustomUserModel
    context_object_name = "users"


class UpdateUserView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "user_id"
    form_class = UpdateUserForm
    model = CustomUserModel
    success_url = reverse_lazy("users")
    template_name = "update_template/user_update.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully updated user information, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class DeleteUserView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "user_id"
    model = CustomUserModel
    success_url = reverse_lazy("users")
    template_name = "remove_template/user_remove.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(
            self.request,
            "You have successfully deleted user information, thank you.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


def generate_report(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")

        from django.utils import timezone

        start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        start_date = (
            timezone.make_aware(start_date)
            if start_date and timezone.is_naive(start_date)
            else start_date
        )
        end_date = (
            timezone.make_aware(end_date)
            if end_date and timezone.is_naive(end_date)
            else end_date
        )

        query_reservation = ReservationModel.objects.filter(
            date_added__range=[start_date, end_date],
        ).order_by("-reserved_by__first_name")

        if not query_reservation.exists():
            messages.error(
                request,
                "No reservation from the given date range, please try again.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("reservation_report"))

        grouped_reservations = defaultdict(list)
        for reservation in query_reservation:
            grouped_reservations[reservation.reserved_by.get_full_name()].append(
                reservation
            )

        buffer = BytesIO()
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="reservation_report.pdf"'

        left_margin = 1 * inch
        right_margin = 1 * inch
        top_margin = 0
        bottom_margin = 1 * inch

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
        )
        doc.title = "Sta. Catalina Cooperative Reservation Report"

        elements = []

        styles = getSampleStyleSheet()
        header_style = styles["Heading2"]
        header_style.alignment = 1

        current_date = datetime.now().strftime("%Y-%m-%d")
        header = Paragraph(
            f"Sta. Catalina Cooperative Reservation<br/>Booking Activity Report<br/><small>{current_date}</small>",
            header_style,
        )
        elements.append(header)
        elements.append(Spacer(1, 0.2 * inch))

        data = [
            [
                "Fullname",
                "Contact",
                "Product Name",
                "Member in COOP",
                "Delivery Status",
                "Status",
                "Date Reserved",
            ]
        ]

        table_styles = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightcyan),
            ("GRID", (0, 0), (-1, -1), 1, colors.darkblue),
        ]

        row_idx = 1
        for name, reservations in grouped_reservations.items():
            reservation_count = len(reservations)

            data.append(
                [
                    name,
                    reservations[0].reserved_by.phone_number,
                    reservations[0].product_name,
                    "Member" if reservations[0].date_reserved else "Non Member",
                    "Delivered" if reservations[0].is_delivered else "Undelivered",
                    reservations[0].reservation_status,
                    (
                        reservations[0].date_reserved.strftime("%Y-%m-%d")
                        if reservations[0].date_reserved
                        else "N/A"
                    ),
                ]
            )

            for reservation in reservations[1:]:
                data.append(
                    [
                        "",
                        "",
                        reservation.product_name,
                        "Member" if reservation.date_reserved else "Non Member",
                        "Delivered" if reservation.is_delivered else "Undelivered",
                        reservation.reservation_status,
                        (
                            reservation.date_reserved.strftime("%Y-%m-%d")
                            if reservation.date_reserved
                            else "N/A"
                        ),
                    ]
                )

            table_styles.append(
                ("SPAN", (0, row_idx), (0, row_idx + reservation_count - 1))
            )
            table_styles.append(
                ("SPAN", (1, row_idx), (1, row_idx + reservation_count - 1))
            )

            table_styles.append(
                ("VALIGN", (0, row_idx), (0, row_idx + reservation_count - 1), "MIDDLE")
            )
            table_styles.append(
                ("VALIGN", (1, row_idx), (1, row_idx + reservation_count - 1), "MIDDLE")
            )

            row_idx += reservation_count

        table = Table(data)
        table.setStyle(TableStyle(table_styles))
        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        response.write(buffer.read())
        return response
