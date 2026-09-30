# GovPilot: Innovation Procurement & Pilot Management Platform

> **Smart India Hackathon (SIH 2026)**
> **Problem Track:** Next-Generation Public Procurement & Innovation Lifecycle Management
> **Target Audience:** Government Departments, DPIIT-Recognized Startups, Technical Evaluators, Independent Auditors

---

## 🏛️ Executive Summary

Public sector organizations face critical operational and urban challenges that high-potential startups can solve. However, traditional government procurement systems (such as GeM and CPPP) are designed for standardized commodities and established vendors with long track records, high turnover requirements, and strict Earnest Money Deposit (EMD) criteria. This creates a high barrier to entry for early-stage and deep-tech startups.

**GovPilot** serves as an agile, compliance-aligned **Innovation Pre-Qualification and Pilot Sandbox Layer**. It transitions government departments through an 8-stage lifecycle:
1. **Unstructured Problem** -> Formulate as measurable challenge
2. **Outcome-Based Challenge** -> Define clear KPI targets
3. **Startup Discovery** -> Semantic matching based on capabilities & TRL
4. **Eligibility & Screening** -> Automated DPIIT, TRL, and compliance checks
5. **Expert Evaluation** -> 6-criteria weighted scoring with Conflict-of-Interest declarations
6. **Controlled Sandbox Pilot** -> 60-to-90 day deployment with milestone telemetry
7. **Independent Validation** -> Third-party technical audit and telemetry verification
8. **Scale-Up Procurement Pack** -> Automated, tamper-evident audit dossier & technical specifications for formal procurement (GFR Rule 149 / Innovation Clauses)

---

## 🔄 End-to-End System Workflow

```
[ Government Department ]
           │
           ▼
1. Problem Definition & AI-Assisted Challenge Formulation
           │
           ▼
2. Public Outcome Challenge (Budget, Duration, Target KPIs)
           │
           ├───────────────────────────────┐
           ▼                               ▼
3. Startup Discovery & Matching    Startup Application
   (TRL, Tech Stack, Certs)       (Technical Proposal & Milestones)
           │                               │
           └──────────────┬────────────────┘
                          ▼
4. Automated Eligibility & DPIIT Verification
                          │
                          ▼
5. Multi-Criteria Expert Evaluation & Scoring
                          │
                          ▼
6. Pilot Award & 10-Tab Pilot Sandbox Passport
   (Telemetry Tracking, Milestones, Payments, Risk Matrix)
                          │
                          ▼
7. Third-Party Technical Validation (NTAC Audit Sign-Off)
                          │
                          ▼
8. Formal Scale-Up Decision & Scale-Up Pack (PDF Generation)
                          │
                          ▼
[ Transition to Statutory Procurement Portals (GeM / CPPP) ]
```

---

## 👥 Role-Based Modules & Stakeholder Matrix

GovPilot provides purpose-built interfaces tailored to each stakeholder in the procurement lifecycle:

| Stakeholder Role | Primary Responsibilities | Core Platform Features |
| :--- | :--- | :--- |
| **Government Officer** | Challenge formulation, sandbox governance, milestone review, scale-up approval | 8-Step Outcome Builder, Semantic Discovery, Application Matrix, Scale-Up Pack Generation |
| **Startup Founder** | Proposal submission, milestone execution, KPI evidence uploads, sandbox telemetry | Innovation Passport, Deployment Registry, Milestone Deliverables, Real-time Status Tracking |
| **Expert Evaluator** | Technical review, weighted criteria scoring, methodology audit | Conflict of Interest (CoI) Declaration, Split-Screen Proposal Evaluator, Comparative Matrix |
| **Independent Validator** | On-site/telemetry technical audit, baseline verification, formal sign-off | Audit Dossier Review, Telemetry Verification Worksheet, Scale-Up Recommendation Engine |
| **Platform Administrator** | Department onboarding, user governance, audit compliance, system logs | Department Registry, Role-Based Access Control, Tamper-Evident Immutable Audit Log |

---

## 🌟 Hero Demo Scenario: Smart Transit Wait-Time Reduction

The platform includes a pre-seeded, end-to-end pilot case ready for demonstration and evaluation:

