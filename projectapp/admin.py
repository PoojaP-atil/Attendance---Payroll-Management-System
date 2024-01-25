from django.contrib import admin
from . import models

# Register your models here.
class empadmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("Name","Designation")}

admin.site.register(models.employee,empadmin)