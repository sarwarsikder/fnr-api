import json

import qrcode
from django.db.models import Q
from django.template.loader import render_to_string
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from adminapp.models import Tasks, BuildingComponents, Buildings, Flats
from adminapp.views.helper import LogHelper


class TasksView(generic.DetailView):
    def get_all_building_tasks(request, *args, **kwargs):
        try:
            building_id = kwargs['building_id']
            building = Buildings.objects.get(id=building_id)
            return render(request, 'tasks/task_list.html', {'building': building})
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def get_all_flat_tasks(request, *args, **kwargs):
        try:
            flat_id = kwargs['flat_id']
            flat = Flats.objects.get(id=flat_id)
            return render(request, 'tasks/task_list.html', {'flat': flat})
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def get_pending_components(request):
        response = {}
        try:
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
                components = BuildingComponents.objects.filter(building_id=building_id, flat__isnull=True,
                                                               component__parent__isnull=True)
            elif 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
                components = BuildingComponents.objects.filter(flat_id=flat_id, component__parent__isnull=True)
            components_list = render_to_string('tasks/pending_components.html', {"components": components, "request": request})
            response['success'] = True
            response['components_list'] = components_list
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get_done_components(request):
        response = {}
        try:
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
                components = BuildingComponents.objects.filter(building_id=building_id, flat__isnull=True,
                                                               component__parent__isnull=True)
            elif 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
                components = BuildingComponents.objects.filter(flat_id=flat_id, component__parent__isnull=True)
            components_list = render_to_string('tasks/done_components.html', {"components": components, "request": request})
            response['success'] = True
            response['components_list'] = components_list
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get_all_components(request):
        response = {}
        try:
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
                components = BuildingComponents.objects.filter(building_id=building_id, flat__isnull=True,
                                                               component__parent__isnull=True)
            elif 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
                components = BuildingComponents.objects.filter(flat_id=flat_id, component__parent__isnull=True)
            components_list = render_to_string('tasks/all_components.html', {"components": components, "request": request})
            response['success'] = True
            response['components_list'] = components_list
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get_component_tasks(request):
        response = {}
        try:
            type = request.POST.get('type')
            component_id = request.POST.get('id')
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
                if type == 'pending':
                    tasks = Tasks.objects.filter(building_component__building_id=building_id, building_component__flat__isnull=True).filter(Q(Q(building_component__component__parent_id=component_id) | Q(building_component__component_id=component_id))).exclude(status='done')
                elif type == 'done':
                    tasks = Tasks.objects.filter(building_component__building_id=building_id,
                                                 building_component__flat__isnull=True, status='done').filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
                else:
                    tasks = Tasks.objects.filter(building_component__building_id=building_id,
                                                 building_component__flat__isnull=True).filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
            elif 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
                if type == 'pending':
                    tasks = Tasks.objects.filter(building_component__flat_id=flat_id).filter(Q(Q(building_component__component__parent_id=component_id) | Q(building_component__component_id=component_id))).exclude(status='done')
                elif type == 'done':
                    tasks = Tasks.objects.filter(building_component__flat_id=flat_id, status='done').filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
                else:
                    tasks = Tasks.objects.filter(building_component__flat_id=flat_id).filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
            tasks_list = render_to_string('tasks/task.html', {"tasks": tasks, "request": request})
            response['success'] = True
            response['tasks_list'] = tasks_list
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

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







