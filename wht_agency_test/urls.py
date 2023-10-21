from django.urls import include, path

urlpatterns = [
    path('', include('people_and_groups.urls'))
]
