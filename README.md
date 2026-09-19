# 🔎 CSV Detective

> **Upload a CSV. Let AI investigate the data. Find the story hidden inside it.**

Most CSV analysis tools require you to already know what you're looking for.

**CSV Detective takes the opposite approach.**

Upload an unfamiliar CSV and let an AI investigation agent decide what is worth investigating. Gemini examines the dataset structure, selects relevant analyses, and uses Python-powered tools to calculate evidence-backed results.

---

## 🚀 What It Does

CSV Detective performs an automated investigation of your dataset:

1. **Profiles the dataset**

   * Rows and columns
   * Column types
   * Numeric, categorical, and date columns
   * Missing values
   * Unique values

2. **Investigates relevant patterns**

   * Group comparisons
   * Trends over time
   * Correlations
   * Frequent categorical values
   * Anomalies

3. **Uses AI to reason about the investigation**

   * Gemini acts as the investigation agent
   * The agent decides which analysis tools are relevant
   * Tool results are treated as evidence

4. **Presents findings**

   * Converts raw analysis results into meaningful findings
   * Includes supporting investigation evidence
   * Generates relevant visualizations

---

## 🧠 How It Works

```text
                 CSV File
                    │
                    ▼
             ┌──────────────┐
             │   FastAPI    │
             │    Backend   │
             └──────┬───────┘
                    │
                    ▼
             Dataset Profiling
                    │
                    ▼
          ┌─────────────────────┐
          │   Gemini Agent      │
          │                     │
          │ Decides what to     │
          │ investigate next    │
          └──────────┬──────────┘
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
       Trends   Comparisons  Correlation
          │          │           │
          └──────────┼───────────┘
                     ▼
              Python Analysis
                     │
                     ▼
             Evidence-backed
                Findings
                     │
                     ▼
              React Frontend
```

### Agent-driven investigation

CSV Detective does **not** simply run a fixed list of analyses.

The agent first understands the dataset and then selects relevant tools based on the available columns and data types.

For example:

```text
Dataset contains:
sales → numeric
profit → numeric
region → categorical
date → date
```

The agent can determine that analyses such as:

```text
Region comparisons
Sales/profit correlation
Sales trends
Numeric anomalies
```

may be relevant.

This makes the investigation adaptable to different CSV structures.

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* Axios
* CSS

### Backend

* Python
* FastAPI
* Pandas
* NumPy

### AI

* Google Gemini API
* Gemini function/tool calling

### Deployment

* Vercel — Frontend
* Render — Backend

---

## 📂 Project Structure

```text
CSV-Detective/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── package.json
│   └── .gitignore
│
└── README.md
```

---

## 🔬 Analysis Tools

CSV Detective currently provides the AI agent with several analysis tools:

| Tool                    | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `profile_dataset`       | Understand dataset structure                  |
| `get_top_values`        | Find frequent categorical values              |
| `compare_groups`        | Compare numeric values across groups          |
| `analyze_trend`         | Analyze numeric changes over time             |
| `detect_anomalies`      | Detect unusual numeric values                 |
| `calculate_correlation` | Measure relationships between numeric columns |

The AI agent chooses tools based on the structure and characteristics of the uploaded dataset.

---

## 🔐 Safety & Reliability

CSV Detective is designed so that the AI does not invent numerical findings.

The investigation follows several safeguards:

* Column names are validated before analysis.
* Numeric operations require numeric columns.
* Correlation requires two different numeric columns.
* Trend analysis requires a valid date column.
* Tool failures are handled without crashing the entire investigation.
* Numerical findings are generated from actual tool results.
* Correlation is treated as an association, not automatically as causation.

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/deepikavalluru/CSV-Detective.git
cd CSV-Detective
```

### 2. Backend

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Open the URL provided by Vite.

---

## 🌐 Live Demo

**Frontend:** Add your Vercel deployment URL here.

**Backend:** https://csv-detective.onrender.com

---

## 🎯 Why CSV Detective?

The challenge with an unfamiliar dataset is often not calculating statistics.

It's knowing **what questions to ask in the first place**.

CSV Detective turns that problem into an investigation workflow:

```text
Upload Data
     ↓
Understand Structure
     ↓
Choose Relevant Analyses
     ↓
Calculate Evidence
     ↓
Interpret Findings
     ↓
Discover the Story
```

Instead of asking:

> "What analysis should I run?"

you can simply ask:

> **"What is interesting in this data?"**

---

## 🚧 Future Improvements

Potential future improvements include:

* Real-time investigation progress streaming
* More statistical analysis tools
* Natural-language follow-up questions
* Larger dataset support
* Exportable investigation reports
* More advanced anomaly detection
* Interactive visual exploration

---

## 👩‍💻 Built For

**Hack Devengers 2.0**

Built as an AI-powered data investigation tool focused on making exploratory data analysis more accessible.

---

