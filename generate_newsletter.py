import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_date_range_and_previous_news():
    today = datetime.now()
    today_date = today.date()

    editions_dir = os.path.join(os.path.dirname(__file__), "editions")
    last_date = None
    previous_bullets = []

    if os.path.exists(editions_dir):
        edition_files = []
        for fname in os.listdir(editions_dir):
            m = re.match(r"^edition_(\d{4}-\d{2}-\d{2})\.md$", fname)
            if m:
                try:
                    d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                    edition_files.append((d, os.path.join(editions_dir, fname)))
                except ValueError:
                    pass

        # Sort descending by date
        edition_files.sort(key=lambda x: x[0], reverse=True)

        # Find the latest edition published strictly before today
        past_files = [x for x in edition_files if x[0] < today_date]
        if past_files:
            target_entry = past_files[0]
        elif edition_files:
            # If running on the same day as the newest edition, check for an older edition
            if len(edition_files) > 1:
                target_entry = edition_files[1]
            else:
                target_entry = edition_files[0]
        else:
            target_entry = None

        if target_entry:
            last_date, target_path = target_entry
            try:
                with open(target_path, "r", encoding="utf-8") as pf:
                    for line in pf:
                        line_s = line.strip()
                        if line_s.startswith("- "):
                            previous_bullets.append(line_s)
            except Exception as e:
                print(f"Warning: Could not read previous edition ({target_path}): {e}")

    # Fallback if no prior edition found or if dates match
    if not last_date or last_date >= today_date:
        last_date = today_date - timedelta(days=7)

    delta_days = (today_date - last_date).days
    if delta_days <= 0:
        delta_days = 7

    today_file_str = today.strftime("%Y-%m-%d")
    start_str = last_date.strftime("%B %d, %Y")
    end_str = today.strftime("%B %d, %Y")

    return today_file_str, start_str, end_str, delta_days, previous_bullets

def fetch_recent_news_rss(delta_days=7):
    days = max(3, delta_days)
    topics = [
        "Data Engineering lakehouse dbt",
        "Microsoft Fabric Power BI analytics",
        "Databricks Snowflake data AI",
        "AI agents data engineering text-to-sql",
        "OpenAI Anthropic enterprise AI data",
        "Data tech startup funding acquisition",
    ]
    articles = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for topic in topics:
        try:
            query = urllib.parse.quote(f"{topic} when:{days}d")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item")[:5]:
                    title = item.findtext("title", "")
                    if title:
                        articles.append(f"- {title}")
        except Exception as e:
            print(f"Warning: Could not fetch RSS news for '{topic}': {e}")
    return "\n".join(articles)

def validate_and_count_words(line):
    line = line.strip()
    if not line.startswith("- "):
        return None, 0
    text = line[2:].strip()
    words = text.split()
    return text, len(words)

