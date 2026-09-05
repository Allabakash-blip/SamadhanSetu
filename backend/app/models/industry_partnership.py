from datetime import datetime
import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from app.database.connection import Base


class SupportType(str, enum.Enum):
    MENTORING = "MENTORING"
    FUNDING = "FUNDING"
    TECHNICAL = "TECHNICAL"
    PROTOTYPING = "PROTOTYPING"
    TESTING = "TESTING"
    TECHNOLOGY_TRANSFER = "TECHNOLOGY_TRANSFER"
    CSR = "CSR"
    OTHER = "OTHER"


class OfferStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class PartnershipStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"


class IndustrySupportOffer(Base):
    __tablename__ = "industry_support_offers"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    industry_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    support_type = Column(Enum(SupportType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    status = Column(Enum(OfferStatus), default=OfferStatus.PROPOSED, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class IndustryPartnership(Base):
    __tablename__ = "industry_partnerships"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    industry_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    offer_id = Column(Integer, ForeignKey("industry_support_offers.id"), nullable=True, index=True)
    support_type = Column(Enum(SupportType), nullable=False)
    scope = Column(Text, nullable=False)
    status = Column(Enum(PartnershipStatus), default=PartnershipStatus.ACTIVE, nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
