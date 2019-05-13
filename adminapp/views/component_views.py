from django.shortcuts import render
from django.views import generic


class ComponentView(generic.DetailView):
    def get(self, request):
        return render(request, 'components/list.html', {})
