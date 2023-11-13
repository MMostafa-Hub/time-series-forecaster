from django.core.management.base import BaseCommand
from api.models import Pipeline


class Command(BaseCommand):
    help = "Populate the Dataset model with initial data"

    def handle(self, *args, **options):
        with open("../notebooks/pipelines/preprocessing_pipeline.pkl", "rb") as file:
            preprocessing_pipeline = file.read()

        Pipeline(preprocessing_pipeline=preprocessing_pipeline)
        Pipeline.save()

        self.stdout.write(self.style.SUCCESS("Loaded pipelines successfully"))
