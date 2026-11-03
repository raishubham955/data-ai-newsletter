import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_date_range():
    today = datetime.now()
    start_date = today - timedelta(days=7)
    return today.strftime("%Y-%m-%d"), start_date.strftime("%B %d, %Y"), today.strftime("%B %d, %Y")

def fetch_recent_news_rss():
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
            query = urllib.parse.quote(f"{topic} when:7d")
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

def build_prompt(today_str, start_str, end_str):
    return f"""# MASTER PROMPT: Weekly Data & AI Industry Intelligence

## 1. Your Role

Act as a Senior Technology Research Analyst specializing in Data Engineering, Data Analytics, Business Intelligence, Cloud Data Platforms, and Artificial Intelligence.

Your responsibility is to research the latest industry developments from the previous 7 days ({start_str} to {end_str}) and prepare a comprehensive weekly intelligence report.

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
1. Research news published within the previous 7 calendar days ({start_str} to {end_str}).
2. Mention actual announcement details accurately; never invent releases, amounts, or acquisitions.
3. Exclude rumours and unconfirmed claims. Avoid duplicate news across different sections.
4. Include relevant global developments (and significant Indian data/AI industry developments when applicable).

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
            print("Fetching live news headlines via RSS feeds and generating briefing directly...")
            live_news = fetch_recent_news_rss()
            fallback_prompt = (
                f"{prompt}\n\n"
                f"RECENT LIVE HEADLINES (PAST 7 DAYS):\n"
                f"{live_news}\n\n"
                f"Synthesize the briefing adhering strictly to all formatting rules. Do NOT include URLs."
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
