import json
import random, string

from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from adminapp.views.mail import MailHelper
from adminapp.views.helper import LogHelper
from adminapp.models import Components, Projects, BuildingComponents, Tasks, QrCode, Buildings, Flats
from django.db.models import Q, Count
import qrcode
import io


class IndexView(generic.DetailView):
    def get(self, request):
        return render(request, 'dashboard/index.html', {})


class CommonView(generic.DetailView):

    def sendEmail(request, template, context, subject, to, user_id=None):
        response = {}
        try:
            context["request"] = request
            context["base_url"] = settings.SITE_URL
            context["project_title"] = settings.PROJECT_TITLE
            mail_template_content = render_to_string(template, context)
            sender_mail = settings.EMAIL_HOST_USER
            # if user_id:
            #     CommonHelper.set_history(user_id=user_id, subject=subject, type="email")
            import threading
            task = threading.Thread(target=MailHelper.mail_send, args=(mail_template_content, subject, to, sender_mail))
            task.start()
            response['success'] = True
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
        return HttpResponse(json.dumps(response), content_type='application/json')

    def common_datatable_context(self):
        show_entries = 10
        sorted_column = 0
        sorting_order = 'asc'
        context = {
            'show_entries': show_entries,
            'sorting_order': sorting_order,
            'sorted_column': sorted_column
        }
        return context

    def get_file_path(file):
        file = str(file)
        file_path = ""
        try:
            print(settings.MEDIA_URL)
            # path = file.split("adminapp/")[1]
            file_path = settings.MEDIA_URL+file
            print(file_path)
        except Exception as e:
            LogHelper.elog(e)
        return file_path

    def get_all_main_component(request):
        components = Components.objects.filter(parent__isnull=True)
        return components

    def superuser_login(request):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False

    def get_all_projects(request):
        projects = Projects.objects.all()
        return projects

    def create_default_building_components(request, building):
        try:
            default_components = Components.objects.filter(Q(type__isnull=True) | Q(type=building.grundung) | Q(type=building.aussenwande_eg_og_dg) | Q(type=building.fenster_beschattung) | Q(type=building.dach)).filter(building=True)
            building_components = []
            for component in default_components:
                component_form = {
                    "description": component.static_description,
                    "building": building,
                    "created_by": request.user,
                    "updated_by": request.user,
                    "component": component
                }
                building_components.append(BuildingComponents(**component_form))
            BuildingComponents.objects.bulk_create(building_components)
            return True
        except Exception as e:
            LogHelper.efail(e)
            return False

    def create_default_flat_components(request, flat):
        try:
            default_components = Components.objects.filter(flat=True)
            flat_components = []
            for component in default_components:
                component_form = {
                    "description": component.static_description,
                    "flat": flat,
                    "building": flat.building,
                    "created_by": request.user,
                    "updated_by": request.user,
                    "component": component
                }
                flat_components.append(BuildingComponents(**component_form))
            BuildingComponents.objects.bulk_create(flat_components)
            return True
        except Exception as e:
            LogHelper.efail(e)
            return False

    def create_default_tasks(request, components):
        try:
            task_list = []
            for component in components:
                task_flag = False
                if component.component.parent:
                    task_flag = True
                elif not Components.objects.filter(parent_id=component.component.id).exists():
                    task_flag = True
                if task_flag:
                    task_form = {
                        "building_component": component,
                        "created_by": request.user,
                        "updated_by": request.user
                    }
                    task_list.append(Tasks(**task_form))
            Tasks.objects.bulk_create(task_list)
            return True
        except Exception as e:
            LogHelper.efail(e)
            return False

    def generate_qr_code(request, building, flat=None):
        unique_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        qr_form = {
            "unique_key": unique_key,
            "building": building,
            "flat": flat,
            "created_by": request.user,
        }
        qr_code = QrCode(**qr_form)
        qr_code.save()
        return qr_code


class QRResponse(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            qr_id = kwargs['qr_id']
            qr_info = QrCode.objects.get(id=qr_id)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2
            )
            qr.add_data(qr_info.unique_key)
            qr.make(fit=True)
            img = qr.make_image()
            output = io.BytesIO()
            img.save(output, format='PNG')
            output.seek(0)
            output_s = output.read()
            return HttpResponse(output_s, content_type="image/png")
        except Exception as e:
            LogHelper.efail(e)
            return HttpResponse("", content_type="image/png")


