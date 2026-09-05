# 🌍 Social Innovation Collaboration Portal (SIH Portal)

> **A full-stack platform that converts citizen-reported societal problems into a structured, collaborative, measurable solution workflow.**

The **Social Innovation Collaboration Portal** is designed around a simple idea:

**Citizen Challenge → AI Classification → Institutional Matching → Solution → Industry Collaboration → Implementation → Citizen Verification → Measurable Impact**

The platform connects **Citizens, Universities, Industries, Government stakeholders, and Administrators** through one centralized workflow.

---

## 🚀 What Has Been Implemented So Far

The current implementation covers the core platform lifecycle from problem reporting through solution implementation, industry collaboration, citizen verification, and analytics.

### Current implemented flow

```text
┌──────────────┐
│    CITIZEN   │
│ Report Issue │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ AI Classification    │
│ • Category           │
│ • Confidence         │
│ • Priority           │
│ • Keywords           │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────┐
│ Institutional Matching     │
│ • University expertise     │
│ • Industry expertise      │
│ • Location/state signal    │
│ • Explainable match score  │
└────────────┬───────────────┘
             │
             ▼
┌──────────────────────────┐
│ ADMIN ASSIGNMENT         │
│ Select representative    │
└────────────┬─────────────┘
             │
             ▼
┌────────────────────────────┐
│ UNIVERSITY / INSTITUTION   │
│ Develop solution           │
│ Build team / project      │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ SOLUTION WORKFLOW          │
│ Proposed → Approved →      │
│ Implemented                │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ INDUSTRY COLLABORATION     │
│ Offer → Accept → Active →  │
│ Progress → Completed       │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ CITIZEN VERIFICATION       │
│ Verify implemented result  │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│ IMPACT & ANALYTICS         │
│ Problems • Solutions •     │
│ People affected • Outcomes │
└────────────────────────────┘
```

---

# 📌 1. Problem Statement

Citizens frequently experience local problems such as:

- Drinking-water shortages
- Pipeline leakage
- Irrigation problems
- Electricity interruptions
- Poor roads
- Lack of sanitation
- Healthcare shortages
- Public transport issues
- Street-light failures
- Environmental and drainage problems

Traditional complaint systems mainly record complaints.

This platform goes further by creating a **complete collaboration lifecycle**:

1. Capture the problem.
2. Understand and classify it.
3. Find suitable institutions.
4. Assign responsible representatives.
5. Develop a solution.
6. Bring industry support where required.
7. Track implementation.
8. Ask the citizen to verify the result.
9. Measure the resulting social impact.

---

# 🎯 2. Main Objectives

The implemented platform aims to:

- Provide a structured citizen problem-reporting system.
- Automatically classify reported problems.
- Predict problem priority.
- Extract relevant keywords and expertise requirements.
- Recommend suitable university and industry representatives.
- Make matching explainable rather than presenting an unexplained score.
- Allow administrators to manage the complete problem lifecycle.
- Allow universities to work on assigned challenges.
- Support solution proposals and approval.
- Connect industry organizations for practical support.
- Track industry implementation progress.
- Allow citizens to verify completed solutions.
- Close successfully resolved challenges.
- Provide platform-wide impact analytics.
- Maintain notifications, comments, status history, assignments, and supporting evidence.

---

# 👥 3. User Roles

## 👤 Citizen

Citizens are the source of societal challenges.

Implemented capabilities include:

- Register/login.
- Maintain a profile.
- Report a problem.
- Provide:
  - Title
  - Description
  - Priority-related information
  - Affected people
  - Address
  - Pincode
  - GPS coordinates
  - Additional details
  - Evidence/media
- View submitted problems.
- Track problem status.
- View assignments and progress.
- View proposed solutions.
- Provide solution feedback.
- Verify implemented solutions.
- Add collaboration comments.
- See resolved/closed outcomes.

---

## 🎓 University Representative

University representatives provide technical and academic expertise.

Implemented capabilities include:

- University account/profile.
- Department and designation information.
- Expertise information.
- Administrator verification.
- View assigned challenges.
- Work on assigned problems.
- Propose solutions.
- Provide solution details such as:
  - Solution title
  - Description
  - Benefits
  - Estimated cost
  - Resources
  - Implementation time
- Participate in project/team workflow.
- Track implementation-related activity.

---

## 🏭 Industry Representative

Industry representatives provide practical implementation support.

Industry support can include:

- Technical support
- Funding
- Mentoring
- Prototyping
- Testing
- CSR support
- Technology transfer
- Field implementation

Implemented industry workflow:

