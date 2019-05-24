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
from adminapp.views import common_views, login_views, staff_views, company_views, project_views, buildingplan_views, flatplan_views, component_views, reset_password, datatables, profile_views
from django.conf import settings
from django.views.static import serve
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
    url(r'^projects/$', project_views.ProjectsView.as_view(), name='projects'),
    url(r'^projects/add/$', project_views.ProjectFormView.as_view(), name='projects-add'),
    url(r'^projects/update/(?P<pk>[\w-]+)/$', project_views.ProjectUpdateView.as_view(), name='projects-update'),
    url(r'^projects/delete/$', project_views.ProjectsView.delete, name='projects-delete'),
    url(r'^project-list/$', datatables.ProjectListView.as_view(), name='projectList'),
    url(r'^components/$', component_views.ComponentView.as_view(), name='components'),
    url(r'^components/add/$', component_views.ComponentAddView.as_view(), name='component-add'),
    url(r'^components/update/(?P<pk>[\w-]+)/$', component_views.ComponentUpdateView.as_view(), name='component-update'),
    url(r'^components/delete$', component_views.ComponentView.delete, name='component-delete'),
    url(r'^building-plan/$', buildingplan_views.BuildingPlansView.as_view(), name='building-plan'),
    url(r'^building-plan/add/$', buildingplan_views.BuildingPlansAddView.as_view(), name='building-plan-add'),
    url(r'^building-plan/update/(?P<pk>[\w-]+)/$', buildingplan_views.BuildingPlansUpdateView.as_view(), name='building-plan-update'),
    # url(r'^building-plan/delete$', buildingplan_views.BuildingPlans.delete, name='building-plan-delete'),
    url(r'^flat-plan/$', flatplan_views.FlatPlansView.as_view(), name='flat-plan'),
    url(r'^flat-plan/add/$', flatplan_views.FlatPlansAddView.as_view(), name='flat-plan-add'),
    url(r'^flat-plan/update/(?P<pk>[\w-]+)/$', flatplan_views.BuildingPlansUpdateView.as_view(), name='flat-plan-update'),
    # url(r'^flat-plan/delete$', flatplan_views.FlatPlansView.delete, name='flat-plan-delete'),
]



if settings.DEBUG:
    urlpatterns +=[
        url(r'media/(?P<path>.*)$', serve,{
            'document_root': settings.MEDIA_ROOT
        }),
    ]


