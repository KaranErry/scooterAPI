# Personal Transport API (Bike Rentals – Sprint 1, Flask)

A lightweight REST API for a **Bike Rental** service.

**Sprint 1 goal:** rename, clean up, and ship a working MVP using **Flask** — fast, focused, and demo-ready.

> Why Flask first? Sprint 1 is about momentum, not perfection. We’ll migrate to FastAPI in a future sprint once the MVP is alive.

---

## Features (Sprint 1 scope)
- Basic **CRUD** for bikes and rentals (MVP endpoints)
- Clear repo workflow (Issues → Branches → PRs → Merge)
- Strict branch naming with CI guardrail
- Project board: **To Do → In Progress → Done** (manual column moves)

**Planned (Sprint 2+)**
- Migrate to **FastAPI** (auto-docs, async)
- AuthN/AuthZ
- Payments integration
- Inventory/availability logic
- Test suite + CI

---

## Tech Stack
- **Python** 3.10+
- **Flask** (Sprint 1)
- **JSON REST**
- **GitHub** Projects + Actions

---

## Getting Started (Intern-Friendly)

> If this is your first rodeo, follow these steps exactly — then break stuff *intentionally* once it runs. 😄

### 1) Clone
```bash
git clone https://github.com/MelEUsher/PersonalTransportAPI.git
cd PersonalTransportAPI

### 2) Create & activate a virtual environment
macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

### 3) Install dependencies
If requirements.txt exists:
pip install -r requirements.txt

### 4) Run the app (preferred)
python app.py

#### Alternative (flask run):
# macOS/Linux
export FLASK_APP=app.py
flask run --port 5000

# Windows (cmd)
set FLASK_APP=app.py
flask run --port 5000

# Windows (PowerShell)
$Env:FLASK_APP="app.py"
flask run --port 5000

Visit: http://localhost:5000

## Project Structure
PersonalTransportAPI/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  └─ config.yml
│  ├─ workflows/
│  │  └─ branch-name-check.yml
│  └─ pull_request_template.md
├─ src/                    # (recommended) app code moves here later
│  ├─ __init__.py
│  ├─ app.py               # or at repo root initially
│  └─ routes/              # per-feature blueprints
├─ tests/                  # placeholder for now
├─ requirements.txt
├─ CONTRIBUTING.md
└─ README.md

## Development Workflow (read this like a cheat sheet)
We keep it simple and professional.

### 1) Create an Issue
Every task starts as an Issue (use the Task template).
The Project board is your home base.
### 2) Create a branch from the Issue (strict naming)
feature/issue-<number>-short-name
bugfix/issue-<number>-short-name
chore/issue-<number>-short-name

#### Examples
feature/issue-12-rentals-endpoint
bugfix/issue-7-auth-timezone
chore/issue-3-rewrite-readme

####CLI
git checkout master
git pull
git checkout -b feature/issue-12-rentals-endpoint

### 3) Do the work, commit small, push
git add .
git commit -m "Issue #12: implement /rentals endpoints and basic validation"
git push -u origin feature/issue-12-rentals-endpoint

### 4) Open a PR (link the Issue)
In your PR description, add:
Closes #<issue-number>

GitHub auto-closes the Issue when the PR merges.

### 5) Get green checks, then submit PR.
`master` is protected: PR required, no direct pushes.

## Working With the Project Board
New Issues auto-add to the project (based on your workflow filter).
Move between To Do / In Progress / Done manually (expected in new GitHub Projects).
Status automation is optional; we’re keeping it manual for simplicity.

## Testing (Placeholder -- testing will be added later)
####Expected (when added):
pytest -q
# or
make test

## Contributing
See CONTRIBUTING.md for branch naming, Issue → Branch → PR flow, and checklist.

## License
If a LICENSE file is added, it will be referenced here.

## Project History (Background & Attribution)
This repository began as a fork of `KaranErry/scooterAPI`.
We are transforming it into a **Bike Rental API** with a modernized structure, clearer workflows, and a future migration to FastAPI.
Original project: https://github.com/KaranErry/scooterAPI
Current owner & direction: **Mel Usher** (MelEUsher/PersonalTransportAPI)
