# Smart Backlog Assistant

An AI-powered developer tool that ingests unstructured engineering meeting notes or product requirement documents (PRDs) and automatically translates them into structured, high-quality Agile user stories with Gherkin acceptance criteria.

---

## Features

* **Automated Requirement Grooming:** Slices raw text into fully realized user stories following standard Agile formats (`As a... I want to... So that...`).
* **Strict Type Validation:** Uses Pydantic schemas combined with Google Gemini's structured outputs to guarantee 100% reliable JSON formatting.
* **Risk Identification:** Automatically flags potential technical hurdles, edge cases, and architectural security concerns.
* **Docker Containerized:** Fully isolated execution environment ensuring it runs smoothly across any operating system.

---

## Project Directory Structure

```text
smart-backlog-assistant/
│
├── Dockerfile
├── README.md
├── requirements.txt
├── main.py
│
├── config/
│   └── settings.py
│
├── inputs/
│   └── meeting_notes_auth.txt
│
├── outputs/
│   └── result.json (Generated upon execution)
│
└── src/
    ├── __init__.py
    ├── ai_client.py
    ├── parser.py
    └── validator.py

```

##  Prerequisites
* Docker installed and running on your machine.
* A free Google Gemini API Key.

#### Setup & Execution Guide
1. Navigate to the Project Root
Ensure you are inside the folder containing your Dockerfile and main.py:


```Bash
cd smart-backlog-assistant
```
2. Build the Docker Image
Build the local container image (this will automatically pull python:3.11-slim and install all required dependencies):

```Bash
docker build -t smart-backlog-assistant .
```
3. Run the Tool
Execute the container by passing your Google Gemini API key as an environment variable and volume-mapping your local input/output directories:

```Bash
docker run --rm -it \
  -e GEMINI_API_KEY="your_actual_gemini_api_key_here" \
  -v "$(pwd)/inputs:/app/inputs" \
  -v "$(pwd)/outputs:/app/outputs" \
  smart-backlog-assistant --input inputs/meeting_notes_auth.txt --output outputs/result.json
  ```
###  Example Usage with Custom Inputs
To process your own requirements document or meeting transcript:

Save your text or markdown file inside the local inputs/ folder (e.g., inputs/my_feature_notes.txt).

Run the container pointing to your custom file:

```Bash
docker run --rm -it \
  -e GEMINI_API_KEY="your_actual_gemini_api_key_here" \
  -v "$(pwd)/inputs:/app/inputs" \
  -v "$(pwd)/outputs:/app/outputs" \
  smart-backlog-assistant --input inputs/my_feature_notes.txt --output outputs/my_backlog.json
  ```
### Inspect your generated backlog inside the outputs/ directory.