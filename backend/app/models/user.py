from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum


class UserRole(str, enum.Enum):
    CITIZEN = "CITIZEN"
    UNIVERSITY = "UNIVERSITY"
    INDUSTRY = "INDUSTRY"
    GOVERNMENT = "GOVERNMENT"
    COMMUNITY_GROUP = "COMMUNITY_GROUP"
    PRI = "PRI"
    ULB = "ULB"
    ADMIN = "ADMIN"


class AccountStatus(str, enum.Enum):
    INCOMPLETE = "INCOMPLETE"
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class User(Base):
    __tablename__ = "users"

<<<<<<< HEAD
    citizen_profile = relationship("CitizenProfile", back_populates="user", uselist=False)
    university_profile = relationship("UniversityProfile", back_populates="user", uselist=False)
    industry_profile = relationship("IndustryProfile", back_populates="user", uselist=False)
    government_profile = relationship("GovernmentProfile", back_populates="user", uselist=False)
    civic_profile = relationship("CivicOrganizationProfile", back_populates="user", uselist=False)
=======
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    profile_picture_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    google_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True
    )

    role: Mapped[UserRole | None] = mapped_column(
        Enum(UserRole),
        nullable=True
    )

    account_status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus),
        default=AccountStatus.INCOMPLETE,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    citizen_profile = relationship(
        "CitizenProfile",
        back_populates="user",
        uselist=False
    )

    university_profile = relationship(
        "UniversityProfile",
        back_populates="user",
        uselist=False
    )

    industry_profile = relationship(
        "IndustryProfile",
        back_populates="user",
        uselist=False
    )

    government_profile = relationship(
        "GovernmentProfile",
        back_populates="user",
        uselist=False
    )

>>>>>>> my-changes
    problems = relationship(
        "Problem",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    industry_support_offers = relationship(
        "IndustrySupportOffer",
        foreign_keys="IndustrySupportOffer.industry_id",
        cascade="all, delete-orphan"
    )

    industry_partnerships = relationship(
        "IndustryPartnership",
        foreign_keys="IndustryPartnership.industry_id",
        cascade="all, delete-orphan"
    )


class State(Base):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    code: Mapped[str | None] = mapped_column(
        String(10),
        unique=True
    )


class District(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    state_id: Mapped[int] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )


class Village(Base):
    __tablename__ = "villages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    block_id: Mapped[int] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


class CitizenProfile(Base):
    __tablename__ = "citizen_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    address_line: Mapped[str | None] = mapped_column(
        Text
    )

    state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id")
    )

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id")
    )

    block_id: Mapped[int | None] = mapped_column(
        ForeignKey("blocks.id")
    )

    village_id: Mapped[int | None] = mapped_column(
        ForeignKey("villages.id")
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10)
    )

    latitude: Mapped[float | None] = mapped_column(
        Float
    )

    longitude: Mapped[float | None] = mapped_column(
        Float
    )

    user = relationship(
        "User",
        back_populates="citizen_profile"
    )


class UniversityProfile(Base):
    __tablename__ = "university_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    university_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    university_type: Mapped[str | None] = mapped_column(
        String(100)
    )

    registration_number: Mapped[str | None] = mapped_column(
        String(100)
    )

    department: Mapped[str | None] = mapped_column(
        String(200)
    )

    designation: Mapped[str | None] = mapped_column(
        String(150)
    )

    address: Mapped[str | None] = mapped_column(
        Text
    )

    state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id")
    )

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id")
    )

    city: Mapped[str | None] = mapped_column(
        String(150)
    )

    expertise: Mapped[str | None] = mapped_column(
        Text
    )

    # Feature 08: Advanced Representative Matching
    availability_status: Mapped[str] = mapped_column(
        String(30),
        default="AVAILABLE",
        nullable=False
    )

    relevant_experience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    years_of_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    verification_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING"
    )

    user = relationship(
        "User",
        back_populates="university_profile"
    )


class IndustryProfile(Base):
    __tablename__ = "industry_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    company_type: Mapped[str | None] = mapped_column(
        String(100)
    )

    website: Mapped[str | None] = mapped_column(
        String(255)
    )

    address: Mapped[str | None] = mapped_column(
        Text
    )

    state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id")
    )

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id")
    )

    city: Mapped[str | None] = mapped_column(
        String(150)
    )

    expertise: Mapped[str | None] = mapped_column(
        Text
    )

    available_support: Mapped[str | None] = mapped_column(
        Text
    )

    # Feature 08: Advanced Representative Matching
    availability_status: Mapped[str] = mapped_column(
        String(30),
        default="AVAILABLE",
        nullable=False
    )

    relevant_experience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    years_of_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    verification_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING"
    )

    user = relationship(
        "User",
        back_populates="industry_profile"
    )


class GovernmentProfile(Base):
    __tablename__ = "government_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    designation: Mapped[str | None] = mapped_column(
        String(150)
    )

    official_id: Mapped[str | None] = mapped_column(
        String(100)
    )

    state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id")
    )

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id")
    )

<<<<<<< HEAD


class CivicOrganizationProfile(Base):
    """Profile for non-individual challenge submitters: community groups, PRIs and ULBs."""
    __tablename__ = "civic_organization_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False, index=True)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_type: Mapped[str] = mapped_column(String(40), nullable=False)
    registration_number: Mapped[str | None] = mapped_column(String(120), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    state_id: Mapped[int | None] = mapped_column(ForeignKey("states.id"), nullable=True)
    district_id: Mapped[int | None] = mapped_column(ForeignKey("districts.id"), nullable=True)
    block_id: Mapped[int | None] = mapped_column(ForeignKey("blocks.id"), nullable=True)
    village_id: Mapped[int | None] = mapped_column(ForeignKey("villages.id"), nullable=True)
    city: Mapped[str | None] = mapped_column(String(150), nullable=True)
    ward: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    verification_status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False)

    user = relationship("User", back_populates="civic_profile")
=======
    # Feature 08: Advanced Representative Matching
    availability_status: Mapped[str] = mapped_column(
        String(30),
        default="AVAILABLE",
        nullable=False
    )

    relevant_experience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    years_of_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    verification_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING"
    )

    user = relationship(
        "User",
        back_populates="government_profile"
    )
>>>>>>> my-changes
