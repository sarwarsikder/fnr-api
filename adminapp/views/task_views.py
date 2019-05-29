import json

import qrcode
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from adminapp.models import Tasks
from adminapp.views.helper import LogHelper


class TasksView(generic.DetailView):
    def get_all_building_tasks(request, *args, **kwargs):
        try:
            building_id = kwargs['building_id']

            return render(request, 'tasks/task_list.html', {})
        except Exception as e:
            LogHelper.efail(e)
            return redirect('index')







