from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from adminapp.forms.projectplan_form import ProjectPlansForm
from adminapp.models import Users, ProjectPlans

import json

from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper


class ProjectPlansView(generic.DetailView):

    def get_all_plans_by_active_project(request):
        response = {}
        try:
            project_id = request.session['active_project']['id']
            if 'project_id' in request.POST:
                project_id = request.POST.get('project-id')
            plans = ProjectPlans.objects.filter(project_id=project_id)
            plan_list_tab = render_to_string('projects/plan.html', {"plans": plans})
            response['plan_list_tab'] = plan_list_tab
            response['success'] = True
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def delete(request):
        response = {}
        if CommonView.superuser_login(request):
            try:
                flat_plan_id = request.POST.get('id')
                ProjectPlans.objects.get(id=flat_plan_id).delete()
                response['success'] = True
                response['message'] = "Project delete successfully"
                return HttpResponseRedirect('/project-plan/')
            except Exception as e:
                LogHelper.elog(e)
                response['success'] = False
                response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')


class ProjectPlansAddView(generic.DetailView):
    form_class = ProjectPlansForm
    template_name = 'projects/add_plans.html'

    def get(self, request):
        if request.user.is_superuser:
            response = {}
            form = self.form_class
            response['form'] = form
            return render(request, self.template_name, response)
        else:
            redirect('index')

    def post(self, request, *args, **kwargs):
        print(request.session['supplementer_user'])
        if CommonView.superuser_login(request):
            response = {}
            form = self.form_class(request.POST, request.FILES)
            form.created_by = request.user
            response['form'] = form
            try:
                if form.is_valid():
                    form.save(request=request)
                    return HttpResponseRedirect('/project-plan/')
                else:
                    return render(request, self.template_name, response)
            except Exception as e:
                LogHelper.efail(e)
                return render(request, self.template_name, response)
        else:
            return redirect('index')


class ProjectPlansUpdateView(UpdateView):
    form_class = ProjectPlansForm
    template_name = 'projects/edit_plans.html'
    model = ProjectPlans

    def get(self, request, pk):
        if request.user.is_superuser:
            response = {}
            form = self.form_class
            data = ProjectPlans.objects.filter(id=pk)
            response['data'] = data[0]
            response['form'] = form
            response['pk'] = pk
            return render(request, self.template_name, response)
        else:
            redirect('index')

    def form_valid(self, form):
        if CommonView.superuser_login(self.request):
            form.update(request=self.request)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return redirect('index')

    def get_success_url(self):
        return reverse_lazy('project-plan')

    def get_context_data(self, **kwargs):
        context = super(ProjectPlansUpdateView, self).get_context_data(**kwargs)
        return context
