from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List, Union

from pydantic import BaseModel


class PermissionType(Enum):
    USER_ID = "USER_ID"
    GROUP = "GROUP"
    ROLE = "ROLE"


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


class PermissionRequest(BaseModel):
    resource_id: str
    permission_type: PermissionType
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool


class Field(BaseModel):
    logical_name: str
    type: FieldType


@dataclass
class DocumentRequest:
    name: str
    type: str  # TODO make enum
    classification: str
    document: Union[str, Dict]


@dataclass
class SearchDocumentRequest:
    name: Optional[str]
    type: Optional[str]  # TODO make enum
    classification: Optional[str]
    is_released: Optional[bool]


@dataclass
class Document:
    pk: str
    parent_pk: str
    original_pk: str
    name: str
    type: str  # TODO make enum
    classification: str
    document: Union[str, Dict]
    created_by: str
    created_at: int
    updated_by: str
    updated_at: int
    released_by: str
    released_at: int
    is_released: bool
    deleted_by: str
    deleted_at: int
    is_deleted: bool


@dataclass
class DatasetSearchRequest:
    query: str
    data_types: Optional[List[str]]  # TODO make enum


@dataclass
class DatasetSummaryResponse:
    id: str
    display_name: str
    logical_name: str
    description: Optional[str]
    data_type: str  # TODO make enum
    tag: str
