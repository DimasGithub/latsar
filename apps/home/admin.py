# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from .models import Vehicle

# admin.site.register(Nip)
# admin.site.register(UploadFile)
admin.site.register(Vehicle)