from django.urls import path
from . import views

urlpatterns = [
    path('registry/', views.registry, name='registry'),
    path('registry_input/', views.registry_input, name='registry_input'),
    path('slot_machine_data/', views.slot_machine_data, name='slot_machine_data'),
    path('s_m_data_input/<int:pk>', views.s_m_data_input, name='s_m_data_input'),
    path('', views.act_creation, name='act_creation'),
    path('docx_create', views.docx_create, name='docx_create')
]