from django.db import models


class Dataset(models.Model):
    dataset_id = models.CharField(max_length=255, unique=True, primary_key=True)
    model = models.BinaryField()

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}"

    def get_model(self):
        import pickle

        return pickle.loads(self.model)

    def set_model(self, model):
        import pickle

        self.model = pickle.dumps(model)


class Forecast(models.Model):
    dataset_id = models.CharField(max_length=255, foreign_key=True)
    values = models.JSONField()
    prediction = models.FloatField()

    def __str__(self):
        return f"Dataset ID: {self.dataset_id}, Values: {self.values}, Prediction: {self.prediction}"
