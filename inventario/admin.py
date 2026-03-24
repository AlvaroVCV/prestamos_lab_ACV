from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Notebook)
class NOtebookAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'marca', 'modelo', 'estado', 'disponible')
    search_fields = ('codigo', 'marca', 'modelo')
    list_filter = ('estado', 'disponible')