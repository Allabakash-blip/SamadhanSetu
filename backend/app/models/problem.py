from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base

import enum


class ProblemStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    VALIDATED = "VALIDATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    SOLUTION_PROPOSED = "SOLUTION_PROPOSED"
    PILOT = "PILOT"
    IMPLEMENTED = "IMPLEMENTED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"


class ProblemPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"



class SolutionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    IMPLEMENTATION_STARTED = "IMPLEMENTATION_STARTED"
    IMPLEMENTED = "IMPLEMENTED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    proposer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    benefits = Column(Text, nullable=True)
    estimated_cost = Column(String(100), nullable=True)
    required_resources = Column(Text, nullable=True)
    implementation_time = Column(String(100), nullable=True)
    status = Column(Enum(SolutionStatus), default=SolutionStatus.PROPOSED, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    problem = relationship("Problem", back_populates="solutions")
    proposer = relationship("User", foreign_keys=[proposer_id])
    media = relationship("SolutionMedia", back_populates="solution", cascade="all, delete-orphan")
    feedback = relationship("SolutionFeedback", back_populates="solution", cascade="all, delete-orphan", order_by="SolutionFeedback.created_at")
    implementation_updates = relationship("ImplementationUpdate", back_populates="solution", cascade="all, delete-orphan", order_by="ImplementationUpdate.created_at")


class SolutionMedia(Base):
    __tablename__ = "solution_media"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("solutions.id"), nullable=False, index=True)
    media_type = Column(String(20), nullable=False)
    url = Column(Text, nullable=False)
    public_id = Column(String(500), nullable=True)
    original_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    solution = relationship("Solution", back_populates="media")


class SolutionFeedback(Base):
    __tablename__ = "solution_feedback"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("solutions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    feedback = Column(Text, nullable=False)
    decision = Column(String(30), nullable=False)  # APPROVE / CHANGES_REQUESTED / REJECT
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    solution = relationship("Solution", back_populates="feedback")
    user = relationship("User")


class ImplementationUpdate(Base):
    __tablename__ = "implementation_updates"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("solutions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(40), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    solution = relationship("Solution", back_populates="implementation_updates")
    user = relationship("User")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)

    # Person who submitted the problem
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Type of entity that submitted the challenge. Kept separately from the
    # user role so analytics and admin review can clearly identify the source.
    reporter_type = Column(String(40), nullable=False, default="INDIVIDUAL_CITIZEN", index=True)

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    status = Column(
        Enum(ProblemStatus),
        default=ProblemStatus.SUBMITTED,
        nullable=False,
        index=True,
    )

    priority = Column(
        Enum(ProblemPriority),
        default=ProblemPriority.MEDIUM,
        nullable=False,
    )

    # Location
    state_id = Column(
        Integer,
        ForeignKey("states.id"),
        nullable=True,
    )

    district_id = Column(
        Integer,
        ForeignKey("districts.id"),
        nullable=True,
    )

    block_id = Column(
        Integer,
        ForeignKey("blocks.id"),
        nullable=True,
    )

    village_id = Column(
        Integer,
        ForeignKey("villages.id"),
        nullable=True,
    )

    address = Column(
        Text,
        nullable=True,
    )

    pincode = Column(
        String(10),
        nullable=True,
    )

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )

    # Additional information
    affected_people = Column(
        Integer,
        nullable=True,
    )

    additional_details = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="problems",
    )

    media = relationship(
        "ProblemMedia",
        back_populates="problem",
        cascade="all, delete-orphan",
    )


    assignment = relationship("ProblemAssignment", back_populates="problem", uselist=False, cascade="all, delete-orphan")
    status_history = relationship("ProblemStatusHistory", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemStatusHistory.created_at")
    comments = relationship("ProblemComment", back_populates="problem", cascade="all, delete-orphan", order_by="ProblemComment.created_at")
    solutions = relationship("Solution", back_populates="problem", cascade="all, delete-orphan", order_by="Solution.created_at")
    industry_support_offers = relationship("IndustrySupportOffer", foreign_keys="IndustrySupportOffer.problem_id", cascade="all, delete-orphan", order_by="IndustrySupportOffer.created_at")
    industry_partnerships = relationship("IndustryPartnership", foreign_keys="IndustryPartnership.problem_id", cascade="all, delete-orphan", order_by="IndustryPartnership.created_at")


class ProblemMedia(Base):
    __tablename__ = "problem_media"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    problem_id = Column(
        Integer,
        ForeignKey("problems.id"),
        nullable=False,
        index=True,
    )

    media_type = Column(
        String(20),
        nullable=False,
    )

    url = Column(
        Text,
        nullable=False,
    )

    public_id = Column(
        String(500),
        nullable=True,
    )

    original_filename = Column(
        String(255),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    problem = relationship(
        "Problem",
        back_populates="media",
    )

class ProblemAssignment(Base):
    __tablename__ = "problem_assignments"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, unique=True, index=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_role = Column(String(30), nullable=False)
    remarks = Column(Text, nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    problem = relationship("Problem", back_populates="assignment")
    assignee = relationship("User", foreign_keys=[assignee_id])
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])


class ProblemStatusHistory(Base):
    __tablename__ = "problem_status_history"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    status = Column(String(40), nullable=False)
    note = Column(Text, nullable=True)
    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    problem = relationship("Problem", back_populates="status_history")
    changed_by = relationship("User")


class ProblemComment(Base):
    __tablename__ = "problem_comments"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    problem = relationship("Problem", back_populates="comments")
    user = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True, index=True)
    is_read = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    problem = relationship("Problem")
