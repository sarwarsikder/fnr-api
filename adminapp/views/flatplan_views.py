from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from adminapp.forms.flatplans_form import FlatPlansForm
from adminapp.models import FlatPlans
from adminapp.models import Users

import json

from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper


class FlatPlansView(generic.DetailView):
    def get(self, request):
        response = {}
        if request.user.is_superuser:
            flatplans = FlatPlans.objects.all()
            response['buildingPlans'] = flatplans
            return render(request, 'flats/plans.html', response)
        else:
            redirect('index')

    # def delete(request):
    #     response = {}
    #     if CommonView.superuser_login(request):
    #         try:
    #             building_plan_id = request.POST.get('id')
    #             BuildingPlans.objects.get(id=building_plan_id).delete()
    #             response['success'] = True
    #             response['message'] = "Buildings delete successfully"
    #             return HttpResponseRedirect('/building-plan/')
    #         except Exception as e:
    #             LogHelper.elog(e)
    #             response['success'] = False
    #             response['message'] = "Something went wrong. Please try again"
    #     return HttpResponse(json.dumps(response), content_type='application/json')

class FlatPlansAddView(generic.DetailView):
    form_class = FlatPlansForm
    template_name = 'flats/add_plans.html'

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
                    return HttpResponseRedirect('/flat-plan/')
                else:
                    return render(request, self.template_name, response)
            except Exception as e:
                LogHelper.efail(e)
                return render(request, self.template_name, response)
        else:
            return redirect('index')


class BuildingPlansUpdateView(UpdateView):
    form_class = FlatPlansForm
    template_name = 'flats/edit_plans.html'
    model = FlatPlans

    def get(self, request, pk):
        if request.user.is_superuser:
            response = {}
            form = self.form_class
            data = FlatPlans.objects.filter(id=pk)
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
        return reverse_lazy('flat-plan')

    def get_context_data(self, **kwargs):
        context = super(BuildingPlansUpdateView, self).get_context_data(**kwargs)
        return context
