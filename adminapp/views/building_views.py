import json

import qrcode
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from adminapp.models import Buildings, BuildingComponents, Components, Projects, QrCode
from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper
from adminapp.forms.building_form import BuildingForm
from django.conf import settings
import io


class BuildingsView(generic.DetailView):
    def get(self, request, *args, **kwargs):
        try:
            project_id = kwargs['project_id']
            context = CommonView.common_datatable_context(self)
            context['project_id'] = project_id
            project = Projects.objects.get(id=project_id)
            context['project'] = project
            return render(request, 'buildings/building.html', context)
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def preview_qr(request, pk):
        try:
            context = {}
            qr_info = QrCode.objects.filter(building_id=pk, flat__isnull=True).select_related('building').first()
            context['qr_info'] = qr_info
            return render(request, 'buildings/preview_qr.html', context)
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')

    def delete(request):
        response = {}
        try:
            building_id = request.POST.get('id')
            Buildings.objects.get(id=building_id).delete()
            response['success'] = True
            response['message'] = "Hause deleted successfully"
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')


class BuildingFormView(View):
    form_class = BuildingForm
    template_name = 'buildings/add_building.html'

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'project_id': project_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                project_id = kwargs['project_id']
                request.project_id = project_id
                obj = form.save(request=request)
                default_components = CommonView.create_default_building_components(request, obj)
                qr = CommonView.generate_qr_code(request, obj)
                if default_components:
                    building_components = BuildingComponents.objects.filter(building_id=obj.id, flat__isnull=True)
                    default_tasks = CommonView.create_default_tasks(request, building_components)
                return HttpResponseRedirect('/projects/'+str(obj.project_id)+'/buildings/')
        except Exception as e:
            LogHelper.efail(e)
        return render(request, self.template_name, {'form': form})


class BuildingUpdateView(UpdateView):
    model = Buildings
    template_name = 'buildings/edit_building.html'
    form_class = BuildingForm

    def form_valid(self, form):
        form.update(request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('buildings', kwargs={'project_id': self.object.project_id})

    def get_context_data(self, **kwargs):
        context = super(BuildingUpdateView, self).get_context_data(**kwargs)
        return context