```text
Find Project
     ↓
Submit Support Offer
     ↓
Admin Reviews Offer
     ↓
Offer Accepted
     ↓
Active Partnership
     ↓
Implementation Progress
     ↓
Partnership Completed
```

---

## 🛠️ Administrator

Administrators control platform governance.

Implemented capabilities include:

- Admin dashboard.
- User management.
- Verification management.
- Problem management.
- Status/priority management.
- Representative assignment.
- AI classification review.
- Institutional matching.
- Industry-offer review.
- Partnership monitoring.
- Notifications.
- Impact analytics.

---

# 🤖 4. AI Classification & Institutional Matching

One of the major implemented components is the **Milestone 7 AI classification and institutional matching module**.

When a problem is analyzed, the system provides:

### Predicted Category

Example:

```text
Water Resources
```

### Confidence

Example:

```text
97%
```

### Suggested Priority

Example:

```text
CRITICAL
```

### Required Expertise

For an irrigation/water problem, the system can identify requirements such as:

```text
civil engineering
sanitation
hydraulics
environmental engineering
hydrology
irrigation
```

### Matched Keywords

Example:

```text
irrigation
water shortage
water
```

---

# 🧠 5. Explainable Matching

The matching system does not simply say:

> "Representative X is recommended."

It displays reasons for the recommendation.

Example:

```text
#1 Dr. Anil Kumar
Andhra University

70% Match

✓ Expertise match:
  civil engineering
  hydraulics
  environmental engineering

✓ University representative available
  for technical collaboration.
```

Another representative may receive a lower score because their expertise is less relevant.

Industry representatives can also be matched using signals such as:

- Expertise overlap
- Organization capability
- Same-state/location relevance
- Industry implementation capability

This makes the recommendation easier to understand and demonstrate.

---

# 🏫 6. University Data & Matching

Multiple university representatives have been added so the AI matching system has meaningful alternatives.

Current example representatives include:

| Representative | University | Expertise |
|---|---|---|
| Dr. Anil Kumar | Andhra University | Water resources, civil engineering, irrigation, hydraulics, environmental engineering |
| Dr. Priya Sharma | IIT Hyderabad | AI, ML, data science, computer vision, technology |
| Dr. Ravi Teja | JNTU Anantapur | Agriculture, irrigation, water management, rural development |
| Dr. Sneha Reddy | NIT Warangal | Electricity, renewable energy, electrical engineering, solar energy, power systems |
| Dr. Arjun Rao | IIT Madras | Environmental engineering, sanitation, waste management, water treatment, public health |

Only representatives that satisfy the platform's account/verification conditions are considered for recommendations.

---

# 🔎 7. Example AI Matching Results

## Water Resources Problem

For:

> **Drinking water pipeline leakage**

the system can recommend:

```text
#1 Dr. Anil Kumar
70% match

#2 Dr. Arjun Rao
70% match

#3 Dr. Ravi Teja
40% match
```

The result is based on expertise overlap and institutional capability.

---

## Electricity Problem

For:

> **Irregular electricity supply**

the system can identify:

```text
#1 Dr. Sneha Reddy
70% match
```

because the representative's expertise includes:

```text
energy
renewable energy
power
electrical engineering
```

This demonstrates that the matching system changes recommendations according to the actual problem.

---

# 🧩 8. Problem Lifecycle

Problems use a structured lifecycle.

Supported statuses include:

```text
SUBMITTED
     ↓
UNDER_REVIEW
     ↓
VALIDATED
     ↓
ASSIGNED
     ↓
IN_PROGRESS
     ↓
SOLUTION_PROPOSED
     ↓
PILOT
     ↓
IMPLEMENTED
     ↓
CLOSED
```

A problem may also be:

```text
REJECTED
```

when it does not pass the required review/validation process.

The status is visible to relevant users so that the lifecycle remains traceable.

---

# 📝 9. Solution Management

Universities/institutions can propose solutions for assigned problems.

A solution can contain:

- Solution title
- Description
- Benefits
- Estimated cost
- Required resources
- Estimated implementation time
- Supporting media
- Feedback

Example:

```text
Solution:
School Sanitation and Drinking Water Improvement

Description:
Construct additional toilets and install a safe
drinking water facility in the school.

Benefits:
Better student hygiene,
improved attendance,
safer drinking water.

Estimated Cost:
₹5,50,000

Resources:
Construction materials,
water purifier,
plumbing equipment,
workers.

Time:
10 weeks
```

---

# 🤝 10. Industry Partnership Module

The Industry Partnership workflow is implemented as **Milestone 8**.

Industry organizations can discover suitable projects and submit support offers.

Example:

