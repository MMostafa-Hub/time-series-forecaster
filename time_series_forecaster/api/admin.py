from django.contrib import admin
from .models import Forecast, Dataset

admin.site.register(Forecast)
admin.site.register(Dataset)