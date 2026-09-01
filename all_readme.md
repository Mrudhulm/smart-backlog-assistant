# Smart Backlog Agent

This folder contains a custom agent for the Smart Backlog Assistant project.

## What this project does

This app reads meeting notes or PRD text and turns it into:
- structured backlog JSON
- an HTML dashboard report
- Agile user stories using Gemini

## Folder and file structure

```text
ai-agent/
├── .agent.md                  # Custom Copilot agent instructions for this project
├── README.md                  # Simple project overview
├── summary.md                 # Short summary of the project and goal
├── workflow.md                # Step-by-step workflow of the app
├── all_readme.md              # Main documentation for the project setup
├── troubleshooting.md         # Common problems and fixes
└──

smart-backlog-assistant/
├── Dockerfile                 # Builds the Docker container for the app
├── main.py                    # Entry point for running the CLI app
├── requirements.txt           # Python libraries required by the app
├── README.md                  # Project instructions and usage notes
├── .env.example               # Example environment variables
├── .gitignore                 # Ignores local or generated files
├── config/                    # App configuration files
│   └── ...                    # Settings and config helpers
├── inputs/                    # Place meeting notes or PRDs here
│   └── ...                    # Example input files
├── outputs/                   # Result files are created here
│   └── ...                    # JSON backlog output and HTML dashboard
├── src/                       # Application source code
│   ├── ai_client.py           # Gemini API client logic
│   ├── parser.py              # Reads input files and saves outputs
│   └── ...                    # Other support modules
├── tests/                     # Test scripts or validation files
│   └── ...                    # Automated checks
├── web/                       # Web UI or supporting frontend files
│   └── ...                    # Dashboard or web assets
└── local-installed-software-from-chat.txt
```

## Purpose of each main folder

- `config/` - stores configuration and environment-related settings
- `inputs/` - folder where the meeting notes or PRD input file goes
- `outputs/` - folder where generated result files are saved
- `src/` - main logic of the app: parsing, AI calls, and processing
- `tests/` - app validation and testing files
- `web/` - web-related assets or dashboard frontend support

## Purpose of each main file

- `main.py` - starts the CLI app and processes the input file
- `Dockerfile` - builds the app container
- `requirements.txt` - Python packages to install
- `README.md` - explains setup and how to run the tool
- `.env.example` - sample environment file for API keys
- `.gitignore` - avoids committing local temp or secret files

## How to run

From the project folder:

```bash
cd /Users/mrudhul/Documents/github/acn-ai/gemini-simple/smart-backlog-assistant
```

Build the Docker image:

```bash
docker build -t smart-backlog-gemini-assistant .
```

Run the app:

```bash
docker run --rm -it \
  -e GEMINI_API_KEY="YOUR_KEY" \
  -v "$(pwd)/inputs:/app/inputs" \
  -v "$(pwd)/outputs:/app/outputs" \
  smart-backlog-gemini-assistant \
    --input inputs/meeting_notes_auth.txt \
    --output-json outputs/result.json \
    --output-html outputs/dashboard.html
```

## What the output is

This app produces:
- `outputs/result.json` - structured backlog data
- `outputs/dashboard.html` - HTML dashboard view of the backlog

These are the main result files after the app runs successfully.

## Example prompts for the agent

- Fix the Docker build for this meeting-notes app
- Why is the app not reading my input file?
- Help me run the backlog generator on a meeting notes file
- What output files should I expect after the run?
- Why is the HTML dashboard not generating?

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common errors and fixes.
