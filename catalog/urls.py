from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("search/", views.tutor_search, name="tutor_search"),
]