* **Department:** Urban Transport Authority (CITO: Rajesh Verma)
* **Challenge ID:** `CH-TRANS-2026-001` (Real-time Fleet Telemetry & Commuter ETA Optimization)
* **Startup:** TransitAI Labs (DPIIT-Recognized, TRL 8, AIS-140 & ISO 27001 Certified)
* **Pilot Passport:** `GP-MH-2026-00421` (10 Buses, 5 High-Density Routes, 90-Day Sandbox)
* **Measured Outcome:**
  * Baseline Wait Time: **16.4 minutes**
  * Target Wait Time: **11.0 minutes**
  * Achieved Pilot Metric: **10.8 minutes (-34.1% reduction)**
  * Commuter ETA Accuracy: **94.2%** (Target: >90%)
  * System Uptime: **99.9%** (Target: >99.5%)
* **Independent Audit:** Verified by National Technical Audit Cell (Lead Auditor: Vikram Deshmukh) -> Status: **Recommended for Pan-City Scale-Up (250 Buses)**
* **Procurement Artifact:** Scale-Up Pack with customized technical specifications, milestone benchmarks, and financial projections.

---

## 🛠️ Technology Stack & Architecture

### Backend Architecture
* **Framework:** Python 3.10+ / Flask (Application Factory & Blueprint Architecture)
* **Database ORM:** SQLAlchemy with SQLite / PostgreSQL compatibility
* **Authentication:** Flask-Login with role-based session isolation and secure password hashing (Werkzeug)
* **Document Engine:** ReportLab for dynamic, auditable PDF Scale-Up Pack generation
* **AI & Heuristic Engine:** Rule-based matching engine + contextual NLP challenge generator (LLM-ready with OpenAI/Gemini plug-ins)

### Frontend Architecture
* **Structure:** Semantic HTML5 templates powered by Jinja2
* **Styling:** Custom Enterprise Design System (Navy, Slate, Gold tokens, responsive grids, strict enterprise accessibility)
* **Visualization:** Lightweight HTML5 Canvas-based telemetry and KPI charting engine
* **Modals & Workflows:** Native vanilla JavaScript controllers for multi-step wizards and split-screen evaluations

### Data Models & Schemas
* **Users & Roles:** Hierarchical role definitions with departmental mappings
* **Innovation Passports:** Startup capabilities, TRL, IP declarations, certifications, past deployments
* **Challenges & Applications:** Multi-criteria eligibility schemas, budget allocations, milestone definitions
* **Pilot Passports:** Comprehensive 10-tab state machines tracking telemetry, milestones, disbursements, risks, and documents
* **Audit Registry:** Tamper-evident, timestamped event logging for every state transition and score submission

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Siddharth-CE/SIH2026.git
cd SIH2026
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Application Server
```bash
python app.py
```

### 5. Access the Platform
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Pre-Configured Demo Credentials

The platform auto-seeds with realistic demo data on initialization. You can log in using the credentials below or use the 1-Click Sandbox Switcher on the login screen:

| Role | Email | Password | Persona |
| :--- | :--- | :--- | :--- |
| **Government Officer** | `government@govpilot.demo` | `Password123` | Rajesh Verma (Urban Transport Authority) |
| **Startup Founder** | `startup@innovate.demo` | `Password123` | Aarav Patel (TransitAI Labs) |
| **Expert Evaluator** | `expert@review.demo` | `Password123` | Dr. Sunita Mehra (Transport Systems Evaluator) |
| **Validator / Auditor** | `validator@audit.demo` | `Password123` | Vikram Deshmukh (National Technical Audit Cell) |
| **Platform Administrator** | `admin@govpilot.demo` | `Password123` | Sanjay Kulkarni (System Administrator) |

---

## 📁 Repository Structure

