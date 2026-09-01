# Smart Backlog Assistant (Gemini Edition)

AI-powered tool that converts unstructured meeting notes or PRDs into structured Agile user stories using Google Gemini.

## Summary

This project is a custom AI agent for the Smart Backlog Assistant. It helps with:
- reading meeting notes and PRDs
- fixing Docker build issues
- debugging the Python app
- checking input/output folders
- creating backlog JSON and HTML dashboard output

The goal is to keep the agent focused only on this project workflow.

## What it does

This agent helps with:
- Docker setup and fixes
- Python app debugging
- running assistant tools locally
- fixing input/output folder issues
- simple project startup and script cleanup

## Typical use

Use this agent when you want help with a local smart backlog, AI assistant, or dashboard project.

Example prompts:
- Fix this Docker build
- Why is the app not reading my files?
- Help me run this project locally
- Create a simple command to start this app

## Files

- `.agent.md` - the custom agent definition
- `README.md` - quick project overview
- `workflow.md` - step-by-step local workflow
- `troubleshooting.md` - common issues and fixes

## Local setup and Docker workflow

1. Navigate to the project root:
   ```bash
   cd ~/smart-backlog-assistant
   ```

2. Create or update your environment file if needed:
   ```bash
   cp .env.example .env
   ```

3. Build the Docker image:
   ```bash
   docker build -t smart-backlog-gemini-assistant .
   ```

4. Run the app:
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

## Troubleshooting

### Docker build fails

Check:
- the Dockerfile exists in the project root
- the project path is correct
- the Python version is supported
- dependencies in `requirements.txt` are valid

### Input file not found

Make sure the file exists in the `inputs` folder and the command uses the correct path:
```bash
--input inputs/meeting_notes_auth.txt
```

### Output files not created

Check that the `outputs` folder exists and the command includes both output flags:
```bash
--output-json outputs/result.json
--output-html outputs/dashboard.html
```

### Missing API key

Set the environment variable before running the container:
```bash
-e GEMINI_API_KEY="YOUR_KEY"
```

## Workflow

1. Read the input file.
2. Check the app command and Docker run steps.
3. Verify the input path and output folders.
4. Fix the small issue in the app or config.
5. Run the command again.
6. Check if the JSON and HTML outputs were created.

This workflow is focused on the Smart Backlog Assistant meeting-note process.
