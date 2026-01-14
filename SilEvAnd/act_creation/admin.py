from django.contrib import admin
from .models import Registry, Manufacturer, StickPlace, Boss, Conformity, Act, RegistryModify
from application.admin import StatusAdmin


admin.site.register(Registry)
admin.site.register(RegistryModify)
admin.site.register(Manufacturer)
admin.site.register(StickPlace, StatusAdmin)
admin.site.register(Boss)
admin.site.register(Conformity, StatusAdmin)
admin.site.register(Act)