```
SIH2026/
├── app.py                      # Application factory, blueprint registration & server entry
├── config.py                   # Configuration parameters and environment settings
├── requirements.txt            # Python dependencies
├── test_app.py                 # Automated unit and integration test suite
├── README.md                   # System documentation
│
├── models/                     # SQLAlchemy Models
│   ├── __init__.py             # Database initialization and exports
│   ├── user.py                 # User authentication and role management
│   ├── department.py           # Government departments and sectors
│   ├── startup.py              # Startup Innovation Passport and credentials
│   ├── challenge.py            # Outcome-based challenge blueprints
│   ├── application.py          # Startup proposals and screening records
│   ├── evaluation.py           # 6-criteria weighted scoring and CoI declarations
│   ├── pilot.py                # 10-tab Pilot Passport model
│   ├── kpi.py                  # KPI telemetry and observation data
│   ├── milestone.py            # Milestone deliverable tracking
│   ├── payment.py              # Payment and fund disbursement records
│   ├── risk.py                 # Pilot risk register and mitigations
│   ├── document.py             # Tamper-evident document registry
│   ├── validation.py           # Third-party technical validation dossiers
│   ├── scale_decision.py       # Formal scale-up procurement decisions
│   ├── audit.py                # Immutable audit log entries
│   └── notification.py         # In-app notifications
│
├── routes/                     # Modular Route Blueprints
│   ├── __init__.py             # Blueprint exports
│   ├── auth_routes.py          # Authentication and session switcher
│   ├── main_routes.py          # Public portal, guided tour, and knowledge library
│   ├── dashboard_routes.py     # Role-specific command centers
│   ├── challenge_routes.py     # 8-step challenge builder and public catalog
│   ├── startup_routes.py       # Startup directory and profile management
│   ├── application_routes.py   # Application submission and comparison matrix
│   ├── evaluation_routes.py    # Split-screen evaluation worksheet
│   ├── pilot_routes.py         # Pilot Passport management and milestone review
│   ├── validation_routes.py    # Independent validator audit forms
│   ├── scale_routes.py         # Scale decisions and PDF pack generation
│   ├── admin_routes.py         # Admin governance and audit log viewer
│   └── api_routes.py           # REST APIs for dynamic telemetry charts
│
├── services/                   # Core Business Logic & Services
│   ├── __init__.py             # Service exports
│   ├── seed_data.py            # Auto-seeder for demo walkthroughs
│   ├── ai_service.py           # AI Challenge Assistant (Heuristic + LLM connector)
│   ├── matching_service.py     # Semantic startup discovery and scoring
│   ├── pdf_service.py          # ReportLab official Scale-Up Pack PDF generator
│   └── audit_service.py        # Centralized tamper-evident audit logger
│
├── static/                     # Static Assets
│   ├── css/
│   │   └── main.css            # Enterprise styling and layout system
│   └── js/
│       ├── main.js             # UI interactions and alerts
│       ├── charts.js           # HTML5 Canvas chart renderer
│       └── wizard.js           # Multi-step challenge wizard controller
│
├── templates/                  # Jinja2 HTML5 Templates
│   ├── base.html               # Master shell layout with dynamic role sidebar
│   ├── landing.html            # Public landing page with workflow track
│   ├── login.html              # Authentication portal with 1-click login
│   ├── search_results.html     # Unified search results view
│   ├── dashboards/             # Five role-specific dashboard views
│   ├── challenges/             # Challenge builder, list, and detail views
│   ├── startups/               # Startup directory and passport views
│   ├── applications/           # Application wizard, detail, and matrix views
│   ├── evaluations/            # Evaluation worksheets and scoring tools
│   ├── pilots/                 # 10-tab Pilot Passport views
│   ├── validation/             # Technical audit and validation reporting
│   ├── scale/                  # Scale-up decision and PDF preview views
│   ├── knowledge/              # Procurement knowledge library
│   └── admin/                  # System governance and audit register
│
└── uploads/                    # Secure local storage for pilot evidence and files
```

---

## 🔒 Security, Integrity & Compliance

1. **Role-Based Access Control (RBAC):** Strict view and endpoint decorators ensure users can only access actions aligned with their verified role.
2. **Conflict of Interest (CoI) Enforcement:** Evaluators are barred from reviewing proposals without signing a binding digital CoI disclaimer.
3. **Immutable Audit Trail:** All critical state changes (milestone approvals, score submissions, validation decisions) are permanently logged with timestamps and user IDs.
4. **Statutory Alignment:** Designed to integrate with General Financial Rules (GFR) Rule 149 and Public Procurement Innovation Guidelines, ensuring sandbox results form a legally defensible foundation for subsequent scaling tenders.

---

## 🏆 SIH 2026 Evaluation Highlights

* **End-to-End Operational Completeness:** Every phase from challenge formulation to PDF scale-up generation is fully implemented and interactive.
* **Deterministic & Reproducible:** Auto-seeding guarantees instant, zero-friction demonstration for judges without manual setup.
* **Modular Code Quality:** Strict separation of concerns across SQLAlchemy models, Flask blueprints, and decoupled business logic services.
* **Production-Ready Deliverable:** Includes complete automated test suite (`test_app.py`) validating routes, models, and security access controls.

---

*Submitted for Smart India Hackathon (SIH 2026).*
