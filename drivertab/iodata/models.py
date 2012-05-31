# coding=utf-8

from django.db import models

class Driver (models.Model):
    pin = models.CharField ('PIN', max_length=10, unique=True,)
    firstName = models.CharField ('Jméno', max_length=50,)
    lastName = models.CharField ('Příjmení', max_length=50,)
    password = models.CharField ('Heslo', max_length=25,)
    
    class Meta:
        verbose_name='Řidič'
        verbose_name_plural='Řidiči'
        
    def __unicode__(self):
        return self.firstName+' '+self.lastName
    
class Trip (models.Model):
    driver1 = models.ForeignKey (Driver, related_name='driver1', verbose_name='Řidič 1',)
    driver2 = models.ForeignKey (Driver, related_name='driver2', verbose_name='Řidič 2', blank=True, null=True,)
    customer = models.CharField ('Dodavatel', max_length=75,)
    endCustomer = models.CharField ('Odběratel', max_length=75,)
    truck = models.CharField ('Vůz', max_length=10,)
    fromPlace = models.CharField ('Z místa', max_length=100,)
    toPlace = models.CharField ('Do místa', max_length=100,)
    material = models.CharField ('Materiál', max_length=100,)
    unit = models.CharField ('Jednotka', max_length=100, blank=True, null=True,)
    startDate = models.DateField ('Datum zadání',)
    finished = models.BooleanField ('Ukončeno',)
    loadedQuantity = models.FloatField ('Naložené množství', max_length=100, blank=True, null=True,)
    unloadedQuantity = models.FloatField ('Vyložené množství', max_length=100, blank=True, null=True,)
    deliveryNumber = models.IntegerField ('Č. dodacího listu', max_length=25, unique=True, blank=True, null=True,)
    loadingDriver = models.ForeignKey (Driver, related_name='driver_load', verbose_name='Naložil', blank=True, null=True,)
    loadingDateTime = models.DateTimeField ('Naloženo', blank=True, null=True,)
    unloadingDriver = models.ForeignKey (Driver, related_name='driver_unload', verbose_name='Vyložil', blank=True, null=True,)
    unloadingDateTime = models.DateTimeField ('Vyloženo', blank=True, null=True,)
    note = models.CharField ('Poznámka', max_length=255, blank=True, null=True,)
    
    class Meta:
        verbose_name='Cesta'
        verbose_name_plural='Cesty'
        ordering = ['-startDate']
    
    def __unicode__(self):
        return str(self.deliveryNumber)
    
