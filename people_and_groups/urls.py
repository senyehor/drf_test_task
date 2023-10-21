from django.urls import include, path

urlpatterns = [
    path('api/', include('people_and_groups.api.urls'))
]
