from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):

    name: str = Field(min_length=2, max_length=150)

    email: EmailStr

    phone: Optional[str] = None

    password: str = Field(min_length=8)

    role: str


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class GoogleLoginRequest(BaseModel):

    credential: str


class CompleteProfileRequest(BaseModel):

    role: str

    phone: Optional[str] = None

    address_line: Optional[str] = None

    state_id: Optional[int] = None

    district_id: Optional[int] = None

    block_id: Optional[int] = None

    village_id: Optional[int] = None

    pincode: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    university_name: Optional[str] = None

    university_type: Optional[str] = None

    registration_number: Optional[str] = None

    department: Optional[str] = None

    designation: Optional[str] = None

    city: Optional[str] = None

    expertise: Optional[str] = None

    # Feature 08: Advanced Representative Matching
    availability_status: Optional[str] = None

    relevant_experience: Optional[str] = None

    years_of_experience: Optional[int] = None

    company_name: Optional[str] = None

    company_type: Optional[str] = None

    website: Optional[str] = None

    available_support: Optional[str] = None

    government_department: Optional[str] = None
<<<<<<< HEAD

    official_id: Optional[str] = None
=======
    official_id: Optional[str] = None
    organization_name: Optional[str] = None
    organization_type: Optional[str] = None
    organization_registration_number: Optional[str] = None
    ward: Optional[str] = None
    # Government / institutional location can use city/ward; civic organizations also support block/village.
>>>>>>> origin/main
