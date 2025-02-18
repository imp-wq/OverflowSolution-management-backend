from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    path("serviceM8/", include('ManagementApp.serviceM8.urls')),
    path("jira/", include('ManagementApp.jira.urls'))
]
