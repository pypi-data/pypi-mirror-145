from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List, Union


@dataclass
class CoreEnum:
    name: str
    value: str


class PermissionType(Enum):
    USER_ID = CoreEnum("", "USER_ID")
    GROUP = CoreEnum("", "GROUP")
    ROLE = CoreEnum("", "ROLE")


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


@dataclass
class PermissionRequest:
    resource_id: str
    permission_type: str  # TODO
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool


@dataclass
class Field:
    logical_name: str
    type: FieldType

    def as_dict(self):
        return {
            'logical_name': self.logical_name,
            'type': self.type.value
        }


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
