from django.urls import include, path
from . import views

auth_patterns = [
    path('login/', views.servicem8_login, name='servicem8_login'),
    path('callback/', views.servicem8_callback, name='servicem8_callback'),
]

urlpatterns = [
    path("oauth/", include(auth_patterns)),
    path("get-all-jobs", views.get_servicem8_jobs),
    path("webhook", views.servicem8_webhook, name='webhook')
]
