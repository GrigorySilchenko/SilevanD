from django.urls import path
from . import views

urlpatterns = [
    path('registry/', views.registry, name='registry'),
    path('registry_input/', views.registry_input, name='registry_input'),
    path('slot_machine_data/', views.slot_machine_data, name='slot_machine_data'),
    path('slot_machine_data_change/<int:pk>', views.slot_machine_data_change, name='slot_machine_data_change'),
    path('s_m_data_input/<int:pk>', views.s_m_data_input, name='s_m_data_input'),
    path('application_status_change/<int:pk>', views.application_status_change, name='application_status_change'),
    path('', views.act_creation, name='act_creation'),
    path('docx_create/', views.docx_create, name='docx_create'),
    path('download_act_docx/<str:file_name>/', views.download_act_docx, name='download_act_docx')
]