from django.contrib import admin
from .models import Registry, Manufacturer, StickPlace, Conformity, Act


admin.site.register(Registry)
admin.site.register(Manufacturer)
admin.site.register(StickPlace)
admin.site.register(Conformity)
admin.site.register(Act)