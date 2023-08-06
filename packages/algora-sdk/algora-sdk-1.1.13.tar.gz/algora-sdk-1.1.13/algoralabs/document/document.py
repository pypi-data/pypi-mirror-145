from dataclasses import asdict
from typing import List

from algoralabs.common.enum import PermissionRequest, Document, DocumentRequest, SearchDocumentRequest
from algoralabs.common.requests import __delete_request, __put_request, __get_request, __post_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_document(id: str) -> Document:
    endpoint = f"document-registry/documents/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def search_documents(request: SearchDocumentRequest) -> List[Document]:
    endpoint = f"document-registry/documents/search"
    return __post_request(endpoint, json=asdict(request))


@data_request(transformer=no_transform)
def create_document(request: DocumentRequest) -> Document:
    endpoint = f"document-registry/documents"
    return __post_request(endpoint, json=asdict(request))


@data_request(transformer=no_transform)
def update_document(id: str, request: DocumentRequest) -> Document:
    endpoint = f"document-registry/documents/{id}"
    return __put_request(endpoint, json=asdict(request))


@data_request(transformer=no_transform)
def delete_document(id: str) -> None:
    endpoint = f"document-registry/documents/{id}"
    return __delete_request(endpoint)


@data_request(transformer=no_transform)
def create_permission(request: PermissionRequest):
    endpoint = f"document-registry/documents/permission"
    return __put_request(endpoint, json=request.json())