class CurrentProjects(generic.DetailView):
    def get_all_current_buildings(request):
        response = {}
        try:
            project_id = request.POST.get('project_id')
            change_project = request.POST.get('change_project')
            CurrentProjects.change_active_project(request, project_id)
            buildings = Buildings.objects.annotate(total_flats=Count('flats')).filter(project_id=project_id)
            if change_project == 'true':
                building_list_tab = render_to_string('profiles/buildings.html', {"buildings": buildings, "request": request})
                response['building_list_tab'] = building_list_tab
            current_buildings = []
            for building in buildings:
                current_buildings.append({'id': building.id, 'number': building.display_number})
            response['success'] = True
            response['current_buildings'] = current_buildings
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get_all_current_flats(request):
        response = {}
        try:
            building_id = request.session["active_building"]['id']
            flats = Flats.objects.filter(building_id=building_id)
            current_flats = []
            for flat in flats:
                current_flats.append({'id': flat.id, 'number': flat.number})
            response['success'] = True
            response['current_flats'] = current_flats
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def change_active_project(request, project_id):
        try:
            request.session['active_project']['id'] = project_id
            request.session['active_project']['name'] = Projects.objects.get(id=project_id).name
            request.session.modified = True
            CurrentProjects.change_active_building(request, project_id, True)
            if request.user.current_activity:
                current_activity = json.loads(request.user.current_activity)
                current_activity['project_id'] = request.session['active_project']['id']
                current_activity['project_name'] = request.session['active_project']['name']
                current_activity['building_id'] = request.session['active_building']['id']
                current_activity['building_number'] = request.session['active_building']['number']
                current_activity['flat_id'] = request.session['active_flat']['id']
                current_activity['flat_number'] = request.session['active_flat']['number']
                request.user.current_activity = json.dumps(current_activity)
                request.user.save()
            else:
                current_activity = {
                    'project_id': request.session['active_project']['id'],
                    'project_name': request.session['active_project']['name'],
                    'building_id': request.session['active_building']['id'],
                    'building_number': request.session['active_building']['number'],
                    'flat_id': request.session['active_flat']['id'],
                    'flat_number': request.session['active_flat']['number']
                }
                request.user.current_activity = json.dumps(current_activity)
                request.user.save()
        except Exception as e:
            LogHelper.efail(e)
        return True

    def change_active_building(request, project_id, change_project=False):
        try:
            if project_id:
                current_building = Buildings.objects.filter(project_id=project_id).first()
                request.session["active_building"]['id'] = current_building.id
                request.session["active_building"]['number'] = current_building.display_number
                request.session.modified = True
                if not change_project:
                    if request.user.current_activity:
                        current_activity = json.loads(request.user.current_activity)
                        current_activity['building_id'] = request.session['active_building']['id']
                        current_activity['building_number'] = request.session['active_building']['number']
                        request.user.current_activity = json.dumps(current_activity)
                        request.user.save()
                    else:
                        current_activity = {
                            'building_id': request.session['active_building']['id'],
                            'building_number': request.session['active_building']['number']
                        }
                        request.user.current_activity = json.dumps(current_activity)
                        request.user.save()
                CurrentProjects.change_active_flat(request, request.session["active_building"]['id'], True)
        except Exception as e:
            LogHelper.efail(e)
            request.session["active_building"]['id'] = ''
            request.session["active_building"]['number'] = ''
            request.session.modified = True
        return True

    def change_active_flat(request, building_id, change_building=False):
        try:
            if building_id:
                current_flat = Flats.objects.filter(building_id=building_id).first()
                request.session["active_flat"]['id'] = current_flat.id
                request.session["active_flat"]['number'] = current_flat.number
                request.session.modified = True
                if not change_building:
                    if request.user.current_activity:
                        current_activity = json.loads(request.user.current_activity)
                        current_activity['flat_id'] = request.session['active_flat']['id']
                        current_activity['flat_number'] = request.session['active_flat']['number']
                        request.user.current_activity = json.dumps(current_activity)
                        request.user.save()
                    else:
                        current_activity = {
                            'flat_id': request.session['active_flat']['id'],
                            'flat_number': request.session['active_flat']['number']
                        }
                        request.user.current_activity = json.dumps(current_activity)
                        request.user.save()
            else:
                request.session["active_flat"]['id'] = ''
                request.session["active_flat"]['number'] = ''
                request.session.modified = True
        except Exception as e:
            LogHelper.efail(e)
            request.session["active_flat"]['id'] = ''
            request.session["active_flat"]['number'] = ''
            request.session.modified = True
        return True

    def get_all_buildings_by_active_project(request):
        response = {}
        try:
            project_id = request.session['active_project']['id']
            buildings = Buildings.objects.annotate(total_flats=Count('flats')).filter(project_id=project_id)
            building_list_tab = render_to_string('profiles/buildings.html', {"buildings": buildings, "request": request})
            response['building_list_tab'] = building_list_tab
            response['success'] = True
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get_all_flats_by_active_building(request):
        response = {}
        try:
            building_id = request.session['active_building']['id']
            flats = Flats.objects.annotate(total_tasks=Count('buildingcomponents__tasks')).filter(building_id=building_id)
            flat_list_tab = render_to_string('profiles/flats.html', {"flats": flats, "request": request})
            response['flat_list_tab'] = flat_list_tab
            response['success'] = True
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')








