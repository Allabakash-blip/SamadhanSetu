from typing import Optional
from pydantic import BaseModel, Field


class SupportOfferCreateRequest(BaseModel):
    support_type: str
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=10000)
    amount: Optional[str] = Field(default=None, max_length=100)
    duration: Optional[str] = Field(default=None, max_length=100)


class IndustryPartnershipStatusRequest(BaseModel):
    status: str


class IndustryImplementationUpdateRequest(BaseModel):
    status: str
    note: str = Field(min_length=5, max_length=10000)
