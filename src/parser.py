import os
import json
from pathlib import Path
from pypdf import PdfReader

class DocumentParser:
    @staticmethod
    def load_file(file_path: str, auto_delete: bool = False) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        ext = path.suffix.lower()
        extracted_text = ""

        try:
            if ext == ".pdf":
                reader = PdfReader(path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            elif ext in [".txt", ".md"]:
                with open(path, "r", encoding="utf-8") as f:
                    extracted_text = f.read()
            else:
                raise ValueError(f"Unsupported file format: {ext}. Use .txt, .md, or .pdf")
            
            # Optional auto-deletion feature flag implementation
            if auto_delete:
                path.unlink()
                
            return extracted_text
        except Exception as e:
            raise IOError(f"Error processing file {file_path}: {e}")

    @staticmethod
    def save_output(data: dict, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def save_html_dashboard(data: dict, output_html_path: str):
        """Generates an executive HTML dashboard view from the backlog data with a formatted timestamp."""
        os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
        timestamp = data.get('generated_at', 'N/A')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Smart Backlog Intelligence Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }}
        .container {{ max-width: 1000px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 15px; margin-top: 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
        .timestamp {{ font-size: 14px; color: #94a3b8; font-weight: normal; background: #0f172a; padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }}
        .card {{ background: #0f172a; border-left: 5px solid #38bdf8; padding: 20px; margin-bottom: 20px; border-radius: 8px; }}
        .badge {{ display: inline-block; padding: 4px 10px; font-size: 12px; font-weight: bold; border-radius: 4px; }}
        .High {{ background: #ef4444; color: white; }}
        .Medium {{ background: #f59e0b; color: white; }}
        .Low {{ background: #10b981; color: white; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 6px; color: #cbd5e1; }}
        .risk-box {{ background: #451a03; border-left: 5px solid #f59e0b; padding: 15px; margin-top: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>
            <span>⚡ Smart Backlog Executive Dashboard</span>
            <span class="timestamp">Generated: {timestamp}</span>
        </h1>
        <div class="card">
            <h3>Project Executive Summary</h3>
            <p>{data.get('project_summary', 'No summary available.')}</p>
        </div>
        
        <h2>User Stories ({len(data.get('user_stories', []))})</h2>
"""
        for story in data.get('user_stories', []):
            p_class = story.get('priority', 'Medium')
            html_content += f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-family: monospace; color: #94a3b8;">{story.get('id')}</span>
                <div>
                    <span class="badge {p_class}">Priority: {p_class}</span>
                    <span class="badge" style="background: #6366f1; color: white; margin-left: 5px;">Points: {story.get('estimate_points')}</span>
                </div>
            </div>
            <h3 style="margin: 10px 0; color: #f1f5f9;">{story.get('title')}</h3>
            <p><strong>Story:</strong> <em>{story.get('user_story')}</em></p>
            <p><strong>Acceptance Criteria:</strong></p>
            <ul>
"""
            for ac in story.get('acceptance_criteria', []):
                html_content += f"                <li>{ac}</li>\n"
            html_content += f"""            </ul>
        </div>
"""

        html_content += """
        <div class="risk-box">
            <h3>Identified Technical Risks</h3>
            <ul>
"""
        for risk in data.get('identified_risks', []):
            html_content += f"                <li>{risk}</li>\n"
        html_content += f"""            </ul>
        </div>
    </div>
</body>
</html>
"""
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)