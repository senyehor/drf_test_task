from rest_framework.routers import DefaultRouter

from people_and_groups.api.views import (
    GroupMembersActionSViewSet, GroupViewSet,
    PersonGroupActionsViewSet, PersonViewSet,
)

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='person')
router.register(r'people', PersonGroupActionsViewSet, basename='person')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'groups', GroupMembersActionSViewSet, basename='group')

urlpatterns = []
urlpatterns.extend(router.urls)
