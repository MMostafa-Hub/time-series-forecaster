from django.core.management.base import BaseCommand
from api.models import Dataset
from glob import glob
import pickle


class Command(BaseCommand):
    help = "Populate the Dataset model with initial data"

    def __populate_dataset_model(self):
        datasets_paths = glob("../data/*.csv")
        datasets_names = [path.split("/")[-1].split(".")[0] for path in datasets_paths]

        models_paths = glob("../notebooks/pipelines/models/*.pkl")
        pipelines_paths = glob("../notebooks/pipelines/preprocessing/*.pkl")
        self.stdout.write(
            f"datasets: {len(datasets_names)}\nmodels: {len(models_paths)}\npipelines: {len(pipelines_paths)}"
        )
        with open("../data/datasets_intervals.pkl", "rb") as file:
            intervals = pickle.load(file)

        for dataset_name, model_path, pipeline_path in zip(
            datasets_names, models_paths, pipelines_paths
        ):
            with open(model_path, "rb") as model_file, open(
                pipeline_path, "rb"
            ) as pipeline_file:
                dataset = Dataset(
                    dataset_id=dataset_name,
                    model=model_file.read(),
                    pipeline=pipeline_file.read(),
                    interval=intervals[dataset_name],
                )
            dataset.save()

    def handle(self, *args, **options):
        self.__populate_dataset_model()
        self.stdout.write(self.style.SUCCESS("Dataset model populated successfully"))
