# Project Submission: Smart Backlog Assistant

## 1. Problem Definition

### Problem Statement
Engineering teams often spend hours manually converting unstructured meeting transcripts, raw text notes, and PDF PRDs into formal Agile user stories. This manual grooming process leads to missing edge cases, inconsistent acceptance criteria formats, and delays in sprint planning. 

The **Smart Backlog Assistant** automates requirement grooming by ingesting unstructured documents (`.txt` and `.pdf`) and using AI to extract structured, schema-validated Agile backlogs containing stories, Gherkin acceptance criteria, Fibonacci estimates, priority levels, and risk assessments.

### Key Use Cases
1. **Post-Meeting Requirements Extraction:** A Product Manager uploads raw engineering meeting notes (`.txt` or `.pdf`) to instantly generate estimated user stories and risk flags before sprint grooming.
2. **Multi-User Backlog History:** Different engineers or PMs log into the shared dashboard, process independent feature documents, and reference historical backlog outputs stored in a centralized SQLite database.
3. **PRD & Edge Case Analysis:** A developer uploads a detailed PDF spec sheet; the system parses the text and identifies missing edge cases and technical security risks.

*Note on AI Assistance:* Google Gemini was used during the design phase to iterate on the Pydantic schema structure to ensure generated outputs matched standard software engineering criteria (Gherkin format, Fibonacci sizing).

---

## 2. Solution Design

### Architecture Diagram & Data Flow

```text
  [ User Interface (Streamlit) ]
                 │
                 │ 1. Uploads .txt/.pdf & Username
                 ▼
     [ FastAPI Backend Server ]
                 │
                 ├─► 2. Document Parser (pypdf / Text Loader)
                 │
                 ├─► 3. Pydantic Structured Output Request
                 │        │
                 │        ▼
                 │   [ Google Gemini API ] (gemini-3.6-flash)
                 │        │
                 │        ▼
                 ├─► 4. Structured Backlog JSON (User Stories, Risks, Criteria)
                 │
                 └─► 5. Persists to SQLite Database (backlog.db)
                 │
                 ▼
  [ Interactive Multi-User Dashboard ]