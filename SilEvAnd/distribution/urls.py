from django.urls import path
from . import views

urlpatterns = [
    path('', views.distribution, name='distribution'),
    path('distribution_change/<int:pk>', views.distribution_change, name='distribution_change'),
    path('application_distribution/<int:pk>', views.application_distribution, name='application_distribution')
]