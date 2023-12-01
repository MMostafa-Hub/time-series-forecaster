from django.db import models
import datetime
import pickle

import numpy as np


class Dataset(models.Model):
    dataset_id = models.CharField(
        max_length=255, unique=True, primary_key=True, name="dataset_id"
    )
    pipeline = models.BinaryField(name="pipeline")

    model = models.BinaryField(name="model")

    interval = models.DurationField(
        name="interval", default=datetime.timedelta(days=1), null=False, blank=False
    )

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}"

    def get_model(self):
        return pickle.loads(self.model)

    def get_pipeline(self):
        return pickle.loads(self.pipeline)


class Forecast(models.Model):
    dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    prediction = models.FloatField(null=True, name="prediction", blank=True)

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}, Prediction: {self.prediction}"


class Value(models.Model):
    forecast = models.ForeignKey(
        Forecast, on_delete=models.CASCADE, related_name="values"
    )
    time = models.DateTimeField()
    value = models.FloatField(default=np.nan, null=True, blank=True, name="value")

    def __str__(self):
        return f"Forecast: {self.forecast}, Time: {self.time}, Value: {self.value}"
