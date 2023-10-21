from rest_framework.routers import DefaultRouter

from people_and_groups.api.views import PersonViewSet

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='person')

urlpatterns = []
urlpatterns.extend(router.urls)
