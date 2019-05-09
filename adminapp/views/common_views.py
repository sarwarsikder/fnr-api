import json
from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from adminapp.views.mail import MailHelper
from adminapp.views.helper import LogHelper


class IndexView(generic.DetailView):
    def get(self, request):
        return render(request, 'dashboard/index.html', {})


class CommonView(generic.DetailView):

    def sendEmail(request, template, context, subject, to, user_id=None):
        response = {}
        try:
            context["request"] = request
            context["base_url"] = settings.SITE_URL
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






