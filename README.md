# 🚀 GrowthPilot AI — AI-Powered Business Growth Assistant

GrowthPilot AI is a practical, technology-focused AI growth and automation web application designed to help small businesses, freelancers, and growth consultants research markets, qualify inbound leads, craft personalized outreach, generate multi-platform marketing content, and test prompt engineering strategies.

Built for the **AI Growth & Automation Associate** practical assessment at **Gokul Infocare**.

---

## 🌟 Core Features

The application provides five focused business growth tools accessible via an intuitive sidebar:

1. **🔎 Business Research**
   * Synthesizes user-provided business and audience context into structured market hypotheses, customer segmentation, marketing opportunities, and prioritized growth recommendations.
   * Explicitly avoids hallucinated web research claims and marks speculative items as hypotheses requiring validation before capital is committed.

2. **🎯 Lead Qualification**
   * Evaluates prospect alignment against an Ideal Customer Profile (ICP) using a transparent 100-point scoring rubric:
     - Need Alignment (30 pts)
     - Business Fit (30 pts)
     - Budget Viability (15 pts)
     - Decision-Maker Access (10 pts)
     - Urgency and Timeline (15 pts)
   * Renders the evaluation in a structured Markdown scoring table with confirmed points, evidence, and status. Unknown budget, decision-maker access, or timeline are marked as "Pending discovery" rather than assumed or penalized, accompanied by Confirmed Subtotal (/60), Pending Points (/40), and Potential Score Range.

3. **✉️ Personalized Outreach Email Generator**
   * Produces concise, professional, ready-to-edit B2B outreach emails.
   * Enforces ethical copywriting principles: no fabricated testimonials, no fake mutual connections, clear bracketed placeholders, and low-pressure calls to action.

4. **📣 Marketing Content Generator**
   * Generates platform-tailored marketing copy for LinkedIn, Instagram, Facebook, or Email Campaigns based on specified campaign goals and tone.
   * Provides opening hooks, grounded calls to action, relevant hashtags, and alternative hooks for A/B testing.

5. **🧪 Prompt Testing & Optimization Lab**
   * A side-by-side comparative laboratory that runs a basic, unconstrained prompt against an engineered, constraint-enforced prompt for any user-defined business task.
   * Illustrates how prompt engineering eliminates hallucinations, improves actionability, and ensures factual reliability.

---

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Web Framework:** [Streamlit](https://streamlit.io/)
* **AI Provider / LLM SDK:** [Google GenAI SDK](https://pypi.org/project/google-genai/) (`google-genai`)
* **Environment Configuration:** `python-dotenv`
* **Data & Presentation:** Markdown (GFM tables), Pandas

---

## 📂 Project Structure

```text
growthpilot-ai/
├── app.py                      # Main Streamlit web application
├── llm.py                      # Google Gemini API interface & helper
├── test_gemini.py              # Quick connection test for Google Gemini API
├── requirements.txt            # Python dependencies
├── .env                        # Local environment variables (API key & model; gitignored)
├── .gitignore                  # Git exclusions for secrets, venv, and cache
├── AI_PROMPT_DOCUMENTATION.md  # Detailed prompt engineering documentation
├── DEMO_SCRIPT.md              # 3-4 minute video demonstration presentation script
└── README.md                   # Project overview and evaluation instructions
```

---

## 🚀 Setup & Execution Instructions

Follow these steps to run GrowthPilot AI locally:

### 1. Prerequisites
* Python 3.10, 3.11, or 3.12 installed on your machine.
* A [Google Gemini API Key](https://aistudio.google.com/apikey).

### 2. Clone or Extract the Project
Open a terminal in the project directory:
```bash
cd growthpilot-ai
```

### 3. Create and Activate a Virtual Environment
* **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create or verify a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```
> **Note on Models:** The default model is `gemini-3.5-flash` with automatic fallback to `gemini-3.1-flash-lite` if needed.

### 6. Test the API Connection
Run the included test script to verify your Google Gemini API key and model:
```bash
python test_gemini.py
```
You should see:
```text
Testing GrowthPilot AI connection to Google Gemini API...
SUCCESS! Google Gemini API returned a response.
```

### 7. Run the Web Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Streamlit will automatically open the application in your browser at `http://localhost:8501`.

---

## 🔒 Security & Privacy

* Secret API keys are loaded exclusively from `.env` via `python-dotenv`.
* The `.gitignore` file excludes `.env`, `.venv/`, `.streamlit/secrets.toml`, and all cache directories to prevent accidental credential leakage.

---

## 📑 Assignment Submission Deliverables

Per the assignment requirements:
1. **Video Presentation:** See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the structured 3–4 minute presentation script.
2. **Prompt Documentation:** See [AI_PROMPT_DOCUMENTATION.md](AI_PROMPT_DOCUMENTATION.md) for full documentation of system prompts, user prompts, revisions, rationale, and observed differences.
3. **Project Link:** Code prepared for sharing via GitHub repository or Google Drive folder.