```text
Industry:
Tech Solutions Pvt Ltd

Support:
Pipeline Repair Technical Support

Type:
TECHNICAL

Budget:
₹2,00,000

Duration:
3 months
```

The administrator can review the offer.

After acceptance:

```text
ACCEPTED
   ↓
ACTIVE PARTNERSHIP
   ↓
IMPLEMENTATION PROGRESS
   ↓
COMPLETED
```

---

# 📈 11. Implementation Progress

Industry partners can track implementation progress.

The industry interface provides:

```text
Implementation Progress

Add Progress Update

Mark Partnership Completed
```

This allows the platform to distinguish between:

- An offer being accepted
- A partnership being active
- Actual implementation activity
- A partnership being completed

---

# ✅ 12. Citizen Verification

After a solution is implemented, the citizen receives a verification step.

Example:

```text
Verify Implemented Solution

The solution has been implemented.
Confirm whether it solved the reported problem.

[ Verify Solution ]
```

After citizen verification:

```text
IMPLEMENTED
     ↓
Citizen verifies
     ↓
CLOSED
```

The platform records the verification event in the progress timeline.

Example:

```text
CLOSED

Citizen verified the implemented solution
and confirmed the impact.
```

This creates an important feedback loop:

```text
Problem
  ↓
Solution
  ↓
Implementation
  ↓
Citizen Verification
  ↓
Impact
```

---

# 📊 13. Impact & Analytics Dashboard

The platform includes an administrator **Impact & Analytics** dashboard.

It provides live platform-level indicators such as:

### Problem Metrics

- Total Problems
- Open Problems
- Resolved Problems
- Problems by category
- Problems by status
- Priority distribution

### Solution Metrics

- Total solutions
- Approved solutions
- Proposed solutions
- Verified solutions
- Rejected solutions

### Industry Metrics

- Industry partners
- Support offers
- Active partnerships
- Completed partnerships
- Support types

### Social Impact

- Problems with implemented solutions
- Verified solutions
- Reported people affected
- Rejected problems

---

# 📈 14. Example Analytics

A sample live dashboard can show:

```text
Total Problems          22
Open Problems           19
Resolved                 1
Solutions                8
Verified Solutions       1
People Affected       13,300
```

The system also breaks down categories such as:

```text
Water Resources
Electricity
Roads & Infrastructure
Public Safety
Sanitation
Healthcare
Education
Agriculture
Transport
Environment
```

and statuses such as:

```text
Submitted
Under Review
Assigned
In Progress
Solution Proposed
Pilot
Implemented
Closed
Rejected
```

The "people affected" metric is treated as a **reported impact indicator** supplied through citizen reports, rather than an independently verified population count.

---

# 🔔 15. Notifications

A centralized notification system is implemented.

Notifications can be used to inform users about important platform events such as:

- Problem assignment
- Status changes
- Solution activity
- Industry offers
- Offer acceptance
- Partnership activity
- Implementation progress
- Verification-related events

---

# 💬 16. Collaboration Comments

Problems include a collaboration/comment area.

Users can add comments to support communication around the challenge and its solution.

This provides a communication layer alongside structured workflow data.

---

# 🗂️ 17. Evidence & Media

Problems can contain supporting evidence/media.

This allows citizens to attach visual evidence to demonstrate the reported problem.

Example:

```text
Citizen Report
     +
Description
     +
Location
     +
GPS
     +
Affected People
     +
Evidence Image
```

This makes the problem record richer than a simple text complaint.

---

# 🗃️ 18. Database Structure

The platform uses a relational database with entities covering the major workflow components.

Important tables currently include:

```text
users
citizen_profiles
university_profiles
industry_profiles
government_profiles

states
districts
villages

problems
problem_media
problem_comments
problem_status_history
problem_assignments

solutions
solution_media
solution_feedback

implementation_updates

notifications

industry/project/offer related data
```

The `users` table supports multiple roles:

```text
CITIZEN
UNIVERSITY
INDUSTRY
GOVERNMENT
ADMIN
```

Account status supports:

```text
INCOMPLETE
PENDING
ACTIVE
SUSPENDED
```

University profiles contain fields such as:

```text
university_name
university_type
registration_number
department
designation
address
state
district
city
expertise
verification_status
```

This profile information is used by the institutional matching workflow.

---

# 🔐 19. Authentication & Authorization

The platform includes role-based authentication.

Different roles receive different application experiences:

```text
CITIZEN
   ↓
Citizen Dashboard

UNIVERSITY
   ↓
University Dashboard

INDUSTRY
   ↓
Industry Dashboard

ADMIN
   ↓
Admin Dashboard
```

Authentication endpoints are integrated with the frontend and backend.

The backend also protects role-specific operations.

---

# 🖥️ 20. Frontend

The application uses a modern React-based frontend.

Major UI areas implemented include:

```text
Authentication
Dashboard
Citizen Problems
Problem Details
University Dashboard
Assigned Problems
Projects
Teams
Industry Projects
Industry Support
Admin Dashboard
Admin Problems
AI Matching
Industry Offers
Impact & Analytics
Notifications
```

The UI is organized around the actual user role and workflow stage.

---

# ⚙️ 21. Backend API

The frontend communicates with a backend REST API.

Implemented API areas include routes for:

```text
/auth
/dashboard
/notifications

/admin
/admin/dashboard
/admin/users
/admin/problems
/admin/verifications
/admin/...

/representative/...

/industry/projects
/industry/support
/industry/admin/offers
/industry/projects/{id}/offers

/problems
/solutions
/assignments
/comments
/implementation
```

The exact endpoint list may evolve as additional milestones are integrated.

---

# 🔄 22. End-to-End Demonstrated Scenario

A complete workflow has been exercised using a school sanitation challenge.

### Step 1 — Citizen reports

```text
School sanitation facilities
```

with:

```text
Priority: HIGH
Affected people: 380
Location: Kasmar, Bokaro, Jharkhand
```

### Step 2 — Problem is processed

The problem moves through validation and solution workflow.

### Step 3 — Solution proposed

```text
School Sanitation and Drinking Water Improvement
```

### Step 4 — Solution implemented

The solution becomes:

```text
IMPLEMENTED
```

### Step 5 — Industry collaboration

An industry partner provides:

```text
Pipeline Repair Technical Support
₹2,00,000
3 months
```

### Step 6 — Partnership completion

The industry marks the partnership:

```text
COMPLETED
```

### Step 7 — Citizen verification

The citizen confirms that the implemented solution solved the problem.

### Step 8 — Final state

The challenge becomes:

```text
CLOSED
```

The timeline records the citizen verification event.

This demonstrates the intended:

```text
Challenge → Match → Project → Collaboration → Impact
```

workflow.

---

# 🧪 23. Test Data Used

The platform currently contains sample challenges covering multiple societal domains.

Examples include:

| Category | Example Challenge |
|---|---|
| Water Resources | Drinking water pipeline leakage |
| Water Resources | Irrigation water shortage |
| Electricity | Irregular electricity supply |
| Education | School sanitation facilities |
| Healthcare | Primary health centre shortage |
| Sanitation | Garbage collection problem |
| Public Safety | Lack of street lights |
| Roads & Infrastructure | Poor village road condition |
| Transport | Public transport shortage |
| Environment | Flood water drainage problem |
| Agriculture | Irrigation water shortage |

This diversified data is useful for demonstrating AI classification and representative matching.

---

# 🧠 24. Why Multiple Representatives Matter

Initially, only one university representative was available.

That caused every problem to be recommended to the same person.

To properly demonstrate institutional matching, multiple verified university representatives were added with different expertise.

Now:

```text
Water Problem
      ↓
Water/Civil/Environmental experts
      ↓
Higher match scores
```

while:

```text
Electricity Problem
      ↓
Electrical/Power experts
      ↓
Higher match scores
```

and:

```text
AI/Technology Problem
      ↓
AI/ML/Computer Science experts
      ↓
Higher match scores
```

This makes the recommendation engine visibly meaningful.

---

# 🎯 25. Current Milestone Coverage

Based on the functionality implemented so far, the platform currently covers these major capability areas:

| Capability | Status |
|---|---|
| Multi-role authentication | ✅ Implemented |
| Citizen problem reporting | ✅ Implemented |
| Location/GPS information | ✅ Implemented |
| Evidence/media | ✅ Implemented |
| Problem lifecycle | ✅ Implemented |
| Admin problem management | ✅ Implemented |
| University profiles | ✅ Implemented |
| University verification | ✅ Implemented |
| AI category prediction | ✅ Implemented |
| AI confidence | ✅ Implemented |
| Priority recommendation | ✅ Implemented |
| Keyword extraction | ✅ Implemented |
| Required expertise | ✅ Implemented |
| Explainable representative matching | ✅ Implemented |
| Multiple university representatives | ✅ Implemented |
| Industry representatives | ✅ Implemented |
| Solution proposals | ✅ Implemented |
| Solution feedback | ✅ Implemented |
| Industry support offers | ✅ Implemented |
| Admin offer approval | ✅ Implemented |
| Active partnerships | ✅ Implemented |
| Implementation progress | ✅ Implemented |
| Partnership completion | ✅ Implemented |
| Citizen verification | ✅ Implemented |
| Automatic problem closure after verification | ✅ Implemented |
| Notifications | ✅ Implemented |
| Collaboration comments | ✅ Implemented |
| Impact & analytics dashboard | ✅ Implemented |

---

# 🏗️ 26. High-Level Architecture

```text
                 ┌──────────────────────┐
                 │       React UI       │
                 │ Citizen / University │
                 │ Industry / Admin     │
                 └──────────┬───────────┘
                            │
                            │ REST API
                            ▼
                 ┌──────────────────────┐
                 │   Backend / API      │
                 │ Authentication       │
                 │ Business Logic       │
                 │ Matching             │
                 │ Workflow             │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       ┌──────────┐   ┌────────────┐  ┌──────────────┐
       │ Database │   │ AI/Matching│  │ Media/Cloud  │
       │ MySQL    │   │ Logic      │  │ Storage      │
       └──────────┘   └────────────┘  └──────────────┘
```

---

# 🔐 27. Data & Workflow Integrity

The system maintains structured records for:

- Users
- Profiles
- Problems
- Assignments
- Status history
- Solutions
- Feedback
- Industry offers
- Partnerships
- Implementation updates
- Notifications

This makes it possible to reconstruct the lifecycle of a challenge rather than storing only its latest status.

---

# 🧭 28. Example Complete Flow

```text
CITIZEN
   │
   │ Reports
   ▼
PROBLEM
   │
   │ AI analyzes
   ▼
CATEGORY + PRIORITY + KEYWORDS
   │
   │ Matching
   ▼
REPRESENTATIVE RANKING
   │
   │ Admin assigns
   ▼
UNIVERSITY / INSTITUTION
   │
   │ Proposes
   ▼
SOLUTION
   │
   │ Approved
   ▼
PROJECT / IMPLEMENTATION
   │
   │ Industry support
   ▼
INDUSTRY PARTNERSHIP
   │
   │ Progress updates
   ▼
IMPLEMENTED
   │
   │ Citizen verifies
   ▼
CLOSED
   │
   ▼
IMPACT ANALYTICS
```

---

# 📌 29. What the Current System Demonstrates

The implementation is no longer just a complaint-registration application.

It demonstrates a **closed-loop social innovation ecosystem**:

### 1. Identify

Citizens identify real local problems.

### 2. Understand

AI classifies the challenge and extracts relevant signals.

### 3. Match

The platform identifies institutions and representatives capable of helping.

### 4. Collaborate

Universities and industry partners participate in the solution.

### 5. Implement

Solutions and industry support are tracked through implementation.

### 6. Verify

The citizen confirms whether the solution actually helped.

### 7. Measure

The administrator can observe platform-level outcomes and reported social impact.

---

# ⚠️ 30. Important Notes

Some displayed values in the development environment are **sample/demo data** created to exercise the complete workflow.

For example:

- Sample citizens
- Sample universities
- Sample industry organizations
- Sample problem records
- Sample solution records
- Sample affected-people counts

Therefore, analytics should be interpreted according to the current database contents.

The reported "people affected" value represents what citizens entered into their reports and is not automatically proof of an independently verified population count.

---

# 🚀 31. Current Overall Status

## ✅ Core Platform Workflow: IMPLEMENTED

The current system successfully demonstrates:

```text
Citizen
   ↓
Problem
   ↓
AI Classification
   ↓
Institutional Matching
   ↓
Admin Assignment
   ↓
University Solution
   ↓
Industry Support
   ↓
Implementation
   ↓
Citizen Verification
   ↓
Problem Closure
   ↓
Impact Analytics
```

This is the main end-to-end functionality currently implemented in the SIH Portal.

---

# 🔮 32. Suggested Future Enhancements

The current implementation can be extended with additional advanced capabilities such as:

- Stronger ML/NLP classification models.
- Semantic/vector-based representative matching.
- Geographic distance-aware matching.
- More detailed government-department workflows.
- Automated duplicate-problem detection.
- Problem clustering by village/district.
- Real-time maps and geographic heatmaps.
- Advanced impact KPIs.
- Budget utilization tracking.
- Document verification.
- Mobile/PWA support.
- Audit logs and richer administrator controls.
- Automated reminders and escalation.
- Advanced analytics and exportable reports.
- Production-grade security hardening.
- Comprehensive automated test coverage.

These are **future enhancements**, not claims about already completed functionality.

---

# 🏁 33. Final Summary

The SIH Portal currently provides a structured path from a citizen's problem to a measurable outcome.

Instead of:

```text
Complaint → Status
```

the platform supports:

```text
Challenge
   ↓
AI Understanding
   ↓
Expert Matching
   ↓
Institutional Assignment
   ↓
Solution Development
   ↓
Industry Collaboration
   ↓
Implementation
   ↓
Citizen Verification
   ↓
Impact Measurement
```

The result is a platform designed to transform **local societal challenges into collaborative, trackable and verifiable solutions**.

---

## 🌟 Core Value Proposition

> **Report it. Understand it. Match it. Solve it. Implement it. Verify it. Measure the impact.**

---

## 📚 Technology Stack

The project is built as a full-stack web application using the project's configured technologies, including:

- **Frontend:** React
- **Backend:** Python/FastAPI-based REST APIs
- **Database:** MySQL
- **Authentication:** Role-based authentication with password and Google-login integration
- **Media:** Cloud-based media storage
- **AI:** Classification, keyword/expertise extraction and explainable matching logic
- **API Communication:** REST/JSON

Exact package versions and environment configuration should be taken from the project's dependency/configuration files rather than inferred from this overview.

---

## 👨‍💻 Development Status

**Current focus:** completing and validating the end-to-end SIH social innovation workflow.

**Implemented core:** Citizen → AI → Matching → Assignment → Solution → Industry Partnership → Implementation → Citizen Verification → Closure → Analytics.



# 🚀 11. How to Run the Project

This section is based on the **current project structure and configuration**.

## 11.1 Prerequisites

Install the following before running the project:

- **Python 3.11+**
- **Node.js + npm**
- **MySQL-compatible database** (the current `.env.example` is configured for Aiven MySQL)
- **Git**
- A Google OAuth client only if Google Login is enabled/used
- A Cloudinary account only if image/media upload is enabled/used

Check installations:

```powershell
python --version
node --version
npm --version
git --version
```

---

## 11.2 Clone the GitHub Repository

After pushing the project to GitHub, a team member can use:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SIH-Social-Innovation-Portal
```

> Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the actual GitHub repository URL.

The project currently has this important structure:

```text
SIH-Social-Innovation-Portal/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   └── routers/
│   ├── scripts/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── .env.example
│   └── package.json
│
├── README.md
└── .gitignore
```

---

# 12. Backend Setup

Open **Terminal 1 / PowerShell**:

```powershell
cd backend
```

## 12.1 Create a Python Virtual Environment

```powershell
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

If activation is blocked by PowerShell execution policy, use Command Prompt:

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of the terminal line.

---

## 12.2 Install Backend Dependencies

```powershell
pip install -r requirements.txt
```

The current project uses FastAPI, Uvicorn, SQLAlchemy, PyMySQL, Passlib/Bcrypt, JWT, Cloudinary, Google authentication and related packages.

---

## 12.3 Configure Backend Environment Variables

Copy:

```text
backend/.env.example
```

to:

```text
backend/.env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and replace the placeholder values with your real credentials.

The current project expects these variables:

```env
MYSQL_HOST=...
MYSQL_PORT=3306
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DB=...
MYSQL_SSL_MODE=REQUIRED

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

FRONTEND_ORIGINS=http://localhost:5173
```

### ⚠️ Important GitHub security rule

**Never commit `backend/.env` to GitHub.**

Commit:

```text
backend/.env.example
```

Do NOT commit:

```text
backend/.env
```

The `.env.example` file contains placeholders and is safe to use as a configuration template.

---

# 13. Database Setup

The backend uses SQLAlchemy and creates database tables during FastAPI startup:

```python
Base.metadata.create_all(bind=engine)
```

Therefore, the configured MySQL database must already exist and the credentials in `.env` must be correct.

For example, if using a local MySQL server:

```sql
CREATE DATABASE sih_portal;
```

Then configure the matching database name in `.env`.

If using the project's existing Aiven database, use the supplied Aiven host, username, password and SSL configuration instead.

---

## 13.1 Seed Basic Location Data

The project contains:

```text
backend/scripts/seed_locations.py
```

Run it from the `backend` directory:

```powershell
python -m scripts.seed_locations
```

This seeds:

- Indian states/UTs
- 24 Jharkhand districts

The script deliberately does **not** fabricate blocks/villages. Official LGD data can be imported using the provided LGD import tooling.

---

## 13.2 Create an Admin Account

The project includes:

```text
backend/scripts/create_admin.py
```

Run:

```powershell
python -m scripts.create_admin
```

You will be prompted for:

```text
Admin name
Admin email
Admin password
Confirm password
```

The password must contain at least 8 characters.

---

## 13.3 Industry Milestone Database Scripts

The repository contains:

```text
backend/scripts/m8_industry_migration.sql
backend/scripts/m8_industry_seed.sql
```

The current FastAPI startup also creates SQLAlchemy-defined tables automatically.

The industry seed SQL is **sample data** and contains placeholder IDs. Do not run it blindly against a different database. First confirm the real `user_id` and `problem_id`.

---

# 14. Start the Backend

From:

```text
backend/
```

run:

```powershell
uvicorn app.main:app --reload --port 8000
```

The API will normally be available at:

```text
http://localhost:8000
```

Swagger/OpenAPI documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

The root endpoint should return:

```text
SIH Social Innovation Portal API is running
```

Keep this terminal running.

---

# 15. Frontend Setup

Open **Terminal 2 / PowerShell**.

From the project root:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

The current frontend uses React + Vite and the dependencies defined in `package.json`.

---

## 15.1 Configure Frontend Environment

Copy:

```text
frontend/.env.example
```

to:

```text
frontend/.env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

