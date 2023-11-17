from django.contrib import admin
from .models import Forecast, Dataset, Value

admin.site.register((Forecast, Dataset, Value))
