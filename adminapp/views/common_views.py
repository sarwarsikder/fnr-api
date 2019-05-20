import json
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from adminapp.views.mail import MailHelper
from adminapp.views.helper import LogHelper
from adminapp.models import Components
from django.contrib.auth.decorators import login_required, user_passes_test


class IndexView(generic.DetailView):
    def get(self, request):
        return render(request, 'dashboard/index.html', {})


class CommonView(generic.DetailView):

    def sendEmail(request, template, context, subject, to, user_id=None):
        response = {}
        try:
            context["request"] = request
            context["base_url"] = settings.SITE_URL
            context["project_title"] = settings.PROJECT_TITLE
            mail_template_content = render_to_string(template, context)
            sender_mail = settings.EMAIL_HOST_USER
            # if user_id:
            #     CommonHelper.set_history(user_id=user_id, subject=subject, type="email")
            import threading
            task = threading.Thread(target=MailHelper.mail_send, args=(mail_template_content, subject, to, sender_mail))
            task.start()
            response['success'] = True
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
        return HttpResponse(json.dumps(response), content_type='application/json')

    def common_datatable_context(self):
        show_entries = 10
        sorted_column = 0
        sorting_order = 'asc'
        context = {
            'show_entries': show_entries,
            'sorting_order': sorting_order,
            'sorted_column': sorted_column
        }
        return context

    def get_file_path(file):
        file = str(file)
        file_path = ""
        try:
            path = file.split("adminapp/")[1]
            file_path = settings.SITE_URL+"/"+path
        except Exception as e:
            LogHelper.elog(e)
        return file_path

    def get_all_main_component(request):
        components = Components.objects.filter(parent__isnull=True)
        return components

    def superuser_login(request):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False






