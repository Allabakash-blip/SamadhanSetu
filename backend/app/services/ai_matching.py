from __future__ import annotations

import math
import re
from typing import Any

from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.user import (
    User,
    UserRole,
    AccountStatus,
    UniversityProfile,
    IndustryProfile,
    GovernmentProfile,
)


CATEGORY_RULES = {
    "Water Resources": {
        "water", "drinking", "purified", "purification", "pipeline", "tap",
        "borewell", "well", "irrigation", "drainage", "sewage", "toilet",
        "flood", "water shortage", "water supply",
    },
    "Sanitation": {
        "sanitation", "toilet", "sewer", "sewage", "garbage", "hygiene",
        "drain", "wastewater",
    },
    "Healthcare": {
        "hospital", "health", "healthcare", "clinic", "medicine", "doctor",
        "ambulance", "disease", "maternal", "medical",
    },
    "Education": {
        "school", "college", "education", "teacher", "student", "classroom",
        "library", "learning", "digital education",
    },
    "Agriculture": {
        "farmer", "farming", "agriculture", "crop", "irrigation", "seed",
        "fertilizer", "soil", "pesticide", "livestock",
    },
    "Roads & Transport": {
        "road", "pothole", "transport", "bus", "traffic", "bridge", "street",
        "highway", "footpath", "vehicle",
    },
    "Electricity": {
        "electricity", "power", "transformer", "voltage", "streetlight",
        "electric", "solar",
    },
    "Environment": {
        "pollution", "environment", "air", "river", "forest", "climate",
        "plastic", "emission", "conservation",
    },
    "Waste Management": {
        "waste", "garbage", "dump", "landfill", "recycling", "recycle",
        "solid waste", "plastic waste",
    },
    "Public Safety": {
        "crime", "safety", "security", "accident", "fire", "emergency",
        "street light", "lighting", "women safety",
    },
    "Employment": {
        "job", "employment", "unemployment", "skill", "training", "livelihood",
        "income", "work",
    },
}


EXPERTISE_TERMS = {
    "Water Resources": {
        "water", "hydrology", "hydraulics", "civil engineering",
        "environmental engineering", "water treatment", "wastewater",
        "sanitation", "irrigation", "public health",
    },
    "Sanitation": {
        "sanitation", "civil engineering", "environmental engineering",
        "waste management", "public health",
    },
    "Healthcare": {
        "healthcare", "medical", "medicine", "public health", "hospital",
        "biomedical", "health technology",
    },
    "Education": {
        "education", "teaching", "learning", "edtech", "computer science",
        "social science",
    },
    "Agriculture": {
        "agriculture", "agri", "agronomy", "soil", "irrigation", "farming",
        "food technology", "rural development",
    },
    "Roads & Transport": {
        "civil engineering", "transportation", "transport", "traffic",
        "infrastructure", "urban planning",
    },
    "Electricity": {
        "electrical engineering", "electronics", "power", "energy",
        "renewable energy", "solar",
    },
    "Environment": {
        "environment", "environmental engineering", "ecology", "climate",
        "sustainability", "renewable energy",
    },
    "Waste Management": {
        "waste management", "environmental engineering", "recycling",
        "sustainability", "solid waste",
    },
    "Public Safety": {
        "public safety", "security", "civil engineering", "electronics",
        "emergency management",
    },
    "Employment": {
        "skill development", "employment", "business", "entrepreneurship",
        "vocational training", "social work",
    },
}


