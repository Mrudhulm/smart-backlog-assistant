# Smart Backlog Assistant Workflow

## Summary

This project is a focused local AI assistant for generating Agile backlog artifacts from meeting notes and PRDs. It helps with Docker setup, Python app debugging, validating inputs and outputs, and producing JSON and HTML backlog reports.

## What it does

- reads meeting notes or PRD text
- turns raw notes into structured backlog JSON
- creates an HTML dashboard report
- supports local debugging of Docker and Python startup issues
- helps verify correct input/output paths and environment config

## Local setup and Docker workflow

1. Navigate to the project root:
   ```bash
   cd /Users/mrudhul/Documents/github/acn-ai/smart-backlog-assistant
   ```

2. Create or update your environment file if needed:
   ```bash
   cp .env.example .env
   ```

3. Build the app container:
   ```bash
   docker build -t smart-backlog-gemini-assistant .
   ```

4. Run the app with the required input and output paths:
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

5. If you are running the web dashboard image instead:
   ```bash
   docker run --rm -it --env-file .env -p 5002:5000 \
     -v "$(pwd)/inputs:/app/inputs" \
     -v "$(pwd)/outputs:/app/outputs" \
     smart-backlog-web
   ```

## Troubleshooting

### Docker build fails

Check:
- the Dockerfile exists in the project root
- the project path is correct
- the Python version is supported
- dependencies in `requirements.txt` are valid

Try:
```bash
docker build --no-cache -t smart-backlog-web -f web/Dockerfile .
docker build -t smart-backlog-gemini-assistant .
```

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

### App starts but fails during processing

Check:
- input file format
- file permissions
- whether the output path is writable
- whether Gemini access is working

## Workflow

1. Read the input file.
2. Check the app command and Docker run steps.
3. Verify the input path and output folders.
4. Fix the small issue in the app or config.
5. Run the command again.
6. Check whether the JSON and HTML outputs were created.

This workflow is focused on the Smart Backlog Assistant meeting-note process.
