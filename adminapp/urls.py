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
from django.urls import path
from adminapp.views import common_views, login_views, staff_views, company_views, project_views, building_views, flat_views, component_views

urlpatterns = [
    path('', common_views.IndexView.as_view(), name='index'),
    path('login', login_views.LoginView.as_view(), name='login'),
    path('staffs', staff_views.StaffView.as_view(), name='staffs'),
    path('companies', company_views.CompanyView.as_view(), name='companies'),
    path('projects', project_views.ProjectView.as_view(), name='projects'),
    path('components', component_views.ComponentView.as_view(), name='components'),
]