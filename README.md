# Academia - Industry Collaboration Portal for Skill Mapping, Internships & Placement
**Project Code:** Topic #55 (PB-55)

A comprehensive, full-stack web application bridging academic institutions, students, and corporate industry recruiters. Designed for technical skill mapping, real-time diagnostic skill gap analysis with radar charts, internship and campus placement lifecycle management, and institutional collaboration (curriculum co-design and MoUs).

---

## 🚀 Key Modules & Capabilities

### 1. Multi-Role User Ecosystem
- **Student**:
  - Profile with academic credentials (CGPA, degree stream, roll number, resume, portfolio/GitHub).
  - Multi-level skill self-rating (Levels 1 to 5) with certificate upload and faculty verification status.
  - Interactive **Skill Gap Analyzer** with radar chart benchmark against job descriptions.
  - One-click internship and placement drive application tracking.
- **Industry Recruiter**:
  - Post summer internships, semester internships, and full-time campus placement drives.
  - Set mandatory skill requirements with minimum expected proficiency levels.
  - Automated candidate ranking based on skill match compatibility percentage.
  - Manage application pipeline: Shortlist, schedule video interviews (Google Meet / Zoom), extend offers, and record feedback.
  - Submit curriculum advisory feedback to academic departments.
- **Faculty / Training & Placement Officer (TPO)**:
  - Institutional dashboard with placement percentages and active drive statistics.
  - Approve or decline recruiter job postings before publishing.
  - Verify student certifications and skill claims.
  - Review industry curriculum feedback for Board of Studies (BoS) syllabus revisions.
  - NAAC (Criteria 3 & 5) and NBA (Criterion 10) accreditation analytics & exportable reports.

### 2. Intelligent Skill Mapping & Gap Analysis Engine
- Pre-populated taxonomy across Programming, Web Engineering, Cloud & DevOps, AI/ML & Data Science, and Soft Skills.
- Compatibility Algorithm:
  $$\text{Match Score (\%)} = \min\left(100, \frac{\sum \min(\text{Student Level}, \text{Required Level})}{\sum \text{Required Level}} \times 100\right)$$
- **Chart.js Radar Visualization**: Visual overlay comparing the candidate's verified skill curve against the recruiter's benchmark.
- Automated generation of recommended learning action plans for identified skill deficits.

### 3. Industry-Academia Collaboration & Governance
- **Joint Capstone & R&D Challenges**: Corporate-sponsored student projects and funding grants.
- **Curriculum Co-Design**: Recruiter feedback on outdated course syllabi with faculty review workflows.
- **Institutional MoUs Tracker**: Records formal corporate agreements, validity periods, and collaborative scopes for accreditation audits.

---

## ⚡ Quick Start

### 1. Run the Application
```bash
./run.sh
```
*Or via standard Django command:*
```bash
python3 manage.py runserver
```
Then visit **http://127.0.0.1:8000** in your browser.

---

## 🔑 Pre-Seeded Demo Credentials

The portal comes pre-loaded with sample accounts and 1-click login buttons on the homepage/login page:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Student (Full-Stack)** | `student_rohan` | `student123` | High match for Web & Django roles |
| **Student (Cloud/DevOps)** | `student_priya` | `student123` | AWS Certified, Docker & K8s expert |
| **Corporate Recruiter** | `google_recruiter` | `pass123` | Google Cloud Campus Talent Partner |
| **Corporate Recruiter** | `microsoft_recruiter` | `pass123` | Microsoft IDC University Relations |
| **TPO Head / Faculty** | `prof_sharma` | `tpo123` | Dr. Rajiv Sharma (Training & Placement Cell) |
| **Portal Administrator** | `admin` | `admin123` | Full Django Admin & Institutional control |

---

## 🛠️ Technology Stack
- **Backend Framework**: Django 6.1 (Python 3)
- **Database**: SQLite3 (Zero setup required)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons, Plus Jakarta Sans typography
- **Data Visualization**: Chart.js (Radar charts, Bar charts)
- **Architecture**: Modular Django apps (`core`, `skills`, `internships`, `collaboration`)

---

## 📁 Project Structure
```
ca33/
├── manage.py
├── run.sh
├── portal_project/       # Project configuration & root routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Auth, UserProfile, Role-based Dashboards, Analytics
├── skills/               # Skill taxonomy, Student skills, Gap Analysis engine
├── internships/          # Opportunities, Drives, Applications & Pipeline
├── collaboration/        # Joint R&D, Curriculum feedback, MoUs
└── templates/            # Clean, responsive HTML5 templates
```