# Organization-level capabilities used when a profile does not contain
# an exact expertise phrase but the organization type is still relevant.
ORGANIZATION_CAPABILITIES = {
    "Water Resources": {
        "UNIVERSITY": {
            "research", "civil engineering", "environmental engineering",
            "water", "hydrology", "irrigation",
        },
        "INDUSTRY": {
            "water treatment", "water technology", "infrastructure",
            "irrigation", "engineering", "construction",
        },
        "GOVERNMENT": {
            "water", "irrigation", "municipal", "rural development",
            "public works", "water supply",
        },
    },
    "Sanitation": {
        "UNIVERSITY": {
            "sanitation", "environmental", "civil engineering", "public health",
        },
        "INDUSTRY": {
            "sanitation", "waste management", "environmental", "construction",
        },
        "GOVERNMENT": {
            "sanitation", "municipal", "public health", "rural development",
        },
    },
    "Healthcare": {
        "UNIVERSITY": {
            "medical", "healthcare", "public health", "biomedical",
        },
        "INDUSTRY": {
            "healthcare", "medical", "pharmaceutical", "biomedical",
        },
        "GOVERNMENT": {
            "health", "medical", "public health", "hospital",
        },
    },
    "Education": {
        "UNIVERSITY": {
            "education", "teaching", "learning", "computer science",
        },
        "INDUSTRY": {
            "education", "edtech", "technology", "training",
        },
        "GOVERNMENT": {
            "education", "school", "training", "learning",
        },
    },
    "Agriculture": {
        "UNIVERSITY": {
            "agriculture", "agronomy", "soil", "irrigation", "rural development",
        },
        "INDUSTRY": {
            "agriculture", "agri", "farming", "fertilizer", "food technology",
        },
        "GOVERNMENT": {
            "agriculture", "farming", "rural development", "irrigation",
        },
    },
    "Roads & Transport": {
        "UNIVERSITY": {
            "civil engineering", "transportation", "transport", "urban planning",
        },
        "INDUSTRY": {
            "transport", "construction", "infrastructure", "automotive",
        },
        "GOVERNMENT": {
            "transport", "roads", "public works", "infrastructure",
        },
    },
    "Electricity": {
        "UNIVERSITY": {
            "electrical engineering", "electronics", "power", "energy",
        },
        "INDUSTRY": {
            "electric", "power", "energy", "solar", "renewable",
        },
        "GOVERNMENT": {
            "electricity", "power", "energy", "renewable",
        },
    },
    "Environment": {
        "UNIVERSITY": {
            "environment", "ecology", "climate", "sustainability",
        },
        "INDUSTRY": {
            "environment", "recycling", "sustainability", "renewable",
        },
        "GOVERNMENT": {
            "environment", "forest", "climate", "conservation",
        },
    },
    "Waste Management": {
        "UNIVERSITY": {
            "waste management", "environmental", "recycling", "sustainability",
        },
        "INDUSTRY": {
            "waste management", "recycling", "solid waste", "environmental",
        },
        "GOVERNMENT": {
            "waste", "municipal", "sanitation", "recycling",
        },
    },
    "Public Safety": {
        "UNIVERSITY": {
            "public safety", "security", "electronics", "emergency management",
        },
        "INDUSTRY": {
            "security", "safety", "electronics", "emergency",
        },
        "GOVERNMENT": {
            "public safety", "security", "police", "emergency",
        },
    },
    "Employment": {
        "UNIVERSITY": {
            "skill development", "education", "vocational training",
            "entrepreneurship", "social work",
        },
        "INDUSTRY": {
            "employment", "business", "entrepreneurship", "training",
        },
        "GOVERNMENT": {
            "employment", "skill development", "livelihood", "training",
        },
    },
}


def _normalise(value: Any) -> str:
    """Convert arbitrary profile/problem values into searchable text."""
    return str(value or "").strip().lower()


def _contains_phrase(text: str, phrase: str) -> bool:
    """
    Match a phrase against text using word boundaries where possible.

    This avoids treating a short term such as 'air' as a match inside
    an unrelated word.
    """
    text = _normalise(text)
    phrase = _normalise(phrase)

    if not phrase:
        return False

    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def _text(problem: Problem) -> str:
    return " ".join(
        str(value or "")
        for value in [
            problem.title,
            problem.description,
            problem.additional_details,
            problem.category,
        ]
    ).lower()


