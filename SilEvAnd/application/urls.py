from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('application/', views.application, name='application'),
    path('application_change/<int:pk>', views.application_change, name='application_change'),
    path('application_del/<int:pk>', views.application_del, name='application_del'),
    path('declarant/', views.declarant, name='declarant'),
    path('declarant_change/<int:pk>', views.declarant_change, name='declarant_change'),
    path('declarant_del/<int:pk>', views.declarant_del, name='declarant_del')
]