def build_prompt(today_str, start_str, end_str, previous_bullets):
    previous_block = ""
    if previous_bullets:
        bullets_text = "\n".join(previous_bullets[:40])
        previous_block = f"""
## MANDATORY DEDUPLICATION: ALREADY PUBLISHED NEWS (DO NOT REPEAT)

The following developments were ALREADY reported in the previous edition ({start_str}):
{bullets_text}

CRITICAL DEDUPLICATION RULES:
1. ONLY pick news developments announced strictly AFTER {start_str} up to {end_str}.
2. Do NOT duplicate, re-report, or rephrase any news story from the previous edition above.
3. Every news item must be a fresh development that occurred strictly between {start_str} and {end_str}.
4. If a previously mentioned tool or company is included, it MUST be a brand new, subsequent milestone announced after {start_str}.
"""

    return f"""# MASTER PROMPT: Weekly Data & AI Industry Intelligence

Reporting Period: {start_str} to {end_str}
{previous_block}
## 1. Your Role

Act as a Senior Technology Research Analyst specializing in Data Engineering, Data Analytics, Business Intelligence, Cloud Data Platforms, and Artificial Intelligence.

Your responsibility is to research the latest industry developments that occurred strictly between {start_str} (last execution date) and {end_str} (current execution date) and prepare a comprehensive weekly intelligence report.

The report will be delivered to my email every week and used to create my LinkedIn newsletter.

My objective is to keep data professionals informed about the latest industry developments and help them understand where the Data and AI industry is heading.

## 2. Main Research Categories

### A. Data Engineering
Track the latest developments in:
- Data Engineering tools and technologies.
- ETL and ELT platforms.
- Data pipelines and workflow orchestration.
- Data warehouses, data lakes, and lakehouse architecture.
- Real-time data processing and streaming.
- Data quality, observability, and governance.
- Apache Spark, Kafka, Flink, Airflow, and dbt.
- Delta Lake and Apache Iceberg.
- Data integration and migration solutions.
- AI-powered data engineering and autonomous pipelines.
- Database innovations and vector databases.
- Data infrastructure and cloud computing.

### B. Data Analytics and Business Intelligence
Track developments related to:
- Microsoft Power BI.
- Microsoft Fabric.
- Tableau and Looker.
- Databricks AI/BI.
- Snowflake analytics.
- Semantic models and semantic layers.
- Self-service analytics.
- Natural language querying.
- AI-powered dashboards and reporting.
- Predictive and advanced analytics.
- Business intelligence automation.
- Analytics engineering.

### C. AI Developments in Data Engineering and Analytics (HIGH PRIORITY)
Research how AI is changing traditional data engineering and analytics workflows.
Cover:
- AI agents for Data Engineering and AI Data Analysts.
- Autonomous data pipelines.
- AI-powered SQL generation and Text-to-SQL solutions.
- AI-assisted Python and coding.
- AI-powered ETL and data transformation.
- Automated data quality monitoring.
- AI-powered database management.
- Agentic analytics.
- Model Context Protocol (MCP) for data platforms.
- Retrieval Augmented Generation (RAG).
- Enterprise AI data integration.
- AI-powered reporting and visualization.
- AI-assisted data migration.
- AI agents interacting with enterprise databases.
Focus on real product developments, practical use cases, and industry adoption.

### D. Major AI Company Developments
Closely monitor:
- OpenAI: GPT models, ChatGPT, Codex, APIs, agents, and developer tools.
- Anthropic: Claude models, Claude Code, Agent Skills, MCP, and enterprise AI.
- Google: Gemini, Google DeepMind, Vertex AI, and AI developer tools.
- Microsoft: Copilot, Azure AI, Fabric AI, and enterprise AI.
- Meta: Llama models, AI infrastructure, and open-source AI.
- Amazon: AWS Bedrock, Amazon Q, and AI services.
- Perplexity: AI search, enterprise solutions, and developer products.
- xAI: Grok models and AI infrastructure.
- Mistral AI: Enterprise models and AI development tools.
- Cohere: Enterprise AI and retrieval solutions.
Include only developments relevant to Data Engineering, Analytics, databases, enterprise data, and AI-powered development.

### E. Major Data Technology Companies
Monitor these companies and their products:
- Microsoft (Fabric, Power BI, Azure Data Factory, Azure Synapse, OneLake, Fabric Data Engineering, Fabric Data Warehouse, Copilot)
- Databricks (Lakehouse, Delta Lake, Unity Catalog, Databricks SQL, Lakeflow, Genie, Genie Code, Lakebase, AI/BI, Mosaic AI, MLflow)
- Snowflake (Snowflake Cortex AI, Snowpark, Snowflake Intelligence, Snowflake Openflow, Snowflake Data Cloud, Apache Iceberg integration)
- Other Important Companies: Google Cloud, AWS, Oracle, Salesforce, MongoDB, Confluent, dbt Labs, Fivetran, Informatica, Palantir, Elastic, ThoughtSpot, Qlik, Teradata, Starburst, ClickHouse, SingleStore.
Track their new features, product releases, partnerships, acquisitions, funding, and technology announcements.

## 3. Funding, Acquisitions and Business Developments
Research important industry business news, including startup funding rounds (Series A/B/C/later), M&A, partnerships, IPOs, enterprise contracts, GPU/cloud investments. Prioritize Data Engineering, Analytics, AI, databases, and enterprise software. Include funding amounts when officially available.

## 4. New Product and Feature Releases
Prioritize actual product launches, GA announcements, public beta releases, and significant feature enhancements. Do not include minor updates.

## 5. Strict Research Rules
1. Research news strictly published between {start_str} and {end_str} (after the previous execution date).
2. Do NOT duplicate or repeat any news from the previous edition. Only fresh developments announced after {start_str}.
3. Mention actual announcement details accurately; never invent releases, amounts, or acquisitions.
4. Exclude rumours and unconfirmed claims. Avoid duplicate news across different sections.
5. Include relevant global developments (and significant Indian data/AI industry developments when applicable).

## 6. FINAL REPORT FORMAT
Prepare the report using EXACTLY the following structure:

# WEEKLY DATA & AI INDUSTRY INTELLIGENCE

Reporting Period: {start_str} to {end_str}

### 1. TOP 5 INDUSTRY HEADLINES

- [Headline 1 (10-15 words)]
- [Headline 2 (10-15 words)]
- [Headline 3 (10-15 words)]
- [Headline 4 (10-15 words)]
- [Headline 5 (10-15 words)]

### 2. DATA ENGINEERING NEWS

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 3. DATA ANALYTICS & BUSINESS INTELLIGENCE

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 4. AI x DATA

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 5. FUNDING, ACQUISITIONS & PARTNERSHIPS

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 6. NEW PRODUCTS & FEATURE RELEASES

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 7. INDUSTRY INSIGHTS: WHAT THIS MEANS FOR DATA PROFESSIONALS

- [Item 1 (10-15 words)]
- [Item 2 (10-15 words)]
- [Item 3 (10-15 words)]
- [Item 4 (10-15 words)]

### 8. LINKEDIN NEWSLETTER TOPIC IDEAS

1. [Topic 1 Headline]
2. [Topic 2 Headline]
3. [Topic 3 Headline]

## 7. STRICT OUTPUT FORMATTING RULES (MANDATORY)

- One News = One Line. Every news item must appear on a single line starting with a dash: -
- Each line must contain exactly one news development.
- EVERY single news line MUST contain between 10 and 15 words only.
- Do NOT write paragraphs under any section.
- Do NOT add separate What Happened / Why Important / Impact fields.
- Combine the announcement and its importance into one concise sentence.
- CRITICAL: DO NOT INCLUDE SOURCE URLS OR HYPERLINKS IN THE OUTPUT.
- Do not add lengthy explanations.
- Do not repeat the same news in multiple sections.
- Use simple, conversational English.
- Headings and reporting dates are exempt from the word limit.
- Company names, product names, technical terms, and financial figures must remain accurate.
- Strictly count words for each news line before generating. Every single news item must be 10-15 words.

## 8. STRICT TECHNICAL SPECIFICITY (NO VAGUE/GENERIC STATEMENTS)

Every news item MUST be concrete, detailed, and technically specific:
- Name the exact feature, protocol, API, parameter, library, benchmark, or architecture.
- Use precise technical terminology (e.g., DAX, CDC, Iceberg, Delta Lake, MCP, S/4HANA, Zero-ETL, Structured Outputs, OpenTelemetry).
- STRICTLY BANNED VAGUE PHRASES:
  * DO NOT WRITE: "released new capabilities", "simplifying workflows", "improving analytics", "enhancing features", "expanding possibilities", "improving performance", "advancing workflows".
  * INSTEAD WRITE: What exact tool was released, what exact mechanism it uses, and what architectural problem it solves.
- Examples:
  * BAD (Vague): "Microsoft released new Fabric capabilities, simplifying enterprise analytics and data management workflows."
  * GOOD (Specific): "Microsoft Fabric launched native Apache Iceberg support, allowing direct Delta-to-Iceberg engine querying."
  * BAD (Vague): "OpenAI introduced new developer capabilities, expanding automated coding and data workflows."
  * GOOD (Specific): "OpenAI introduced Structured Outputs in the Responses API, guaranteeing strict JSON schema compliance."
  * BAD (Vague): "Databricks introduced additional Lakeflow features, reducing infrastructure management for data ingestion."
  * GOOD (Specific): "Databricks released Lakeflow Connect for serverless change data capture across enterprise databases."
"""