def classify_problem(problem: Problem) -> dict:
    text = _text(problem)

    scores: dict[str, int] = {}
    evidence: dict[str, list[str]] = {}

    for category, keywords in CATEGORY_RULES.items():
        matched = [
            keyword
            for keyword in keywords
            if _contains_phrase(text, keyword)
        ]

        if matched:
            # Exact multi-word phrases are stronger than single terms.
            score = sum(
                3 if " " in keyword else 2
                for keyword in matched
            )

            scores[category] = score
            evidence[category] = matched

    supplied = (
        problem.category
        if problem.category in CATEGORY_RULES
        else None
    )

    if supplied:
        scores[supplied] = scores.get(supplied, 0) + 2

    if scores:
        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        predicted = ranked[0][0]
        max_score = ranked[0][1]
        second = ranked[1][1] if len(ranked) > 1 else 0

        confidence = min(
            97,
            55
            + max_score * 5
            + max(0, max_score - second) * 3,
        )

        keywords = evidence.get(predicted, [])

    else:
        predicted = supplied or "Other"
        confidence = 55 if supplied else 45
        keywords = []

    urgent_terms = {
        "urgent", "emergency", "critical", "immediate", "danger",
        "life threatening", "outbreak", "accident", "unsafe", "shortage",
    }

    high_terms = {
        "severe", "serious", "no water", "no electricity", "hospital",
        "disease", "flood", "fire", "contamination",
    }

    critical = any(
        _contains_phrase(text, term)
        for term in urgent_terms
    )

    high = any(
        _contains_phrase(text, term)
        for term in high_terms
    )

    affected = problem.affected_people or 0

    if critical or affected >= 1000:
        priority = "CRITICAL"
        priority_reason = (
            "Urgent/critical language or very high reported impact."
        )
    elif high or affected >= 200:
        priority = "HIGH"
        priority_reason = (
            "High-severity indicators or substantial reported impact."
        )
    elif affected >= 50:
        priority = "MEDIUM"
        priority_reason = "Moderate reported impact."
    else:
        priority = "MEDIUM"
        priority_reason = (
            "Default review priority; administrator can adjust it."
        )

    expertise = list(
        EXPERTISE_TERMS.get(predicted, set())
    )

    return {
        "predicted_category": predicted,
        "confidence": round(float(confidence), 1),
        "priority": priority,
        "priority_reason": priority_reason,
        "matched_keywords": keywords[:12],
        "required_expertise": expertise[:8],
        "method": "Rule-based NLP baseline",
        "note": (
            "This baseline uses transparent keyword/phrase scoring. "
            "It is designed to work without an external AI API and can "
            "later be replaced or augmented with an LLM."
        ),
    }


def _profile_data(
    user: User,
) -> dict[str, Any]:
    """
    Extract all matching-relevant information from a representative.

    Keeping this in one place makes the scoring model easier to understand
    and prevents University, Industry and Government logic from drifting
    apart.
    """

    role = user.role.value if user.role else ""

    organization = ""
    expertise_text = ""
    experience_text = ""
    state_id = None
    district_id = None
    latitude = None
    longitude = None
    availability_status = "AVAILABLE"

    if (
        user.role == UserRole.UNIVERSITY
        and user.university_profile
    ):
        profile = user.university_profile

        organization = profile.university_name or ""

        expertise_text = " ".join(
            [
                profile.department or "",
                profile.expertise or "",
            ]
        )

        experience_text = " ".join(
            [
                profile.relevant_experience or "",
                profile.expertise or "",
                profile.department or "",
            ]
        )

        state_id = profile.state_id
        district_id = profile.district_id
        latitude = profile.latitude
        longitude = profile.longitude

        availability_status = (
            profile.availability_status
            or "AVAILABLE"
        )

    elif (
        user.role == UserRole.INDUSTRY
        and user.industry_profile
    ):
        profile = user.industry_profile

        organization = profile.company_name or ""

        expertise_text = " ".join(
            [
                profile.company_type or "",
                profile.expertise or "",
                profile.available_support or "",
            ]
        )

        experience_text = " ".join(
            [
                profile.relevant_experience or "",
                profile.expertise or "",
                profile.available_support or "",
                profile.company_type or "",
            ]
        )

        state_id = profile.state_id
        district_id = profile.district_id
        latitude = profile.latitude
        longitude = profile.longitude

        availability_status = (
            profile.availability_status
            or "AVAILABLE"
        )

    elif (
        user.role == UserRole.GOVERNMENT
        and user.government_profile
    ):
        profile = user.government_profile

        organization = profile.department or ""

        expertise_text = " ".join(
            [
                profile.department or "",
                profile.designation or "",
            ]
        )

        experience_text = " ".join(
            [
                profile.relevant_experience or "",
                profile.department or "",
                profile.designation or "",
            ]
        )

        state_id = profile.state_id
        district_id = profile.district_id
        latitude = profile.latitude
        longitude = profile.longitude

        availability_status = (
            profile.availability_status
            or "AVAILABLE"
        )

    return {
        "role": role,
        "organization": organization,
        "expertise_text": expertise_text,
        "experience_text": experience_text,
        "state_id": state_id,
        "district_id": district_id,
        "latitude": latitude,
        "longitude": longitude,
        "availability_status": availability_status,
    }


