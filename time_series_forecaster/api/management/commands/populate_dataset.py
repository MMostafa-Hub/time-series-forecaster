from django.core.management.base import BaseCommand
from api.models import Dataset
from glob import glob


class Command(BaseCommand):
    help = "Populate the Dataset model with initial data"

    def __populate_dataset_model(self):
        datasets_paths = glob("../data/*.csv")
        datasets_names = [path.split("/")[-1].split(".")[0] for path in datasets_paths]

        models_paths = glob("../notebooks/pipelines/models/*.pkl")

        self.stdout.write(
            f"datasets: {len(datasets_names)}\nmodels: {len(models_paths)}"
        )
        
        for dataset_name, model_path in zip(datasets_names, models_paths):
            with open(model_path, "rb") as file:
                dataset = Dataset(dataset_id=dataset_name, model=file.read())
            dataset.save()

    def handle(self, *args, **options):
        self.__populate_dataset_model()
        self.stdout.write(self.style.SUCCESS("Dataset model populated successfully"))
