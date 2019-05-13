from django.shortcuts import render
from django.views import generic


class ProjectView(generic.DetailView):
    def get(self, request):
        return render(request, 'projects/list.html', {})
