import json

from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from adminapp.models import Users
from adminapp.forms.user_form import UserForm, UserUpdateForm, UserPasswordChangeForm
from adminapp.views.common_views import CommonView
from adminapp.views.helper import LogHelper
from django.conf import settings


class StaffsView(generic.DetailView):
    def get(self, request):
        context = CommonView.common_datatable_context(self)
        return render(request, 'staffs/staff.html', context)

    def delete(request):
        response = {}
        try:
            userId = request.POST.get('id')
            # Users.objects.filter(id=userId).update(is_active='0')
            Users.objects.get(id=userId).delete()
            response['success'] = True
            response['message'] = "User delete successfully"
        except Exception as e:
            LogHelper.elog(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')


class StaffFormView(View):
    form_class = UserForm
    template_name = 'staffs/add_staff.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(self, request)
            mailTemplate = "mails/user_registered.html"
            context = {
                "user_full_name": obj.get_full_name(),
                "password": self.request.POST.get('password'),
                "username": self.request.POST.get('username')
            }
            subject = "Staff Register"
            to = obj.email
            CommonView.sendEmail(self.request, mailTemplate, context, subject, to, obj.id)
            return HttpResponseRedirect('/staffs/')
        return render(request, self.template_name, {'form': form})


class StaffUpdateView(UpdateView):

    model = Users
    template_name = 'staffs/edit_staff.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        form.update(request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('staffs')

    def get_context_data(self, **kwargs):
        context = super(StaffUpdateView, self).get_context_data(**kwargs)
        context['avatar'] = CommonView.get_file_path(self.object.avatar)
        return context


class StaffPasswordChangeView(UpdateView):
    model = Users
    form_class = UserPasswordChangeForm
    template_name = 'users/user_password_change.html'

    def get_success_url(self):
        return reverse_lazy('staffs-all')

    def form_valid(self, form):
        form.save(request=self.request)
        mailTemplate = "mails/user_password_change.html"
        context = {
            "user_full_name": self.object.get_full_name(),
            "password": self.request.POST.get('password')
        }
        subject = "Password Change"
        to = self.object.email
        CommonView.sendEmail(self.request, mailTemplate, context, subject, to, self.object.id)
        return HttpResponseRedirect(self.get_success_url())

