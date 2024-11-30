from typing import Any
from django.views.generic import ListView

from app.mixins import CustomLoginRequiredMixin
from app.models import ReservationModel


class ManagerView(CustomLoginRequiredMixin, ListView):
    template_name = "manager_index.html"
    model = ReservationModel
    context_object_name = "reservations"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reservations"] = ReservationModel.objects.all()
        return super().get_context_data(**kwargs)