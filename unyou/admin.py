from django.contrib import admin
from .models import Unyou
admin.site.register(Unyou)


class UnyouAdmin(admin.ModelAdmin):
    pass

# Register your models here.
