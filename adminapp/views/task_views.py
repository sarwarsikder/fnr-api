import json
from django.db.models import Q
from django.template.loader import render_to_string
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render, redirect
from adminapp.models import Tasks, BuildingComponents, Buildings, Flats, HandWorker, Users
from adminapp.views.helper import LogHelper
from adminapp.views.common_views import CurrentProjects


class TasksView(generic.DetailView):
    def get_all_building_tasks(request, *args, **kwargs):
        try:
            building_id = kwargs['building_id']
            building = Buildings.objects.get(id=building_id)
            if str(building.project_id) == request.session['active_project']['id']:
                CurrentProjects.change_active_building(request, building_id)
            return render(request, 'tasks/task_list.html', {'building': building})
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def get_all_flat_tasks(request, *args, **kwargs):
        try:
            flat_id = kwargs['flat_id']
            flat = Flats.objects.get(id=flat_id)
            if str(flat.building_id) == request.session['active_building']['id']:
                CurrentProjects.change_active_flat(request, flat_id)
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

    def get_handwerker_list(request):
        response = {}
        try:
            component_id = request.POST.get('component_id')
            handworker_list = []
            handworkers = HandWorker.objects.values('user__avatar','user__first_name', 'user__last_name', 'user_id').filter(user__is_active=True, working_type__contains={"id":component_id})
            for handworker in handworkers:
                data = {
                    # "avatar": handworker['user__avatar'],
                    "text": handworker['user__first_name'] + " " +handworker['user__last_name'],
                    "id": handworker['user_id'],
                }
                handworker_list.append(data)
            response['success'] = True
            response['handworkers'] = handworker_list
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def assign_handwerker(request):
        response = {}
        try:
            component_id = request.POST.get('component_id')
            user_id = request.POST.get('user_id')
            BuildingComponents.objects.filter(id=component_id).update(assign_to_id=user_id, assigned_by=request.user)
            handworker = Users.objects.get(id=user_id)
            handworker_info = {
                "fullname": handworker.get_full_name(),
                "avatar": handworker.avatar.url if handworker.avatar else ''
            }
            response['success'] = True
            response['handworker'] = handworker_info
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')







