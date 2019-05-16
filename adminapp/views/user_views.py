from django.shortcuts import render
from django.views import generic
from adminapp.models import Users
from django.shortcuts import redirect

class UserView(generic.DetailView):
    def get(self, request):
        user_list = Users.objects.filter()
        return render(request, 'users/list.html', {"user_list":user_list})

    def profile(request, id):
        user_profile = Users.objects.get(id=id)
        return render(request, 'users/profile.html',{"profile":user_profile})

    def edit(request, id):
        user_edit = Users.objects.get(id=id)
        return render(request, 'users/edit.html',{'edit': user_edit})

    def update(request, id):
        form_data = {

            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        Users.objects.filter(id=id).update(**form_data)
        return redirect('users')