def _profile_category_hits(
    profile_text: str,
    category: str,
) -> list[str]:
    """Return category keywords found in a representative profile."""

    keywords = CATEGORY_RULES.get(category, set())

    return [
        keyword
        for keyword in keywords
        if _contains_phrase(profile_text, keyword)
    ]


def _expertise_score(
    profile_text: str,
    required_expertise: list[str],
) -> tuple[int, list[str]]:
    """
    Score direct expertise alignment.

    Maximum: 25 points.
    """

    if not required_expertise:
        return 0, []

    hits = [
        term
        for term in required_expertise
        if _contains_phrase(profile_text, term)
    ]

    if not hits:
        return 0, []

    # The first few strong expertise matches carry most of the score.
    points = min(25, len(hits) * 7 + 4)

    return points, hits[:5]


def _category_score(
    profile_text: str,
    role: str,
    category: str,
) -> tuple[int, list[str]]:
    """
    Score how relevant the representative's profile is to the
    problem category.

    Maximum: 20 points.
    """

    if category == "Other":
        return 8, ["Problem category could not be confidently classified."]

    category_hits = _profile_category_hits(
        profile_text,
        category,
    )

    if category_hits:
        points = min(
            20,
            10 + len(category_hits) * 3,
        )

        return points, category_hits[:4]

    # Fall back to organization-level capability.
    capability_terms = (
        ORGANIZATION_CAPABILITIES
        .get(category, {})
        .get(role, set())
    )

    capability_hits = [
        term
        for term in capability_terms
        if _contains_phrase(profile_text, term)
    ]

    if capability_hits:
        points = min(
            16,
            8 + len(capability_hits) * 3,
        )

        return points, capability_hits[:4]

    return 0, []


