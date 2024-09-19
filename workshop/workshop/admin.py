from django.contrib import admin
from workshop.models import Fruits, Sell
# Register your models here.

class fruitsadmin(admin.ModelAdmin):
    list_display = ("name", "clas", "fresh", "quant", "value")

admin.site.register(Fruits, fruitsadmin)

class selladmin(admin.ModelAdmin):
    list_display = ("products", "hour", "value")

admin.site.register(Sell, selladmin)