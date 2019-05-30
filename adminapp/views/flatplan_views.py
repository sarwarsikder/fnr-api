from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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
    def get_all_plans_by_active_flat(request):
        response = {}
        try:
            flat_id = request.session['active_flat']['id']
            if 'flat_id' in request.POST:
                flat_id = request.POST.get('flat_id')
            plans = FlatPlans.objects.filter(flat_id=flat_id)
            plan_list_tab = render_to_string('flats/plan.html', {"plans": plans, "flat_id": flat_id})
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
            flat_plan_id = request.POST.get('id')
            FlatPlans.objects.get(id=flat_plan_id).delete()
            response['success'] = True
            response['message'] = "Flat delete successfully"
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')


class FlatPlansAddView(generic.DetailView):
    form_class = FlatPlansForm
    template_name = 'flats/add_plans.html'

    def get(self, request, *args, **kwargs):
        flat_id = kwargs['flat_id']
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'flat_id': flat_id})

    def post(self, request, *args, **kwargs):
        response = {}
        form = self.form_class(request.POST, request.FILES)
        form.created_by = request.user
        response['form'] = form
        flat_id = kwargs['flat_id']
        request.flat_id = flat_id
        response['flat_id'] = flat_id
        try:
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('/flats/'+str(flat_id)+'/tasks/#plans')
            else:
                return render(request, self.template_name, response)
        except Exception as e:
            LogHelper.efail(e)
            return render(request, self.template_name, response)


# class FlatPlansUpdateView(UpdateView):
#     form_class = FlatPlansForm
#     template_name = 'flats/edit_plans.html'
#     model = FlatPlans
#
#     def get(self, request, pk):
#         if request.user.is_superuser:
#             response = {}
#             form = self.form_class
#             data = FlatPlans.objects.filter(id=pk)
#             response['data'] = data[0]
#             response['form'] = form
#             response['pk'] = pk
#             return render(request, self.template_name, response)
#         else:
#             redirect('index')
#
#     def form_valid(self, form):
#         if CommonView.superuser_login(self.request):
#             form.update(request=self.request)
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return redirect('index')
#
#     def get_success_url(self):
#         return reverse_lazy('flat-plan')
#
#     def get_context_data(self, **kwargs):
#         context = super(FlatPlansUpdateView, self).get_context_data(**kwargs)
#         return context
