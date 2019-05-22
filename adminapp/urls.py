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
    url(r'^staffs/change-password/(?P<pk>[\w-]+)$', staff_views.StaffPasswordChangeView.as_view(),name='staffs-password-update'),

    url(r'^companies/$', company_views.CompaniesView.as_view(), name='companies'),
    url(r'^companies/add/$', company_views.CompanyFormView.as_view(), name='companies-add'),
    url(r'^companies/update/(?P<pk>[\w-]+)/$', company_views.CompanyUpdateView.as_view(), name='companies-update'),
    url(r'^companies/delete/$', company_views.CompaniesView.delete, name='companies-delete'),
    url(r'^company-list/$', datatables.CompanyListView.as_view(), name='companyList'),
    url(r'^companies/change-password/(?P<pk>[\w-]+)$', company_views.CompanyPasswordChangeView.as_view(),name='companies-password-update'),

    url(r'^change-user-status/$', staff_views.StaffsView.change_user_status, name='change-user-status'),

    url(r'^projects/$', project_views.ProjectsView.as_view(), name='projects'),
    url(r'^projects/add/$', project_views.ProjectFormView.as_view(), name='projects-add'),
    url(r'^projects/update/(?P<pk>[\w-]+)/$', project_views.ProjectUpdateView.as_view(), name='projects-update'),
    url(r'^projects/delete/$', project_views.ProjectsView.delete, name='projects-delete'),
    url(r'^project-list/$', datatables.ProjectListView.as_view(), name='projectList'),
    url(r'^projects/(?P<project_id>[\w-]+)/buildings/$', building_views.BuildingsView.as_view(), name='buildings'),
    url(r'^building-list/$', datatables.BuildingListView.as_view(), name='buildingList'),
    url(r'^projects/(?P<project_id>[\w-]+)/buildings/add/$', building_views.BuildingFormView.as_view(), name='buildings-add'),
    url(r'^buildings/update/(?P<pk>[\w-]+)/$', building_views.BuildingUpdateView.as_view(), name='buildings-update'),
    url(r'^buildings/delete/$', building_views.BuildingsView.delete, name='buildings-delete'),
    url(r'^buildings/qr/(?P<pk>[\w-]+)/$', building_views.BuildingsView.preview_qr, name='buildings-qr'),

    url(r'^buildings/(?P<building_id>[\w-]+)/flats/$', flat_views.FlatsView.as_view(), name='flats'),
    url(r'^flats-list/$', datatables.FlatListView.as_view(), name='flatList'),
    url(r'^buildings/(?P<building_id>[\w-]+)/flats/add/$', flat_views.FlatFormView.as_view(), name='flats-add'),
    url(r'^flats/update/(?P<pk>[\w-]+)/$', flat_views.FlatUpdateView.as_view(), name='flats-update'),
    url(r'^flats/delete/$', flat_views.FlatsView.delete, name='flats-delete'),
    url(r'^flats/qr/(?P<pk>[\w-]+)/$', flat_views.FlatsView.preview_qr, name='flats-qr'),

    url(r'^components/$', component_views.ComponentView.as_view(), name='components'),

    url(r'^qr-to-png/(?P<qr_id>[\w-]+)/$', common_views.QRResponse.as_view(), name='qr-to-png'),
]