import os
import re
import sys
from datetime import datetime, timedelta

def get_date_range():
    today = datetime.now()
    start_date = today - timedelta(days=7)
    return today.strftime("%Y-%m-%d"), start_date.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")

def validate_and_count_words(line):
    # Extracts text before [URL] and counts words
    m = re.match(r"^-\s+(.*?)\s+\[(https?://[^\s\]]+)\]$", line.strip())
    if not m:
        return None, 0
    text = m.group(1).strip()
    words = text.split()
    return text, len(words)

def build_prompt(today_str, start_str, end_str):
    return f"""Role: Senior Technology Research Analyst specializing in Data Engineering, Analytics, BI, and AI.

Task: Prepare the weekly Data & AI Industry Intelligence report covering the LAST 7 DAYS ({start_str} to {end_str}).

CRITICAL OUTPUT FORMATTING RULES (STRICTLY ENFORCE):
1. Each news item must appear on a single line starting with a dash: - 
2. One line must contain only ONE news development.
3. Every single news item MUST contain between 10 and 15 words only (excluding the source URL in brackets at the end).
4. Include the company or product name in every news line.
5. Add the verified original source URL in brackets at the end of each line, e.g. [https://www.example.com]
6. No paragraphs, sub-bullets, asterisks inside lines, or lengthy explanations.
7. Use simple, direct, conversational English.
8. Maintain the exact following sections with bold headers:

**Top Data & AI News | Weekly Edition ({end_str})**

**Data Engineering**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]
- [Item 4 (10-15 words)] [Source URL]

**Data Analytics & BI**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]
- [Item 4 (10-15 words)] [Source URL]

**AI x Data**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]
- [Item 4 (10-15 words)] [Source URL]

**Funding & Acquisitions**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]
- [Item 4 (10-15 words)] [Source URL]

**New Tools & Hardware**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]

**Industry Insights**
- [Item 1 (10-15 words)] [Source URL]
- [Item 2 (10-15 words)] [Source URL]
- [Item 3 (10-15 words)] [Source URL]
- [Item 4 (10-15 words)] [Source URL]

Strictly count words before outputting. Every item must be between 10 and 15 words.
"""

def generate_report():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    today_file_str, start_str, end_str = get_date_range()
    prompt = build_prompt(today_file_str, start_str, end_str)

    # Use Google GenAI SDK
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    
    model_name = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    print(f"Generating newsletter for {start_str} to {end_str} using {model_name}...")
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}],
            temperature=0.2,
        )
    )

    report_text = response.text.strip()
    
    # Save output to editions folder
    output_dir = os.path.join(os.path.dirname(__file__), "editions")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"edition_{today_file_str}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")

    print(f"Successfully generated and saved: {filepath}")

if __name__ == "__main__":
    generate_report()
