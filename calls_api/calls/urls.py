from django.conf.urls import url
from .views import CallsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('calls', CallsViewSet, 'call')

urlpatterns = router.urls

