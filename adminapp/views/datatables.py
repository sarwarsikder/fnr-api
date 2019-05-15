from django.db.models import Case, Value, When, Count
from django.db.models.functions import Concat

from adminapp.models import Users
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
        return Users.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(is_active=1).exclude(id=self.request.user.id)