def generate_report():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    today_file_str, start_str, end_str, delta_days, previous_bullets = get_date_range_and_previous_news()
    prompt = build_prompt(today_file_str, start_str, end_str, previous_bullets)

    # Use Google GenAI SDK
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    
    model_name = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    print(f"Generating newsletter for period {start_str} to {end_str} ({delta_days} days) using {model_name}...")
    if previous_bullets:
        print(f"Loaded {len(previous_bullets)} previously published stories to prevent duplication.")
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                temperature=0.2,
            )
        )
    except Exception as e:
        error_msg = str(e)
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            print("Notice: Search Grounding quota exceeded or unbilled project detected.")
            print(f"Fetching live news headlines via RSS feeds for past {delta_days} days...")
            live_news = fetch_recent_news_rss(delta_days=delta_days)
            fallback_prompt = (
                f"{prompt}\n\n"
                f"RECENT LIVE HEADLINES (PAST {delta_days} DAYS, AFTER {start_str}):\n"
                f"{live_news}\n\n"
                f"Synthesize the briefing adhering strictly to all formatting rules. Do NOT include URLs or repeat previous news."
            )
            response = client.models.generate_content(
                model=model_name,
                contents=fallback_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                )
            )
        else:
            raise e

    report_text = response.text.strip()
    
    # Save output to editions folder
    output_dir = os.path.join(os.path.dirname(__file__), "editions")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"edition_{today_file_str}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")

    # Also save/update the root edition copy
    root_filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(root_filepath, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")

    print(f"Successfully generated and saved: {filepath}")
    print(f"Successfully updated root copy: {root_filepath}")

if __name__ == "__main__":
    generate_report()
