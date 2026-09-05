from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

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


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+(?:\s+[a-z0-9]+){0,2}", text.lower()))


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


def _contains_phrase(text: str, phrase: str) -> bool:
    return phrase.lower() in text


def classify_problem(problem: Problem) -> dict:
    text = _text(problem)

    scores: dict[str, int] = {}
    evidence: dict[str, list[str]] = {}

    for category, keywords in CATEGORY_RULES.items():
        matched = [k for k in keywords if _contains_phrase(text, k)]
        if matched:
            # Exact multi-word phrases are stronger than single terms.
            score = sum(3 if " " in k else 2 for k in matched)
            scores[category] = score
            evidence[category] = matched

    supplied = problem.category if problem.category in CATEGORY_RULES else None
    if supplied:
        scores[supplied] = scores.get(supplied, 0) + 2

    if scores:
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        predicted = ranked[0][0]
        max_score = ranked[0][1]
        second = ranked[1][1] if len(ranked) > 1 else 0
        confidence = min(97, 55 + max_score * 5 + max(0, max_score - second) * 3)
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
    critical = any(_contains_phrase(text, k) for k in urgent_terms)
    high = any(_contains_phrase(text, k) for k in high_terms)

    affected = problem.affected_people or 0
    if critical or affected >= 1000:
        priority = "CRITICAL"
        priority_reason = "Urgent/critical language or very high reported impact."
    elif high or affected >= 200:
        priority = "HIGH"
        priority_reason = "High-severity indicators or substantial reported impact."
    elif affected >= 50:
        priority = "MEDIUM"
        priority_reason = "Moderate reported impact."
    else:
        priority = "MEDIUM"
        priority_reason = "Default review priority; administrator can adjust it."

    expertise = list(EXPERTISE_TERMS.get(predicted, set()))
    return {
        "predicted_category": predicted,
        "confidence": round(float(confidence), 1),
        "priority": priority,
        "priority_reason": priority_reason,
        "matched_keywords": keywords[:12],
        "required_expertise": expertise[:8],
        "method": "Rule-based NLP baseline",
        "note": "This baseline uses transparent keyword/phrase scoring. It is designed to work without an external AI API and can later be replaced or augmented with an LLM.",
    }


def _profile_data(user: User) -> tuple[str, str, set[int]]:
    role = user.role.value if user.role else ""
    organization = ""
    expertise_text = ""
    location_ids: set[int] = set()

    if user.role == UserRole.UNIVERSITY and user.university_profile:
        p = user.university_profile
        organization = p.university_name or ""
        expertise_text = " ".join([p.department or "", p.expertise or ""])
        location_ids = {x for x in [p.state_id, p.district_id] if x}
    elif user.role == UserRole.INDUSTRY and user.industry_profile:
        p = user.industry_profile
        organization = p.company_name or ""
        expertise_text = " ".join([p.company_type or "", p.expertise or "", p.available_support or ""])
        location_ids = {x for x in [p.state_id, p.district_id] if x}
    elif user.role == UserRole.GOVERNMENT and user.government_profile:
        p = user.government_profile
        organization = p.department or ""
        expertise_text = " ".join([p.department or "", p.designation or ""])
        location_ids = {x for x in [p.state_id, p.district_id] if x}

    return role, organization, location_ids | set()


def _match_score(problem: Problem, user: User, analysis: dict) -> tuple[int, list[str]]:
    role, organization, location_ids = _profile_data(user)
    profile_text = ""
    if user.role == UserRole.UNIVERSITY and user.university_profile:
        p = user.university_profile
        profile_text = " ".join([p.department or "", p.expertise or "", p.address or ""])
    elif user.role == UserRole.INDUSTRY and user.industry_profile:
        p = user.industry_profile
        profile_text = " ".join([p.company_type or "", p.expertise or "", p.available_support or "", p.address or ""])
    elif user.role == UserRole.GOVERNMENT and user.government_profile:
        p = user.government_profile
        profile_text = " ".join([p.department or "", p.designation or ""])

    lower = profile_text.lower()
    expertise_hits = [
        term for term in analysis["required_expertise"]
        if term.lower() in lower
    ]

    score = 20
    reasons = []

    if expertise_hits:
        score += min(45, 15 * len(expertise_hits))
        reasons.append("Expertise match: " + ", ".join(expertise_hits[:3]))
    else:
        # Category-specific role relevance is still useful.
        if problem.category == "Water Resources" and role == "GOVERNMENT":
            score += 10
            reasons.append("Government role can coordinate public water services.")
        elif role in {"UNIVERSITY", "INDUSTRY"}:
            score += 5
            reasons.append("Organization can provide technical support.")

    if problem.state_id and problem.state_id in location_ids:
        score += 15
        reasons.append("Same state as reported problem.")
    if problem.district_id and problem.district_id in location_ids:
        score += 15
        reasons.append("Same district as reported problem.")

    # Prefer verified organization representatives, but this is enforced by query.
    if role == "UNIVERSITY":
        score += 5
        reasons.append("University representative available for technical collaboration.")
    elif role == "INDUSTRY":
        score += 5
        reasons.append("Industry representative available for implementation support.")
    elif role == "GOVERNMENT":
        score += 5
        reasons.append("Government representative can coordinate public implementation.")

    return min(score, 100), reasons


def find_matches(db: Session, problem: Problem, analysis: dict, limit: int = 5) -> list[dict]:
    users = (
        db.query(User)
        .outerjoin(UniversityProfile)
        .outerjoin(IndustryProfile)
        .outerjoin(GovernmentProfile)
        .filter(
            User.role.in_([
                UserRole.UNIVERSITY,
                UserRole.INDUSTRY,
                UserRole.GOVERNMENT,
            ]),
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

        if not profile or getattr(profile, "verification_status", None) != "APPROVED":
            continue

        score, reasons = _match_score(problem, user, analysis)
        role, organization, _ = _profile_data(user)

        matches.append({
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "role": role,
            "organization": organization,
            "score": score,
            "match_reasons": reasons,
        })

    matches.sort(key=lambda x: (-x["score"], x["name"].lower()))
    for index, match in enumerate(matches[:limit], start=1):
        match["rank"] = index
    return matches[:limit]
