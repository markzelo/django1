from django.contrib import admin
from .models import Task


#ver datos en admin
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )  #como cambiar created by

#registrar modelos
admin.site.register(Task, TaskAdmin)
