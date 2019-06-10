from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from pushnotificationapp.views import SubscriberViewSet, PushNotificationViewSet

router = routers.DefaultRouter()
router.register(r'subscribe', SubscriberViewSet)
router.register(r'push', PushNotificationViewSet)

urlpatterns = [
    path('docs/', include_docs_urls(title='API Lists')),
]

urlpatterns += router.urls