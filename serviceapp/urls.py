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
from django.conf.urls import include
from django.conf.urls import url
from serviceapp.views.user_views import UserInfo, ResetPasswordRequestViewSet
from rest_framework.routers import SimpleRouter
from serviceapp.views.projects import ProjectViewSet, ProjectPlanViewSet

router = SimpleRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^user-profile/', UserInfo.as_view()),
    url(r'^forget-password/', ResetPasswordRequestViewSet.forget_password),
    url(r'^change-user-password/', ResetPasswordRequestViewSet.change_user_password),

    url(r'^project-plans/(?P<project_id>[\w-]+)/$', ProjectPlanViewSet.as_view()),
] + router.urls