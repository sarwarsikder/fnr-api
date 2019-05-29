import json

import qrcode
from django.db.models import Q
from django.template.loader import render_to_string
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from adminapp.models import Tasks, BuildingComponents
from adminapp.views.helper import LogHelper


class TasksView(generic.DetailView):
    def get_all_building_tasks(request, *args, **kwargs):
        try:
            return render(request, 'tasks/task_list.html')
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def get_active_tasks(request):
        response = {}
        try:
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
                components = BuildingComponents.objects.filter(building_id=building_id, flat__isnull=True, component__parent__isnull=True)
                for component in components:
                    component.tasks = Tasks.objects.filter(building_component__building_id=building_id, building_component__flat__isnull=True).filter(Q(Q(building_component__component__parent_id=component.component_id) | Q(building_component__component_id=component.component_id))).exclude(status='done')
            elif 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
                components = BuildingComponents.objects.filter(flat_id=flat_id, component__parent__isnull=True)
                for component in components:
                    component.tasks = Tasks.objects.filter(building_component__component__parent_id=component.component_id).exclude(status='done')
            active_tasks = render_to_string('tasks/task.html', {"components": components, "request": request})
            response['success'] = True
            response['active_tasks'] = active_tasks
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')







