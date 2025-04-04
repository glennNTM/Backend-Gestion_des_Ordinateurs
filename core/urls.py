from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrdinateurViewSet, ReportIssueViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'ordinateurs', OrdinateurViewSet, basename='ordinateurs')
router.register(r'signalements', ReportIssueViewSet, basename='signalements')

urlpatterns = router.urls
