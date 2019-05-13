from django.shortcuts import render
from django.views import generic


class CompanyView(generic.DetailView):
    def get(self, request):
        return render(request, 'companies/list.html', {})
