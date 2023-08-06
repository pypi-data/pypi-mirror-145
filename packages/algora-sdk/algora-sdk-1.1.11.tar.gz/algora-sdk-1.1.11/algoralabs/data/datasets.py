from dataclasses import asdict
from typing import List

from algoralabs.common.enum import PermissionRequest, DatasetSearchRequest, DatasetSummaryResponse
from algoralabs.common.requests import __delete_request, __put_request, __post_request, __get_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_dataset(id: str):
    endpoint = f"data/datasets/dataset/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_datasets() -> List[DatasetSummaryResponse]:
    endpoint = f"data/datasets/dataset"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def search_datasets(request: DatasetSearchRequest) -> List[DatasetSummaryResponse]:
    endpoint = f"data/datasets/dataset/search"
    return __post_request(endpoint, json=asdict(request))


@data_request(transformer=no_transform)
def delete_field(id: str) -> None:
    endpoint = f"data/datasets/field/{id}"
    return __delete_request(endpoint)


@data_request(transformer=no_transform)
def delete_schema(id: str) -> None:
    endpoint = f"data/datasets/schema/{id}"
    return __delete_request(endpoint)


@data_request(transformer=no_transform)
def delete_dataset(id: str) -> None:
    endpoint = f"data/datasets/dataset/{id}"
    return __delete_request(endpoint)


def query_dataset(id: str, data=None, json=None):
    """
    Query dataset by ID

    Args:
        id: UUID of dataset
        data: (Optional) Data to POST
        json: (Optional) Data to POST

    Returns: HTTP Response Object
    """
    endpoint = f"data/datasets/query/{id}"
    return __post_request(endpoint, data=data, json=json)


@data_request(transformer=no_transform)
def create_permission(request: PermissionRequest):
    endpoint = f"data/datasets/permission"
    return __put_request(endpoint, json=request.json())
