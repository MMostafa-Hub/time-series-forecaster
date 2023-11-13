from django.core.management.base import BaseCommand
from api.models import Pipeline


class Command(BaseCommand):
    help = "Populate the Dataset model with initial data"

    def handle(self, *args, **options):
        # Make sure the pipeline table has only one row
        Pipeline.objects.all().delete()
        
        with open("../notebooks/pipelines/preprocessing_pipeline.pkl", "rb") as file:
            preprocessing_pipeline = file.read()

        pipeline = Pipeline(preprocessing_pipeline=preprocessing_pipeline)
        pipeline.save()

        self.stdout.write(self.style.SUCCESS("Loaded preprocessing pipeline successfully"))
