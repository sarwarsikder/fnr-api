from django.shortcuts import render, redirect
from django.views import generic
from adminapp.models import Components
import json


class ComponentView(generic.DetailView):
    def get(self, request):
        response = {}
        if request.user.is_superuser:
            components = Components.objects.filter(parent__isnull=True)
            for component in components:
                component.sub_components = Components.objects.filter(parent_id=component.id)
            response['components'] = components
            # return render(request, 'components/list.html', {})
            return render(request, 'components/component.html', response)
        else:
            redirect('index')
