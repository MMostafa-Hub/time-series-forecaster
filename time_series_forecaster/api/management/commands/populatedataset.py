from django.core.management.base import BaseCommand
from api.models import Dataset
from glob import glob
import pickle


class Command(BaseCommand):
    help = "Populate the Dataset model with initial data"

    def __populate_dataset_model(self):
        datasets_paths = glob("../data/*.csv")
        datasets_names = [path.split("/")[-1].split(".")[0] for path in datasets_paths]
        with open("../data/datasets_intervals.pkl", "rb") as file:
            intervals = pickle.load(file)

        for dataset_name in datasets_names:
            with open(
                f"../notebooks/pipelines/models/{dataset_name}.pkl", "rb"
            ) as model_file, open(
                f"../notebooks/pipelines/preprocessing/{dataset_name}.pkl", "rb"
            ) as pipeline_file:
                dataset = Dataset(
                    dataset_id=dataset_name,
                    model=model_file.read(),
                    pipeline=pipeline_file.read(),
                    interval=intervals[dataset_name],
                )
                print(f"Saving dataset {dataset_name}")
            dataset.save()

    def handle(self, *args, **options):
        self.__populate_dataset_model()
        self.stdout.write(self.style.SUCCESS("Dataset model populated successfully"))
