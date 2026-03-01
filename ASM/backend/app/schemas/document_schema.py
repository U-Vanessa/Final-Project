from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


DocumentPriority = Literal["low", "medium", "high", "critical"]


class DocumentCreateRequest(BaseModel):
    date: str
    name_of_staff: str = Field(min_length=2)
    position: str = Field(min_length=2)
    division: str = Field(min_length=2)
    device_model: str = Field(min_length=2)
    device_serial_number: str = Field(min_length=2)
    rab_asset_code: str | None = None
    nature_of_problem: str = Field(min_length=3)
    observation: str | None = None
    key_recommendation: str | None = None
    priority: DocumentPriority = "medium"
    voucher_id: int | None = None
    submitted_by_email: str | None = None


class DocumentResponse(BaseModel):
    id: int
    document_ref: str
    date: str
    name_of_staff: str
    position: str
    division: str
    device_model: str
    device_serial_number: str
    rab_asset_code: str | None = None
    nature_of_problem: str
    observation: str | None = None
    key_recommendation: str | None = None
    priority: str
    status: str
    submitted_by_id: int | None = None
    voucher_id: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentLinkRequest(BaseModel):
    voucher_id: int | None = None
