from rest_framework.routers import DefaultRouter

from people_and_groups.api.views import GroupViewSet, PersonViewSet

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='person')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = []
urlpatterns.extend(router.urls)
