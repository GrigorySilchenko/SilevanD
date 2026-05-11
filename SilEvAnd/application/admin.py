from django.contrib import admin
from .models import Application, Declarant, Status, NetworkGraph, ApplicationTest

class StatusAdmin(admin.ModelAdmin):
    readonly_fields = ['id']

admin.site.register(Application)
admin.site.register(Declarant)
admin.site.register(Status, StatusAdmin)
admin.site.register(NetworkGraph)
admin.site.register(ApplicationTest)