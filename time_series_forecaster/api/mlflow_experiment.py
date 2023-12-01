from api.transformers.auto_correlation import AutocorrelationTransformer
from api.transformers.seasonality import SeasonalityFeaturesTransformer
from api.transformers.interpolation import InterpolationTransformer
from api.transformers.outlier import OutlierTransformer
from api.transformers.trend import TrendTransformer
from sklearn.linear_model import LinearRegression
from mlflow.client import MlflowClient
from sklearn.pipeline import Pipeline
import pickle


class MLFlowExperiment:
    def __init__(self, experiment_name, tracking_uri: str = "http://localhost:5000"):
        self.experiment_name = experiment_name
        self.client = MlflowClient(tracking_uri=tracking_uri)
        self.experiment = self.client.get_experiment_by_name(experiment_name)

        if not self.experiment:
            raise ValueError(
                f"Experiment {experiment_name} not found. "
                f"Please create the experiment before using it."
            )

        self.__runs = self.client.search_runs(self.experiment.experiment_id)

    def get_run(self, index: int = 0):
        return self.__runs[index]

    def get_run_params(self, index: int = 0):
        return self.get_run(index).data.params

    def get_run_artifact_uri(self, index: int = 0):
        return self.get_run(index).info.artifact_uri

    def get_model(self) -> LinearRegression:
        with open(self.get_run_artifact_uri() + "/model/model.pkl", "rb") as f:
            model = pickle.load(f)

        return model

    def get_pipeline(self) -> Pipeline:
        with open(
            self.get_run_artifact_uri() + f"/pipeline/{self.experiment_name}.pkl", "rb"
        ) as f:
            pipeline = pickle.load(f)

        return pipeline
