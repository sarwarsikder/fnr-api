from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from adminapp.forms.buildingplans_form import BuildingPlansForm
from adminapp.models import BuildingPlans
from adminapp.models import Users

import json

from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper


class BuildingPlansView(generic.DetailView):

    def get_all_plans_by_active_building(request):
        response = {}
        try:
            building_id = request.session['active_building']['id']
            if 'building_id' in request.POST:
                building_id = request.POST.get('building_id')
            plans = BuildingPlans.objects.filter(building_id=building_id)
            plan_list_tab = render_to_string('buildings/plan.html', {"plans": plans, "building_id": building_id})
            response['plan_list_tab'] = plan_list_tab
            response['success'] = True
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def delete(request):
        response = {}
        try:
            building_plan_id = request.POST.get('id')
            BuildingPlans.objects.get(id=building_plan_id).delete()
            response['success'] = True
            response['message'] = "Buildings Plan delete successfully"
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')


class BuildingPlansAddView(generic.DetailView):
    form_class = BuildingPlansForm
    template_name = 'buildings/add_plans.html'

    def get(self, request, *args, **kwargs):
        building_id = kwargs['building_id']
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'building_id': building_id})

    def post(self, request, *args, **kwargs):
        response = {}
        form = self.form_class(request.POST, request.FILES)
        response['form'] = form
        building_id = kwargs['building_id']
        request.building_id = building_id
        response['building_id'] = building_id
        try:
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('/current-project-flats/')
            else:
                return render(request, self.template_name, response)
        except Exception as e:
            LogHelper.efail(e)
            return render(request, self.template_name, response)


# class BuildingPlansUpdateView(UpdateView):
#     form_class = BuildingPlansForm
#     template_name = 'buildings/edit_plans.html'
#     model = BuildingPlans
#
#     def get(self, request, pk):
#         print("Got Update!!")
#         if request.user.is_superuser:
#             response = {}
#             form = self.form_class
#             data = BuildingPlans.objects.filter(id=pk)
#             response['data'] = data[0]
#             response['form'] = form
#             response['planID'] = pk
#             return render(request, self.template_name, response)
#
#         else:
#             redirect('index')
#
#     def form_valid(self, form):
#         if CommonView.superuser_login(self.request):
#
#             form.update(request=self.request)
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return redirect('index')
#
#     def get_success_url(self):
#         return reverse_lazy('building-plan')
#
#     def get_context_data(self, **kwargs):
#         context = super(BuildingPlansUpdateView, self).get_context_data(**kwargs)
#         return context
