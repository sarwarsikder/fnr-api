from django.shortcuts import render
from django.views import generic


class StaffView(generic.DetailView):
    def get(self, request):
        return render(request, 'staffs/list.html', {})
