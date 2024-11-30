from django.urls import path
from manager.views import *

urlpatterns = [
    path('', ManagerView.as_view(), name="manager_page"),
]