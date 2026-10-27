# GrowthPilot AI — Video Demonstration Script

**Target Video Length:** 3 to 4 minutes (minimum requirement: 2 minutes)  
**Speaker:** Candidate / Project Developer  
**Audience:** Evaluation Team, Gokul Infocare  
**Role:** AI Growth & Automation Associate  

---

## Demonstration Overview Timeline

| Timecode | Segment | Core Topic Covered |
|---|---|---|
| **0:00 – 0:35** | Introduction & Tools Selected | Project purpose, domain, tech stack (Streamlit, Python, OpenRouter). |
| **0:35 – 1:20** | Prompt Engineering & Iterative Design | Evolution from naive prompts to constrained, rubric-driven prompts. |
| **1:20 – 1:55** | Development Approach & Problem Solving | Systematic design, handling rate limits & raw markdown table formatting. |
| **1:55 – 3:15** | Live Walkthrough & Five Core Features | Guided demonstration of all 5 features in GrowthPilot AI. |
| **3:15 – 3:45** | Practical Business Impact & Conclusion | Real-world application, validation ethics, wrap-up. |

---

## Detailed Script & Visual Direction

### Section 1: Introduction & Tools Used (0:00 – 0:35)

* **Visual on Screen:**  
  * Screen recording showing the GrowthPilot AI homepage running locally in the browser (`http://localhost:8501`).
  * Sidebar showing the title "🚀 GrowthPilot AI" and dropdown of the 5 tools.
* **Spoken Dialogue:**  
  > "Hello everyone. Today I'm excited to present **GrowthPilot AI**, an AI-powered business growth and automation assistant designed specifically for small businesses, freelancers, and growth consultants in the technology domain.  
  >  
  > For this project, I chose **Python** and **Streamlit** for rapid, interactive web application deployment, paired with **OpenRouter** as the unified LLM API. OpenRouter was selected because it provides flexible access to state-of-the-art open-source and proprietary models without vendor lock-in, allowing seamless testing and cost optimization."

---

### Section 2: Prompt Engineering Strategy & Iteration (0:35 – 1:20)

* **Visual on Screen:**  
  * Transition to the `AI_PROMPT_DOCUMENTATION.md` file or code view in `app.py`, highlighting the system prompts and user prompts.
* **Spoken Dialogue:**  
  > "Prompt engineering is the core driver of GrowthPilot AI. When I initially experimented with simple prompts, the AI consistently suffered from three major issues:  
  > 1. It hallucinated fake market statistics and customer research.  
  > 2. It gave subjective, unverified scores without clear criteria.  
  > 3. It wrote pushy sales copy claiming non-existent client testimonials.  
  >  
  > To solve this, I implemented an iterative prompt architecture:  
  > - **System Prompt Grounding:** The system prompt explicitly forbids inventing data or claiming web search capabilities.  
  > - **Hypothesis Separation:** Recommendations must distinguish known user facts from reasonable hypotheses that require validation.  
  > - **Mathematical Rubrics:** The Lead Qualification feature uses a transparent 100-point rubric across five defined criteria, scoring unknown fields conservatively rather than assuming full fit."

---

### Section 3: Technical Approach & Challenges Resolved (1:20 – 1:55)

* **Visual on Screen:**  
  * Showing `app.py` helper functions, specifically `format_ai_markdown` and the OpenRouter error handler.
* **Spoken Dialogue:**  
  > "During development, I encountered two technical challenges:  
  >  
  > First, in the **Lead Qualification** feature, models occasionally wrapped the markdown scoring table inside code blocks or omitted preceding blank lines. This caused the UI to display raw pipes and markdown characters rather than a clean table. I solved this by refining the prompt to specify exact table formatting and building a sanitization helper (`format_ai_markdown`) that strips accidental code fences and normalizes spacing so Streamlit's GFM renderer always outputs a proper HTML table.  
  >  
  > Second, handling upstream API rate limits. Instead of letting the application crash, I implemented defensive error handling that cleanly displays user-friendly warnings and technical diagnostics while keeping API keys completely secure."

---

### Section 4: Live Application Walkthrough (1:55 – 3:15)

* **Visual on Screen:**  
  * Return to the live Streamlit web application. Walk through the sidebar dropdown step-by-step.

#### 1. Business Research (1:55 – 2:15)
* **Visual:** Select **Business Research**. Input:
  * *Business:* "Cloud-based inventory management for boutique coffee roasters."
  * *Audience:* "Independent specialty coffee shop owners."
  * Click **Research Business**.
* **Spoken Dialogue:**  
  > "First is **Business Research**. Notice how the output provides a structured overview, customer needs labeled explicitly as hypotheses, potential segments, and three prioritized growth recommendations with validation steps."

#### 2. Lead Qualification (2:15 – 2:35)
* **Visual:** Switch to **Lead Qualification**. Input:
  * *ICP:* "Small businesses needing modern websites with online ordering."
  * *Lead:* "A local bakery with an outdated website wanting online orders, budget unverified."
  * Click **Qualify Lead**.
* **Spoken Dialogue:**  
  > "Next, **Lead Qualification**. Look at the scoring table: it renders as a clean, structured table with Max Points, Awarded Points, and evidence. Because budget is unverified, it awards zero points for that criterion rather than guessing, resulting in a conservative 65 out of 100 with actionable discovery questions."

#### 3. Email Generator & Marketing Content (2:35 – 2:55)
* **Visual:** Briefly demonstrate **Email Generator** and **Marketing Content**.
* **Spoken Dialogue:**  
  > "The **Email Generator** produces concise, professional outreach emails with clear placeholders and low-pressure calls to action—no pushy sales tricks. Meanwhile, the **Marketing Content Generator** tailors copy specifically for LinkedIn, Instagram, or Facebook with multiple alternative hooks for A/B testing."

#### 4. Prompt Testing Lab (2:55 – 3:15)
* **Visual:** Select **Prompt Testing Lab**. Enter:
  * *Task:* "Write a LinkedIn post promoting website development for dentists."
  * Click **Compare Prompts**.
* **Spoken Dialogue:**  
  > "Finally, the **Prompt Testing Lab** gives users a transparent look at prompt engineering by running a basic prompt and an engineered prompt side-by-side. You can immediately see the improved version eliminates fluff, respects factual boundaries, and provides structured value."

---

### Section 5: Conclusion & Real-World Impact (3:15 – 3:45)

* **Visual on Screen:**  
  * Return to main page header or camera view.
* **Spoken Dialogue:**  
  > "In summary, GrowthPilot AI demonstrates how thoughtful prompt engineering, disciplined guardrails, and clean user experience turn AI from a novelty into a dependable business growth tool.  
  >  
  > The entire project is documented in `AI_PROMPT_DOCUMENTATION.md`, ready to run locally, and structured for easy review. Thank you for your time, and I look forward to discussing how I can bring these AI growth and automation skills to Gokul Infocare."

---

## Recording Checklist for the Candidate
- [ ] Ensure local virtual environment is active: `.venv\Scripts\activate`
- [ ] Confirm `.env` has valid `OPENROUTER_API_KEY` and accessible `OPENROUTER_MODEL`
- [ ] Run the app: `streamlit run app.py`
- [ ] Test screen recorder (OBS, Loom, or Windows Game Bar `Win + G`) with microphone audio
- [ ] Verify video duration is at least 2 minutes (target: 3–4 minutes)
- [ ] Upload video to Google Drive or YouTube (unlisted) and ensure link sharing is set to "Anyone with the link can view"
