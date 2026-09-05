from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class ProblemCreate(BaseModel):
    title: str
    description: str
    category: str
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    block_id: Optional[int] = None
    village_id: Optional[int] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    affected_people: Optional[int] = None
    additional_details: Optional[str] = None

class ProblemMediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    media_type: str
    url: str
    original_filename: Optional[str] = None

class ProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    category: str
    status: str
    priority: str
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    block_id: Optional[int] = None
    village_id: Optional[int] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    affected_people: Optional[int] = None
    additional_details: Optional[str] = None
    created_at: datetime
    media: List[ProblemMediaResponse] = Field(default_factory=list)
