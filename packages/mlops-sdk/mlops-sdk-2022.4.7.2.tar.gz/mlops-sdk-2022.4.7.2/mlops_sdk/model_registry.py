import json
from mlops_sdk.models.ml_model import MLModel
from google.cloud import storage
from pathlib import Path


MODEL_META_NAME = "model.json"
BUCKET = "emartdt-model-registry-bf0725d"


class ModelRegistryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelRegistry:
    """
    모델 레지스트리 클래스입니다.
    """

    def __init__(self):
        """
        ## Args

        ## Returns
        `mlops_sdk.ModelRegistry`

        ## Example

        ```python
        model_registry = ModelRegistry()
        ```
        """

    def save(self, ml_model: "MLModel", force: bool = False, model_path: str = None) -> None:
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 모델 레지스트리에 등록합니다.

        ## Args


        ## Example

        ```python
        model_registry = ModelRegistry()
        model_registry.save(gbm_model)
        ```
        """
        ml_model_dir = Path(model_path).absolute()
        model_meta_path = ml_model_dir.joinpath(MODEL_META_NAME)

        with model_meta_path.open("w") as f:
            json.dump(
                {
                    "id": ml_model.id,
                    "name": ml_model.name,
                    "version": ml_model.version,
                    "creator": ml_model.creator,
                    "created_at": ml_model.created_at,
                    "updated_at": ml_model.updated_at,
                    "status": ml_model.status,
                    "description": ml_model.description,
                    "table": ml_model.table,
                    "model_data": ml_model.model_data,
                    "model_lib": ml_model.model_lib,
                    "model_lib_version": ml_model.model_lib_version,
                    "model_checkpoint": ml_model.model_checkpoint,
                    "product_name": ml_model.product_name,
                    "dataset_train": ml_model.dataset_train,
                    "dataset_test": ml_model.dataset_test,
                    "eval_metric": ml_model.eval_metric,
                    "eval_method": ml_model.eval_method,
                    "class": ml_model.__class__.__name__,
                    "metric": getattr(ml_model, "metric", None),
                    "performance": getattr(ml_model, "performance", None),
                    "feature_importance": getattr(ml_model, "feature_importance", None),
                    "model_info": getattr(ml_model, "model_info", None),
                },
                f,
            )

        bucket_name = BUCKET

        destination_blob_name = f"{ml_model.name}/{ml_model.version}/{ml_model.id}.pt"
        storage_client = storage.Client(project="emart-dt-dev-ds")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(model_path + f"/{ml_model.id}.pt")

        destination_blob_name = f"{ml_model.name}/{ml_model.version}/" + MODEL_META_NAME
        storage_client = storage.Client(project="emart-dt-dev-ds")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(model_meta_path)
