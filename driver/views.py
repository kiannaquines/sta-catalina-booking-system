from django.shortcuts import render
from django.views.generic import View


class DriverPage(View):
    template_name = 'driver_index.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass