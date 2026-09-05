# 🚀 SamadhanSetu — SIH 2026

## ⚡ QUICK START — RUN THE PROJECT

> **Team members: Start here.** Follow these steps to run SamadhanSetu locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Allabakash-blip/SamadhanSetu.git
cd SamadhanSetu
```

### 2️⃣ Backend Setup — Terminal 1

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create/configure `backend/.env` using the environment variables required by the project.

Then start the backend:

```powershell
uvicorn app:app --reload --port 8000
```

Backend:
**http://localhost:8000**

API documentation:
**http://localhost:8000/docs**

### 3️⃣ Frontend Setup — Terminal 2

Open a **new terminal** from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:
**http://localhost:5173**

### 4️⃣ Open the Application

Open:

**http://localhost:5173**

Keep both the backend and frontend terminals running.

---

## 🔄 QUICK PROJECT FLOW

```text
Citizen Reports Problem
        ↓
AI Classification
        ↓
Institutional Matching
        ↓
Admin Assignment
        ↓
University Collaboration
        ↓
Solution Proposal
        ↓
Solution Approval
        ↓
Industry Support / Partnership
        ↓
Implementation
        ↓
Citizen Verification
        ↓
Problem Closed
        ↓
Impact & Analytics
```

---

## 👥 PLATFORM ROLES

| Role | Main Responsibility |
|---|---|
| 👤 Citizen | Report societal problems, track progress and verify implemented solutions |
| 🎓 University | Receive assigned challenges, collaborate and propose solutions |
| 🏭 Industry | Discover projects and provide practical support, funding, mentoring or technical assistance |
| 🛡️ Admin | Verify users, manage problems, assignments, solutions, partnerships and analytics |

---

## 🤖 AI & INTELLIGENCE

The platform includes AI-assisted:

- Problem category classification
- Confidence scoring
- Priority suggestion
- Required-expertise extraction
- Matched-keyword detection
- Transparent representative ranking
- Institutional matching using explainable signals

---

## 🤝 INDUSTRY COLLABORATION

Industry partners can:

- Discover eligible projects
- Submit support offers
- Specify support type, resources, cost and duration
- Receive admin approval
- Track active partnerships
- Add implementation progress
- Mark partnerships completed

---

## 📊 IMPACT & ANALYTICS

Admin analytics provide visibility into:

- Total and open problems
- Resolved problems
- Problems by category
- Problems by lifecycle status
- Priority distribution
- Solution outcomes
- Industry engagement
- Reported people affected
- Verified social impact

---

## 🔐 IMPORTANT SETUP NOTES

- Do **not** commit `.env` files or secrets.
- Do **not** commit `venv/` or `node_modules/`.
- Use the credentials/configuration provided by the project team for local services.
- If PowerShell blocks virtual-environment activation, run the backend using the Python environment configured on your machine or use Command Prompt.
- If the backend starts on a different port, make sure the frontend API configuration matches it.

---

# 🌍 SOCIAL INNOVATION COLLABORATION PORTAL

SamadhanSetu is a full-stack Social Innovation Collaboration Portal developed for **SIH 2026**.

The platform connects citizens, universities, industries and administrators to transform local societal challenges into collaborative, measurable solutions.

## 🎯 Core Platform Workflow

**Challenge → AI Match → Collaboration → Solution → Implementation → Impact**

---

## 📌 IMPLEMENTED FUNCTIONALITY

### Citizen

- Registration/login
- Citizen dashboard
- Report societal problems
- Add description, priority, affected people, address, pincode and GPS
- Upload problem evidence
- View submitted problems
- Track lifecycle status
- View assignments
- View solution proposals
- Provide solution feedback
- Verify implemented solutions
- Add collaboration comments
- Receive notifications

### University / Institutional Representative

- University account/login
- View assigned citizen challenges
- Review challenge details
- Work with assigned problems
- Participate in solution workflow
- Submit/manage solution proposals
- Track project progress
- Participate in multidisciplinary collaboration

### Industry

- Industry account/login
- Browse eligible projects
- View project details
- Submit support offers
- Define support type
- Provide offer description/resources
- Specify estimated cost and duration
- View offer status
- Track accepted partnerships
- Add implementation progress
- Complete partnerships

### Admin

- Admin dashboard
- User management
- Organization/user verification
- Problem management
- Problem status and priority management
- AI classification and institutional matching
- Representative recommendations
- Representative assignment
- Solution management
- Industry support-offer review
- Partnership management
- Notifications
- Impact and analytics dashboard

---

## 🧠 AI MATCHING — EXPLAINABLE APPROACH

The matching screen provides transparent signals rather than only returning a black-box recommendation.

It can show:

- Predicted category
- Classification confidence
- Suggested priority
- Required expertise
- Matched keywords
- Expertise overlap
- Institutional availability
- Geographic/state relevance where applicable
- Ranked representatives

Example:

```text
Problem
   ↓
AI Category
   ↓
Required Expertise
   ↓
Keyword Matching
   ↓
Representative Expertise
   ↓
Explainable Match Score
   ↓
Ranked Recommendations
```

---

## 🔄 PROBLEM LIFECYCLE

Typical lifecycle:

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

A problem may also be **REJECTED** where appropriate.

---

## 🏆 SOLUTION & IMPACT WORKFLOW

```text
Problem
   ↓
Institutional Assignment
   ↓
Solution Proposal
   ↓
Solution Approval
   ↓
Industry Collaboration
   ↓
Implementation
   ↓
Citizen Verification
   ↓
Verified Outcome
   ↓
Closed Problem
   ↓
Analytics / Social Impact
```

---

## 🛠️ TECHNOLOGY STACK

### Frontend

- React
- JavaScript
- CSS
- Vite

### Backend

- Python
- FastAPI
- REST APIs
- Authentication and authorization

### Data & Services

- Relational database
- Environment-based configuration
- Cloud/media services where configured

---

## 📁 PROJECT STRUCTURE

```text
SamadhanSetu/
│
├── backend/
│   ├── application/backend source files
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
│
├── .gitignore
└── README.md
```

> Local `.env`, virtual environments and generated frontend dependencies should remain untracked.

---

## 🧪 BASIC VERIFICATION

After starting both services:

1. Open **http://localhost:5173**
2. Login with a valid test account.
3. Test the appropriate role dashboard.
4. For API-level verification, open **http://localhost:8000/docs**
5. Verify that frontend requests reach the backend successfully.

---

## 📚 TEAM WORKING RULE

Before changing the code:

1. Pull the latest `main` branch.
2. Create a feature branch for your work.
3. Make and test your changes.
4. Commit with a meaningful message.
5. Push the branch.
6. Create a Pull Request for team review.

Example:

```bash
git pull origin main
git checkout -b feature/your-feature
```

---

## 🚀 PROJECT STATUS

SamadhanSetu currently implements the core end-to-end social innovation workflow:

**Citizen Challenge → AI Classification → Institutional Matching → Assignment → Solution → Industry Partnership → Implementation → Citizen Verification → Impact Analytics**

