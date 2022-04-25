from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    path('', csrf_exempt(views.ResumeView.as_view())),
    path('error/', csrf_exempt(views.ErrorView.as_view())),
]