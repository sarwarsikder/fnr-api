from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from adminapp.forms.component_form import ComponentForm
from adminapp.models import Components
from adminapp.models import Users

import json

from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper


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

class ComponentAddView(generic.DetailView):
    form_class = ComponentForm
    template_name = 'components/add_component.html'
    def get(self, request):
        if request.user.is_superuser:
            response = {}
            form = self.form_class
            parents = Components.objects.filter(parent__isnull=True)
            response['parents'] = parents
            response['form'] = form
            return render(request, self.template_name, response)
        else:
            redirect('index')

    def post(self, request, *args, **kwargs):
        print(request.session['supplementer_user'])
        if CommonView.superuser_login(request):
            response = {}
            print("in super user!!")
            form = self.form_class(request.POST)
            form.created_by = request.user

            parents = Components.objects.filter(parent__isnull=True)
            response['parents'] = parents
            response['form'] = form
            print("form posted!!")
            try:
                print("in valid!!")
                print(form)
                if form.is_valid():
                    print("form valid!!")
                    form.save(request=request)
                    return HttpResponseRedirect('/components/')
                else:
                    print("form not valid!!")
                    return render(request, self.template_name, response)
            except Exception as e:
                print(e)
                LogHelper.efail(e)
                return render(request, self.template_name, response)
        else:
            return redirect('index')