The current frontend configuration is:

```env
VITE_API_URL=http://localhost:8000/api
VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
```

If Google Login is not being used in a particular local setup, follow the application's existing login flow.

Do not put a Google **client secret** in the frontend `.env`. Frontend Vite variables are exposed to the browser.

---

# 16. Start the Frontend

From:

```text
frontend/
```

run:

```powershell
npm run dev
```

Vite will normally start at:

```text
http://localhost:5173
```

Open that address in the browser.

---

# 17. Complete Local Startup — Quick Version

After the repository is cloned and environment variables are configured:

### Terminal 1 — Backend

```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

Backend API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 18. How to Verify the Full Platform

Use separate accounts/roles for the end-to-end demonstration.

```text
CITIZEN
   │
   │ Report Problem
   ▼
AI CLASSIFICATION
   │
   │ Category + Confidence + Priority + Keywords
   ▼
INSTITUTIONAL MATCHING
   │
   │ University / Industry representatives
   ▼
ADMIN
   │
   │ Review + Assign
   ▼
UNIVERSITY
   │
   │ Solution Proposal
   ▼
ADMIN / SOLUTION WORKFLOW
   │
   │ Approve → Implement
   ▼
INDUSTRY
   │
   │ Support Offer
   ▼
ADMIN
   │
   │ Accept Offer
   ▼
ACTIVE PARTNERSHIP
   │
   │ Progress Updates
   ▼
IMPLEMENTED
   │
   ▼
CITIZEN
   │
   │ Verify Result
   ▼
CLOSED
   │
   ▼
IMPACT & ANALYTICS
```

---

# 19. Recommended Demo Test

For a clean team demonstration:

### Step 1 — Citizen

Login as a citizen and create a challenge such as:

```text
Title:
Irrigation water shortage

