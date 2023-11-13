from django.db import models


class Dataset(models.Model):
    dataset_id = models.CharField(max_length=255, unique=True, primary_key=True, name="dataset_id")
    model = models.BinaryField(name="model")

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}"

    def get_model(self):
        import pickle

        return pickle.loads(self.model)


class Forecast(models.Model):
    dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    values = models.JSONField(name="values")
    prediction = models.FloatField(null=True, name="prediction")

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}, Values: {self.values}, Prediction: {self.prediction}"
