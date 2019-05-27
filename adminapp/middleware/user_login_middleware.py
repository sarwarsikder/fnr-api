import json

import requests
from django.views import generic
from adminapp.models import Users, Projects, Buildings, Flats
from adminapp.views.common_views import CommonView
import os.path
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import resolve


class UserLoginMiddleware(generic.DetailView):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.split('/')[1]
        # user = authenticate(username='admin', password='wsit97480')
        # logout(request)
        # if user is not None:
        #     login(request, user)
        # request.user = Users.objects.get(id=1)
        if path == '' or path != 'api':
            print(request.is_ajax())
            if request.is_ajax() == False:
                settings.USE_TZ = False
                browser_current_url = resolve(request.path_info).url_name
                # if 'bikeshare_settings' not in request.session:
                #     request.session["bikeshare_settings"] = CommonView.getCommonSettings(request)
                if browser_current_url != 'login' and browser_current_url != 'forget-password' and browser_current_url != 'reset-password':
                    if not request.user.is_authenticated:
                        return redirect('login')
                    current_projects = list(Projects.objects.filter(is_complete=False).order_by('-id').values('id', 'name'))
                    request.session["current_projects"] = current_projects
                    if 'active_project' not in request.session:
                        request.session["active_project"] = current_projects[0]['id']
                    if 'active_building' not in request.session:
                        try:
                            request.session["active_building"] = Buildings.objects.filter(project_id=request.session["active_project"]).first().id
                        except Exception as e:
                            print(e)
                    if 'active_flat' not in request.session:
                        try:
                            request.session["active_flat"] = Flats.objects.filter(building_id=request.session["active_building"]).first().id
                        except Exception as e:
                            print(e)
                    request.session.modified = True
        # elif path != 'api':
        #     if request.is_ajax() == False:
        #         if 'user_bikeshare_settings' not in request.session:
        #             response = requests.get(settings.API_URL+"/settings/")
        #             default_settings = json.loads(response._content)
        #             request.session["user_bikeshare_settings"] = default_settings
        #             request.session.modified = True
        #         if 'is_user_login' in request.session and request.session['is_user_login']:
        #             print("logged in")
        #         else:
        #             return redirect('user-login')
        return self.get_response(request)

    def process_response(self, request, response):
        path = request.path.split('/')[1]
        response['Pragma'] = 'no-cache'
        if path == 'admin' or path == '':
            response['Cache-Control'] = 'no-cache must-revalidate proxy-revalidate'
        else:
            response['Cache-Control'] = 'no-cache, max-age=0, must-revalidate, no-store'
        return response

