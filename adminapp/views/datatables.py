from django.db.models import Case, Value, When, Count
from django.db.models.functions import Concat

from adminapp.models import Users, HandWorker, Projects, Buildings
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db import connection
from django.template.loader import render_to_string
from datetime import datetime, timedelta, date
from django.db.models import Q


class StaffListView(BaseDatatableView):
    model = Users
    columns = ['id', 'username', 'full_name', 'email', 'is_active']
    order_columns = ['id', 'username', 'full_name', 'email', 'is_active']

    def get_initial_queryset(self):
        return Users.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(is_staff=True).exclude(id=self.request.user.id).exclude(is_superuser=True)


class CompanyListView(BaseDatatableView):
    model = HandWorker
    columns = ['user.id', 'company_name', 'user.username', 'full_name', 'user.email', 'user.is_active', 'telephone']
    order_columns = ['user.id', 'company_name', 'user.username', 'full_name', 'user.email', 'user.is_active', 'telephone']

    def get_initial_queryset(self):
        return HandWorker.objects.annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name')).all()


class ProjectListView(BaseDatatableView):
    model = Projects
    columns = ['id', 'name', 'city', 'type', 'start_date', 'end_date', 'user_type']
    order_columns = ['id', 'name', 'city', 'type', 'start_date', 'end_date']

    def get_initial_queryset(self):
        if self.request.user.is_superuser:
            return Projects.objects.all()
        else:
            return Projects.objects.annotate(user_type=Case(When(projectstuff__user__is_superuser=True, then='projectstuff__user__is_superuser'), default='projectstuff__user__is_superuser')).filter(projectstuff__user_id=self.request.user.id)


class BuildingListView(BaseDatatableView):
    model = Buildings
    columns = ['id', 'hause_number', 'display_number', 'description']
    order_columns = ['id', 'hause_number', 'display_number', 'description']

    def get_initial_queryset(self):
        project_id = self.request.GET.get('project_id')
        return Buildings.objects.filter(project_id=project_id)
