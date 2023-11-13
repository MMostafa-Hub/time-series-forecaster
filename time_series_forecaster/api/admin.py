from django.contrib import admin
from .models import Forecast, Dataset, Pipeline, Value

admin.site.register((Forecast, Dataset, Pipeline, Value))
