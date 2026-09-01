# Troubleshooting

## 1. Docker build fails

Check:
- the Dockerfile exists in the project root
- the project path is correct
- the Python version is supported
- dependencies in requirements.txt are valid

Try:
```bash
cd -/smart-backlog-assistant
docker build --no-cache -t smart-backlog-web -f web/Dockerfile .
docker build -t smart-backlog-gemini-assistant .

```

## 2. Input file not found

Make sure the file exists in the `inputs` folder and the command uses the correct path:
```bash
--input inputs/meeting_notes_auth.txt
```

## 3. Output files not created

Check that the `outputs` folder exists and the command includes both output flags:
```bash
--output-json outputs/result.json
--output-html outputs/dashboard.html
```

## 4. Missing API key

Set the environment variable before running the container:
```bash
-e GEMINI_API_KEY="YOUR_KEY"
```

## 5. App starts but fails during processing

Check:
- input file format
- file permissions
- whether the output path is writable
- whether Gemini access is working

## Common startup command

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

```bash
docker run --rm -it --env-file .env -p 5002:5000 \
  -v "$(pwd)/inputs:/app/inputs" \
  -v "$(pwd)/outputs:/app/outputs" \
  smart-backlog-web
```
