from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AssignProblemRequest(BaseModel):
    assignee_id: int
    remarks: Optional[str] = None


class AdminProblemUpdateRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    note: Optional[str] = None


class RepresentativeStatusRequest(BaseModel):
    status: str
    note: Optional[str] = None


class CommentRequest(BaseModel):
    comment: str = Field(min_length=1, max_length=5000)


class RepresentativeSummary(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None
    organization: Optional[str] = None
    designation: Optional[str] = None


class AssignmentResponse(BaseModel):
    id: int
    assignee: RepresentativeSummary
    assigned_by: RepresentativeSummary
    organization_role: str
    remarks: Optional[str] = None
    assigned_at: datetime


class StatusHistoryResponse(BaseModel):
    id: int
    status: str
    note: Optional[str] = None
    changed_by: RepresentativeSummary
    created_at: datetime


class CommentResponse(BaseModel):
    id: int
    comment: str
    user: RepresentativeSummary
    created_at: datetime


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    problem_id: Optional[int] = None
    is_read: bool
    created_at: datetime


class SolutionCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=10000)
    benefits: Optional[str] = Field(default=None, max_length=5000)
    estimated_cost: Optional[str] = Field(default=None, max_length=100)
    required_resources: Optional[str] = Field(default=None, max_length=5000)
    implementation_time: Optional[str] = Field(default=None, max_length=100)


class SolutionFeedbackRequest(BaseModel):
    decision: str
    feedback: str = Field(min_length=1, max_length=5000)


class ImplementationUpdateRequest(BaseModel):
    status: str
    note: str = Field(min_length=1, max_length=5000)