Description:
Farmers are not getting enough water for irrigation,
causing crops to dry and reducing agricultural production.
```

Provide affected people, location and evidence where required.

---

### Step 2 — AI Analysis

Open the problem as Admin and run:

```text
Re-analyze
```

Verify:

- Predicted category
- Confidence
- Suggested priority
- Required expertise
- Matched keywords

Example:

```text
Water Resources
97% confidence
HIGH / CRITICAL priority
```

---

### Step 3 — Institutional Matching

Verify that suitable approved representatives are ranked.

For example, an irrigation/water problem should favor representatives with expertise such as:

```text
irrigation
water management
hydraulics
civil engineering
environmental engineering
```

The UI should show the explainable match reasons and percentage score.

---

### Step 4 — Admin Assignment

Select the recommended representative and assign the problem.

Then verify that the university representative can see the assigned challenge.

---

### Step 5 — University Solution

Login as the assigned University representative.

Create a solution containing:

- Title
- Description
- Benefits
- Estimated cost
- Resources
- Implementation time

Move the solution through the available workflow.

---

### Step 6 — Industry Collaboration

Login as Industry.

Open an eligible project and submit an industry support offer.

Example:

```text
Support type: TECHNICAL
Title: Pipeline Repair Technical Support
Amount: ₹2,00,000
Duration: 3 months
```

---

### Step 7 — Admin Approval

Login as Admin.

Open:

```text
Industry Partnerships
```

Review the offer and accept it.

Verify that an active partnership is created.

---

### Step 8 — Industry Implementation

Login as Industry.

Open:

```text
My Support
```

Verify:

```text
ACCEPTED
→ ACTIVE
→ Implementation Progress
→ COMPLETED
```

Add progress updates where appropriate.

---

### Step 9 — Citizen Verification

Login as the reporting Citizen.

Open the implemented problem.

Use:

```text
Verify Solution
```

Submit the verification/feedback.

A successfully verified implemented solution can move the problem to:

```text
CLOSED
```

---

### Step 10 — Impact Analytics

Login as Admin and open:

```text
Impact & Analytics
```

Verify the platform-level metrics, including:

- Total problems
- Open problems
- Resolved problems
- Solutions
- Verified solutions
- People affected
- Category distribution
- Status distribution
- Priority distribution
- Solution outcomes
- Industry engagement
- Industry support types
- Social impact indicators

---

# 20. Troubleshooting

## `ModuleNotFoundError`

Make sure the backend virtual environment is active:

```powershell
venv\Scripts\activate
```

Then:

```powershell
pip install -r requirements.txt
```

---

## Backend cannot connect to MySQL

Check:

```text
MYSQL_HOST
MYSQL_PORT
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
MYSQL_SSL_MODE
```

in:

```text
backend/.env
```

Also verify that the database server is reachable.

---

## Frontend cannot reach backend

Check that backend is running on:

```text
http://localhost:8000
```

and frontend `.env` contains:

```env
VITE_API_URL=http://localhost:8000/api
```

Restart Vite after changing `.env`.

---

## CORS error

Make sure backend `.env` contains:

```env
FRONTEND_ORIGINS=http://localhost:5173
```

Then restart the backend.

---

## `422 Unprocessable Entity`

A `422` response normally means the request reached FastAPI but the submitted data did not satisfy the endpoint's validation/schema.

Check:

1. Browser Network tab.
2. Request URL.
3. Request method.
4. Request payload.
5. Response body.

The response body usually tells which field is missing or invalid.

---

## Port 8000 already in use

Use another backend port:

```powershell
uvicorn app.main:app --reload --port 8001
```

Then update:

```env
VITE_API_URL=http://localhost:8001/api
```

and restart the frontend.

---

## Port 5173 already in use

Vite can choose another available port automatically, or you can specify one through the Vite configuration/command.

If the frontend moves to another port, update:

```env
FRONTEND_ORIGINS=http://localhost:<PORT>
```

in the backend configuration.

---

# 21. GitHub Preparation

Before pushing:

### Check for secrets

Make sure these are NOT committed:

```text
backend/.env
frontend/.env
```

Also do not commit:

```text
__pycache__/
*.pyc
venv/
node_modules/
dist/
```

### Keep these files

```text
backend/.env.example
frontend/.env.example
backend/requirements.txt
frontend/package.json
frontend/package-lock.json
README.md
```

---

# 22. Suggested Git Commands

From the project root:

```powershell
git init
git add .
git status
```

Review the files shown by `git status`.

If everything is safe:

```powershell
git commit -m "Initial SIH Social Innovation Portal implementation"
```

Connect your GitHub repository:

```powershell
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

Rename the branch:

```powershell
git branch -M main
```

Push:

```powershell
git push -u origin main
```

---

# 23. Important Before Sharing the Repository

The repository contains configuration templates, but **database credentials and third-party secrets must be supplied separately** by whoever runs the system.

A new developer should follow:

```text
Clone
  ↓
Install Python dependencies
  ↓
Create backend/.env
  ↓
Configure database / services
  ↓
Seed required data
  ↓
Start FastAPI
  ↓
Create frontend/.env
  ↓
npm install
  ↓
npm run dev
  ↓
Open localhost:5173
```

---

# 24. Current Implementation Status

The implemented platform currently demonstrates the core lifecycle:

```text
Citizen Challenge
       ↓
AI Classification
       ↓
Priority Prediction
       ↓
Explainable Institutional Matching
       ↓
Admin Assignment
       ↓
University Solution
       ↓
Industry Support Offer
       ↓
Admin Acceptance
       ↓
Industry Partnership
       ↓
Implementation Progress
       ↓
Citizen Verification
       ↓
Problem Closure
       ↓
Impact & Analytics
```

This makes the repository suitable for demonstrating the **end-to-end Social Innovation Collaboration Portal workflow**.

---

# 25. Future Enhancements

Potential future work includes:

- More advanced ML/NLP classification.
- Semantic/vector-based representative matching.
- Better duplicate-problem detection.
- Automated impact measurement.
- Richer project/team management.
- Government department integration.
- Real-time notifications.
- Advanced geographic analytics.
- Production deployment.
- Automated testing/CI/CD.
- More granular permissions and audit controls.

---

# 26. License

Add the team's selected license here before publishing publicly.

---

# 27. Contributors

Add the project team members here.