def _haversine_distance_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    """Calculate approximate great-circle distance in kilometres."""

    radius_km = 6371.0

    lat1 = math.radians(latitude_1)
    lat2 = math.radians(latitude_2)

    delta_lat = math.radians(
        latitude_2 - latitude_1
    )

    delta_lon = math.radians(
        longitude_2 - longitude_1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return radius_km * c


def _location_score(
    problem: Problem,
    profile_data: dict[str, Any],
) -> tuple[int, list[str]]:
    """
    Score geographical relevance.

    Maximum: 15 points.

    Exact district:
        15

    Same state:
        10

    Nearby coordinates:
        Up to 10

    Otherwise:
        0
    """

    problem_state_id = getattr(
        problem,
        "state_id",
        None,
    )

    problem_district_id = getattr(
        problem,
        "district_id",
        None,
    )

    profile_state_id = profile_data["state_id"]
    profile_district_id = profile_data["district_id"]

    if (
        problem_district_id
        and profile_district_id
        and problem_district_id == profile_district_id
    ):
        return 15, [
            "Representative is in the same district as the problem."
        ]

    if (
        problem_state_id
        and profile_state_id
        and problem_state_id == profile_state_id
    ):
        return 10, [
            "Representative is in the same state as the problem."
        ]

    problem_latitude = getattr(
        problem,
        "latitude",
        None,
    )

    problem_longitude = getattr(
        problem,
        "longitude",
        None,
    )

    profile_latitude = profile_data["latitude"]
    profile_longitude = profile_data["longitude"]

    if all(
        value is not None
        for value in [
            problem_latitude,
            problem_longitude,
            profile_latitude,
            profile_longitude,
        ]
    ):
        distance = _haversine_distance_km(
            float(problem_latitude),
            float(problem_longitude),
            float(profile_latitude),
            float(profile_longitude),
        )

        if distance <= 10:
            return 15, [
                f"Representative is approximately {distance:.1f} km from the problem."
            ]

        if distance <= 25:
            return 12, [
                f"Representative is approximately {distance:.1f} km from the problem."
            ]

        if distance <= 50:
            return 9, [
                f"Representative is approximately {distance:.1f} km from the problem."
            ]

        if distance <= 100:
            return 6, [
                f"Representative is approximately {distance:.1f} km from the problem."
            ]

        if distance <= 250:
            return 3, [
                f"Representative is approximately {distance:.1f} km from the problem."
            ]

    return 0, []


def _organization_capability_score(
    role: str,
    category: str,
    profile_text: str,
) -> tuple[int, list[str]]:
    """
    Score the organization's practical ability to contribute.

    Maximum: 15 points.
    """

    capability_terms = (
        ORGANIZATION_CAPABILITIES
        .get(category, {})
        .get(role, set())
    )

    hits = [
        term
        for term in capability_terms
        if _contains_phrase(profile_text, term)
    ]

    if hits:
        points = min(
            15,
            6 + len(hits) * 3,
        )

        if role == "UNIVERSITY":
            reason_prefix = "University capability"
        elif role == "INDUSTRY":
            reason_prefix = "Industry capability"
        else:
            reason_prefix = "Government capability"

        return points, [
            f"{reason_prefix} matches: "
            + ", ".join(hits[:4])
        ]

    # Organization type itself provides a small baseline capability.
    if role == "UNIVERSITY":
        return 5, [
            "University can contribute research and technical expertise."
        ]

    if role == "INDUSTRY":
        return 5, [
            "Industry can contribute implementation and technical support."
        ]

    if role == "GOVERNMENT":
        return 5, [
            "Government can contribute public-service coordination and implementation."
        ]

    return 0, []


def _availability_score(
    availability_status: str,
) -> tuple[int, list[str]]:
    """
    Score current availability.

    Maximum: 10 points.
    """

    status = _normalise(
        availability_status
    ).upper()

    if status == "AVAILABLE":
        return 10, [
            "Representative is currently available."
        ]

    if status == "LIMITED":
        return 5, [
            "Representative has limited availability."
        ]

    if status == "UNAVAILABLE":
        return 0, [
            "Representative is currently unavailable."
        ]

    # Existing profiles created before Feature 08 receive a neutral
    # available status through the model/API defaults.
    return 10, [
        "Availability has not been explicitly changed; default is available."
    ]


def _experience_score(
    problem: Problem,
    profile_data: dict[str, Any],
    analysis: dict,
    user: User,
) -> tuple[int, list[str]]:
    """
    Score relevant experience.

    Maximum: 15 points.

    The score combines:
    - explicit years of experience
    - matching terms in relevant experience
    """

    experience_text = profile_data["experience_text"]

    required_terms = (
        analysis.get("required_expertise", [])
    )

    experience_hits = [
        term
        for term in required_terms
        if _contains_phrase(experience_text, term)
    ]

    years = None

    if (
        user.role == UserRole.UNIVERSITY
        and user.university_profile
    ):
        years = user.university_profile.years_of_experience

    elif (
        user.role == UserRole.INDUSTRY
        and user.industry_profile
    ):
        years = user.industry_profile.years_of_experience

    elif (
        user.role == UserRole.GOVERNMENT
        and user.government_profile
    ):
        years = user.government_profile.years_of_experience

    points = 0
    reasons = []

    # Explicit relevant experience contributes up to 9 points.
    if experience_hits:
        experience_points = min(
            9,
            len(experience_hits) * 3,
        )

        points += experience_points

        reasons.append(
            "Relevant experience mentions: "
            + ", ".join(experience_hits[:4])
        )

    # Years of experience contributes up to 6 points.
    if years is not None:
        try:
            years_value = max(0, int(years))
        except (TypeError, ValueError):
            years_value = 0

        years_points = min(
            6,
            years_value // 2,
        )

        if years_value > 0:
            points += years_points

            reasons.append(
                f"{years_value} years of stated experience."
            )

    return min(points, 15), reasons


def _match_score(
    problem: Problem,
    user: User,
    analysis: dict,
) -> tuple[int, list[str], dict[str, Any]]:
    """
    Calculate an explainable representative score.

    Total = 100 points:

        Expertise          25
        Category relevance 20
        Location           15
        Organization       15
        Availability       10
        Experience         15
    """

    profile_data = _profile_data(user)

    role = profile_data["role"]

    # Include expertise, organization information and relevant experience
    # when searching for matching terms.
    profile_text = " ".join(
        [
            profile_data["expertise_text"],
            profile_data["experience_text"],
            profile_data["organization"],
        ]
    ).lower()

    category = analysis.get(
        "predicted_category",
        "Other",
    )

    expertise_points, expertise_hits = _expertise_score(
        profile_text,
        analysis.get("required_expertise", []),
    )

    category_points, category_hits = _category_score(
        profile_text,
        role,
        category,
    )

    location_points, location_reasons = _location_score(
        problem,
        profile_data,
    )

    capability_points, capability_reasons = (
        _organization_capability_score(
            role,
            category,
            profile_text,
        )
    )

    availability_points, availability_reasons = (
        _availability_score(
            profile_data["availability_status"]
        )
    )

    experience_points, experience_reasons = (
        _experience_score(
            problem,
            profile_data,
            analysis,
            user,
        )
    )

    breakdown = {
        "expertise": {
            "score": expertise_points,
            "max_score": 25,
            "matched_terms": expertise_hits,
        },
        "category_relevance": {
            "score": category_points,
            "max_score": 20,
            "matched_terms": category_hits,
        },
        "location": {
            "score": location_points,
            "max_score": 15,
        },
        "organization_capability": {
            "score": capability_points,
            "max_score": 15,
        },
        "availability": {
            "score": availability_points,
            "max_score": 10,
            "status": profile_data["availability_status"],
        },
        "relevant_experience": {
            "score": experience_points,
            "max_score": 15,
        },
    }

    score = (
        expertise_points
        + category_points
        + location_points
        + capability_points
        + availability_points
        + experience_points
    )

    reasons = []

    if expertise_hits:
        reasons.append(
            "Expertise match: "
            + ", ".join(expertise_hits[:4])
            + f" (+{expertise_points}/25)"
        )

    if category_hits:
        reasons.append(
            "Category relevance: "
            + ", ".join(category_hits[:4])
            + f" (+{category_points}/20)"
        )

    reasons.extend(
        [
            f"{reason} (+{location_points}/15)"
            for reason in location_reasons
        ]
    )

    reasons.extend(
        [
            f"{reason} (+{capability_points}/15)"
            for reason in capability_reasons
        ]
    )

    reasons.extend(
        [
            f"{reason} (+{availability_points}/10)"
            for reason in availability_reasons
        ]
    )

    reasons.extend(
        [
            f"{reason} (+{experience_points}/15)"
            for reason in experience_reasons
        ]
    )

    if not reasons:
        reasons.append(
            "Limited matching evidence was found in the representative profile."
        )

    return min(score, 100), reasons, breakdown


def find_matches(
    db: Session,
    problem: Problem,
    analysis: dict,
    limit: int = 5,
) -> list[dict]:
    """
    Find verified, active representatives and rank them using
    the transparent Feature 08 scoring model.
    """

    users = (
        db.query(User)
        .outerjoin(UniversityProfile)
        .outerjoin(IndustryProfile)
        .outerjoin(GovernmentProfile)
        .filter(
            User.role.in_(
                [
                    UserRole.UNIVERSITY,
                    UserRole.INDUSTRY,
                    UserRole.GOVERNMENT,
                ]
            ),
            User.account_status == AccountStatus.ACTIVE,
        )
        .all()
    )

    matches = []

    for user in users:

        if user.role == UserRole.UNIVERSITY:
            profile = user.university_profile

        elif user.role == UserRole.INDUSTRY:
            profile = user.industry_profile

        else:
            profile = user.government_profile

        # Only approved representatives participate in matching.
        if (
            not profile
            or getattr(
                profile,
                "verification_status",
                None,
            ) != "APPROVED"
        ):
            continue

        score, reasons, breakdown = _match_score(
            problem,
            user,
            analysis,
        )

        profile_data = _profile_data(user)

        matches.append(
            {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": profile_data["role"],
                "organization": profile_data["organization"],
                "score": score,
                "match_reasons": reasons,
                "score_breakdown": breakdown,
                "availability_status": (
                    profile_data["availability_status"]
                ),
            }
        )

    matches.sort(
        key=lambda item: (
            -item["score"],
            item["name"].lower(),
        )
    )

    for index, match in enumerate(
        matches[:limit],
        start=1,
    ):
        match["rank"] = index

    return matches[:limit]