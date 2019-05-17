"""supplementer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from adminapp.views import common_views, login_views, staff_views, company_views, project_views, building_views, flat_views, component_views, reset_password, datatables, profile_views

urlpatterns = [
    url(r'^$', common_views.IndexView.as_view(), name='index'),
    url(r'^login/$', login_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', login_views.LogoutView.as_view(), name='logout'),
    url(r'^forget-password/$', reset_password.ResetPasswordRequestView.as_view(), name='forget-password'),
    url(r'^reset-password/$', reset_password.ResetPasswordView.as_view(), name='reset-password'),

    url(r'^profile/update/$', profile_views.ProfileUpdateView.as_view(), name='profile-update'),
    url(r'^change-password/$', profile_views.ChangePassword.as_view(), name='change-password'),

    url(r'^staffs/$', staff_views.StaffsView.as_view(), name='staffs'),
    url(r'^staffs/add/$', staff_views.StaffFormView.as_view(), name='staffs-add'),
    url(r'^staffs/update/(?P<pk>[\w-]+)/$', staff_views.StaffUpdateView.as_view(), name='staffs-update'),
    url(r'^staffs/delete/$', staff_views.StaffsView.delete, name='staffs-delete'),
    url(r'^staff-list/$', datatables.StaffListView.as_view(), name='staffList'),
    url(r'^companies/$', company_views.CompaniesView.as_view(), name='companies'),
    url(r'^companies/add/$', company_views.CompanyFormView.as_view(), name='companies-add'),
    url(r'^companies/update/(?P<pk>[\w-]+)/$', company_views.CompanyUpdateView.as_view(), name='companies-update'),
    url(r'^companies/delete/$', company_views.CompaniesView.delete, name='companies-delete'),
    url(r'^company-list/$', datatables.CompanyListView.as_view(), name='companyList'),
    url(r'^change-user-status/$', staff_views.StaffsView.change_user_status, name='change-user-status'),
    url(r'^projects/$', project_views.ProjectView.as_view(), name='projects'),
    url(r'^components/$', component_views.ComponentView.as_view(), name='components'),
]