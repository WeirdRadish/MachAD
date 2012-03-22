# coding=utf-8

from models import Driver, Trip
from django.contrib import admin

class Driveradmin (admin.ModelAdmin):
    list_display = ('pin', 'firstName', 'lastName',)

class Tripadmin (admin.ModelAdmin):
    list_display = ('startDate', 'customer', 'endCustomer', 'truck', 'deliveryNumber', 'material', 'unit', 'loadingDriver', 'loadingDateTime', 'loadedQuantity', 'unloadingDriver', 'unloadingDateTime', 'unloadedQuantity')

admin.site.register(Driver, Driveradmin)
admin.site.register(Trip, Tripadmin)
