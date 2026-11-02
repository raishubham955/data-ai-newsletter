# Weekly Data & AI Newsletter (Cloud Automated)

Autonomous weekly intelligence briefing for Data Engineering, BI, and AI professionals.

## How It Works in the Cloud
* **Schedule:** Runs in the cloud every **Sunday at 09:00 AM IST** (`30 3 * * 0` UTC).
* **Zero PC Dependency:** Executes entirely on GitHub Actions servers. Your PC can be turned off.
* **Storage:** Generates and auto-commits `editions/edition_YYYY-MM-DD.md` directly into this repository.

---

## 3-Step Setup Guide

### 1. Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new) and create a repository (e.g., `data-ai-newsletter`).
2. Make it **Private** or **Public**.

### 2. Push this Folder to Your Repository
Open PowerShell or Terminal in this folder (`C:\Users\shubham.rai\Downloads\Newsletter`) and run:
```bash
git init
git add .
git commit -m "Initial newsletter automation setup"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/data-ai-newsletter.git
git push -u origin main
```

### 3. Add Your Free Gemini API Key to GitHub Secrets
1. Get a free API key at [aistudio.google.com](https://aistudio.google.com/).
2. On your GitHub repository page:
   - Go to **Settings** > **Secrets and variables** > **Actions**.
   - Click **New repository secret**.
   - **Name:** `GEMINI_API_KEY`
   - **Secret:** *(Paste your API key)*
   - Click **Add secret**.
3. Enable Workflow write permissions:
   - Go to **Settings** > **Actions** > **General**.
   - Under **Workflow permissions**, select **Read and write permissions**.
   - Click **Save**.

---

## Manual Test (Optional)
To test immediately without waiting for Sunday:
1. Go to your repo on GitHub.
2. Click the **Actions** tab.
3. Select **Weekly Data & AI Newsletter** on the left.
4. Click **Run workflow** > **Run workflow**.
5. Within 60 seconds, check the `editions/` folder for the newly generated file.
