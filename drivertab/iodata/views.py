# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.db import IntegrityError
from django.forms import ValidationError
from drivertab.iodata.models import Driver, Trip

import datetime

def login(request):
      
     
    if not 'context' in request.session:
        request.session['context'] = {'logged_in':False}
         
    if request.method == 'POST':
        try:
            driver = Driver.objects.get(pin = request.POST.get('pin'))
        
            if driver.password == request.POST.get('password'):
                request.session['context']['logged_in'] = True
                request.session['context']['logged_driver'] = driver.id
                request.session['context']['driver_name'] = driver.firstName+' '+driver.lastName
            
                try:
                    del request.session['context']['error']
                except KeyError:
                    pass
                return HttpResponseRedirect ('/trips/')
            else:
                request.session['context']['error'] = 'Špatné heslo!'
        
        except Driver.DoesNotExist:
            request.session['context']['logged_in'] = False
            request.session['context']['error'] = 'Špatný PIN!'
    
    if request.session['context']['logged_in'] == True:
        
        try:
            del request.session['context']['error']
        except KeyError:
            pass
        return HttpResponseRedirect ('/trips/')

    else:
        fullcontext = {'csrftoken':csrf(request)}
        fullcontext.update(request.session['context'])
        
        return render_to_response('iodata/login.html',
                                  fullcontext,
                                  context_instance=RequestContext(request))

def logout (request):
    try:
        del request.session['context']
    except KeyError:
        pass
    return HttpResponseRedirect ('/')


def trips(request):

    if not 'context' in request.session:
        request.session['context'] = {'logged_in':False}
        
    if request.session['context']['logged_in']:

        def makeTripList():
            today = datetime.datetime.today()
            driver = request.session['context']['logged_driver']
            try:
                tripList = [(trip.customer, 
                             trip.endCustomer,
                             trip.truck, 
                             trip.fromPlace,
                             trip.toPlace,
                             trip.unit,
                             trip.loadedQuantity,
                             trip.unloadedQuantity,   
                             trip.material,
                             trip.startDate, 
                             trip.deliveryNumber,
                             trip.loadingDriver,
                             trip.loadingDateTime,
                             trip.unloadingDriver,
                             trip.unloadingDateTime,
                             trip.note,
                             trip.id) for trip in Trip.objects.filter(Q(driver1 = driver) | Q(driver2 = driver), 
                                                                      Q(startDate = today.date()) | Q(startDate__lt = today.date()),
                                                                      finished = False,).order_by('-startDate')]
            except Trip.DoesNotExist:
                tripList = []
   
            try:
                finishedTripList = [(trip.customer, 
                                     trip.endCustomer,
                                     trip.truck, 
                                     trip.fromPlace,
                                     trip.toPlace,
                                     trip.unit,
                                     trip.loadedQuantity,
                                     trip.unloadedQuantity,   
                                     trip.material,
                                     trip.startDate, 
                                     trip.deliveryNumber,
                                     trip.loadingDriver,
                                     trip.loadingDateTime,
                                     trip.unloadingDriver,
                                     trip.unloadingDateTime,
                                     trip.note,
                                     trip.id) for trip in Trip.objects.filter(Q(driver1 = driver) | Q(driver2 = driver), 
                                                                              Q(unloadingDateTime__gte = today.date()),
                                                                              finished = True).order_by('-unloadingDateTime')]
            
            except Trip.DoesNotExist:
                finishedTripList = []
            
            request.session['context']['today'] = today
            request.session['context']['tripList'] = tripList
            request.session['context']['finishedTripList'] = finishedTripList
    
        def toFloat(unicode):
            try:
                return float(unicode)
            except ValueError:
                split = unicode.split(',')
                return float(split[0]+'.'+split[1])                           

        makeTripList()

        if not 'loaded' in request.session['context']:
            request.session['context']['loaded'] = False
            for trip in request.session['context']['tripList']:
                if (trip[12]) and (trip[14] == None):
                    request.session['context']['loaded'] = True
                    break
                  
        if request.method == 'POST':
             
            if request.POST.get('load_button'):
                try:
                    driver = Driver.objects.get(pin = request.POST.get('pin'))
                    trip = Trip.objects.get(id = request.POST.get('load_button'))
                    
                    if (driver == trip.driver1) or (driver == trip.driver2):
                        if (driver.password == request.POST.get('password')):
                    
                            try:
                                loadingDateTime = request.POST.get('loadingDate')+':'+request.POST.get('loadingTime')
                                trip.loadingDateTime = datetime.datetime.strptime(loadingDateTime, "%d.%m.%y:%H:%M")
                                trip.loadedQuantity = toFloat(request.POST.get('loadedQuantity'))
                                trip.deliveryNumber = request.POST.get('deliveryNumber')
                                trip.loadingDriver = driver
                                trip.save()
                                request.session['context']['loaded'] = True
                                try:
                                    del request.session['context']['error']
                                except KeyError:
                                    pass
                                makeTripList()
                            except (ValueError, ValidationError, IntegrityError):
                                request.session['context']['error'] = 'Špatně zadané údaje!'
                                
                        else:
                            request.session['context']['error'] = 'Špatné heslo!'
                    else:
                        request.session['context']['error'] = 'Špatný řidič!'
                    
                except Driver.DoesNotExist:
                    request.session['context']['error'] = 'Špatný PIN!'
                            

                    
            if request.POST.get('unload_button'):
                
                try:
                    driver = Driver.objects.get(pin = request.POST.get('pin'))
                    trip = Trip.objects.get(id = request.POST.get('unload_button'))
                    
                    if (driver == trip.driver1) or (driver == trip.driver2):
                        if (driver.password == request.POST.get('password')):
                            try:
                                unloadingDateTime = request.POST.get('unloadingDate')+':'+request.POST.get('unloadingTime')
                                trip.unloadingDateTime = datetime.datetime.strptime(unloadingDateTime, "%d.%m.%y:%H:%M")
                                trip.unloadedQuantity = request.POST.get('unloadedQuantity')
                                trip.unloadingDriver = driver
                                trip.finished = True
                                trip.save()
                                request.session['context']['loaded'] = False
                                try:
                                    del request.session['context']['error']
                                except KeyError:
                                    pass
                                makeTripList()
                            except (ValueError, IntegrityError):
                                request.session['context']['error'] = 'Špatně zadané údaje!'
                        else:
                            request.session['context']['error'] = 'Špatné heslo!'
                    else:
                        request.session['context']['error'] = 'Špatný řidič!'
    
                except Driver.DoesNotExist:
                    request.session['context']['error'] = 'Špatný PIN!'
    
        fullcontext = {'csrftoken':csrf(request),
                       'loaded':request.session['context']['loaded']}
    
        fullcontext.update(request.session['context'])
        return render_to_response('iodata/trips.html',
                                  fullcontext,
                                  context_instance=RequestContext(request))
    
    else:
        return HttpResponseRedirect ('/')

    