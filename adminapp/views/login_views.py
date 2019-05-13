from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from adminapp.models import Users
from adminapp.views.helper import LogHelper


class LoginView(generic.DetailView):
    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'profiles/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'profiles/login.html', {'msg': 'Authenntication failed.Wrong Phone number or Password. Try Again'})


class LogoutView(generic.DetailView):
    def get(self, request):
        del request.session['supplementer_user']
        logout(request)
        return redirect('login')



