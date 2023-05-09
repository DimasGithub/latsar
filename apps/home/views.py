# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import time
import json
import random
import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import (TemplateView, DetailView)

from .models import Vehicle

class RetributionCalulationViewSet(TemplateView):
    def get(self, request):
        context = {'segment': 'hitung-retribusi',
            'category_vehicles': Vehicle.objects.all()
            }
        return render(request, 'home/hitung_retribusi.html', context=context)

    def post(self, request):
        context = {'segment': 'hitung-retribusi',
            'category_vehicles': Vehicle.objects.all()
            }
        try:
            price_vehicle = request.POST['vehicle_price']
            date_input_str = request.POST['date_vehicle_test']
            vehicle = Vehicle.objects.get(id=price_vehicle)
            is_cash_fine =False
            if vehicle.active_cash_fine: is_cash_fine=True
            # Get the current date
            now = datetime.date.today()           
            date_input = datetime.datetime.strptime(date_input_str, "%m/%d/%Y %I:%M %p").date()
            diff_months = (now.year - date_input.year) * 12 + (now.month - date_input.month)
            total_percentage = 0.02 * int(vehicle.price)
            total_retribution_price = (diff_months * total_percentage) + int(vehicle.price)
            if is_cash_fine: total_retribution_price = int(vehicle.price)
            results = {
                'mutation':is_cash_fine,
                'name': vehicle.name,
                'date_vehicle_test':date_input_str,
                'price': vehicle.price,
                'diff_month': diff_months,
                'total_retribution_price':total_retribution_price
            }
            context.update({'results': results})
            return render(request,'home/hitung_retribusi.html', context=context)
        
        except Vehicle.DoesNotExist:
            messages.warning(request, f"Tipe kendaraan tidak tersedia.")
        except Exception as err:
            messages.warning(request, f"{err}, Please contact admin.")
        return redirect(reverse('dashboard:hitung_retribusi'))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
