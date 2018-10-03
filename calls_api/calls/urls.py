from django.conf.urls import url
from .views import CallsViewSet, BillViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('calls', CallsViewSet, 'call')
router.register('bill', BillViewSet, 'bill')

urlpatterns = router.urls

