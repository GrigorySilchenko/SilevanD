from django.contrib import admin
from django.urls import path
from . import views
from .autocomplete import DeclarantAutocomplete

urlpatterns = [
    path('', views.home, name='home'),
    path('application/', views.application, name='application'),
    path('application_change/<int:pk>', views.application_change, name='application_change'),
    path('application_del/<int:pk>', views.application_del, name='application_del'),
    path('declarant/', views.declarant, name='declarant'),
    path('declarant-autocomplete/', DeclarantAutocomplete.as_view(), name='declarant-autocomplete'),
    path('declarant_change/<int:pk>', views.declarant_change, name='declarant_change'),
    path('declarant_del/<int:pk>', views.declarant_del, name='declarant_del'),
    path('network_graph/', views.network_graph, name='network_graph'),
    path('network_graph_change/<int:pk>', views.network_graph_change, name='network_graph_change'),
]
