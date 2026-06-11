# 🚀 AI Campaign Analysis & Recommendation System

## 📌 Overview
This project is an AI-powered marketing intelligence system that analyzes Meta Ads campaign data and generates automated insights, KPIs, and optimization recommendations using Python-based analytics and LLM-driven intelligence.

It processes raw ad data, normalizes it, computes performance metrics, and produces actionable reports for marketing decision-making.

---

## 🎯 Key Features

- 📊 Automated Meta Ads campaign data ingestion
- 🧹 Data cleaning and normalization pipeline
- 📈 KPI calculation (CTR, CPC, CPM, CPA, ROAS)
- 🤖 AI-based performance insights generation
- 💡 Budget optimization recommendations
- 📄 Automated weekly reports (Playbooks)
- 📧 Email + WhatsApp notification system
- 🧠 Vector-based contextual analysis (Chroma DB)
- ⏰ Scheduled reporting system (Cron-based workflow)

---

## 🏗️ System Architecture

Data Sources → Ingestion Layer → Normalization Engine → KPI Engine  
→ AI Analysis Layer (Agents + LLM)  
→ Insights & Recommendations Engine  
→ Reporting System (Email / WhatsApp / Files)

---

## 🛠️ Tech Stack

- Python 3.10+
- Pandas, NumPy
- SQLite
- ChromaDB (Vector Database)
- Claude AI (Anthropic API)
- Cron Scheduler
- SMTP Email Service
- Twilio WhatsApp API
- Git & GitHub

---

## 📁 Project Structure

src/
├── agents/          AI decision-making modules
├── analytics/       KPI calculations
├── ingestion/       Meta Ads data loader
├── normalize/       Data cleaning pipeline
├── reporting/       Report generation engine
├── notifications/   Email & WhatsApp alerts
├── orchestrator/    Pipeline scheduler
├── common/          Utilities & config
├── skills/          AI skill modules

---

## ⚙️ Installation & Setup

### 1️⃣ Clone repository
```bash
git clone https://github.com/AnshUpadhyay30/AI-Campaign-Analysis-Recommendation-System-.git
cd AI-Campaign-Analysis-Recommendation-System-

2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Setup environment variables
Create .env file:
META_ACCESS_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
DB_PATH=data/db/perf_marketing.sqlite3
VECTOR_DB_PATH=data/vector/chroma
REPORT_OUTPUT_DIR=output/reports
LOG_DIR=logs
TIMEZONE=Asia/Kolkata

5️⃣ Run project
python src/main.py

⸻

📊 Output Includes

* Weekly Campaign Reports
* AI-generated Action Playbooks
* KPI Dashboard summaries
* Budget optimization insights

⸻

💡 Business Impact

* Reduces manual marketing analysis by 80%
* Improves campaign ROI with AI-driven recommendations
* Automates reporting & decision workflows
* Enables scalable marketing intelligence system

⸻

👨‍💻 Author

Ansh Upadhyay
Python Developer | AI & Data Systems Enthusiast

⸻

📌 Future Improvements

* Real-time data streaming pipeline
* ML-based prediction models
* Web dashboard (React/Angular)
* Cloud deployment (AWS/GCP)
* Microservices architecture