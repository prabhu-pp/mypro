from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, IncomingDataView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('data-handler/', IncomingDataView.as_view(), name='data-handler'),
]