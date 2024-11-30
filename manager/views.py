from django.shortcuts import render
from django.views import View

class ManagerView(View):
    template_name = 'manager_index.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        pass