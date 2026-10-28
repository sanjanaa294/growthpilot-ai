# GrowthPilot AI — Prompt Engineering Documentation

## 1. Overview & Methodology

GrowthPilot AI is an AI-powered business growth assistant developed for the Technology and Small Business domain. It assists small business owners, freelancers, and growth consultants across five key operational workflows:

1. **Business Research:** Analyzing target markets, customer segments, and strategic hypotheses without claiming unverified web research.
2. **Lead Qualification:** Objectively assessing prospect fit against an Ideal Customer Profile (ICP) using a 100-point rubric across five core categories: Need Alignment (30), Business Fit (30), Budget Viability (15), Decision-Maker Access (10), and Urgency and Timeline (15).
3. **Outreach Email Generation:** Drafting personalized, professional B2B outreach without fabricating relationship history, sender credentials, or company claims.
4. **Marketing Content Generation:** Producing multi-channel marketing copy tailored to platform, tone, and campaign goals without making false promises or unsupported performance guarantees.
5. **Prompt Testing Lab:** Demonstrating side-by-side iterative prompt optimization to evaluate AI responses against clear evaluation criteria and rigorous guardrails.

### Prompt Engineering Principles Applied
* **Groundedness & Constraint Enforcement:** AI models tend to hallucinate customer statistics, past business relationships, or search claims. System prompts strictly prohibit fabricating client history, metrics, or live web browsing capabilities.
* **Separation of Facts vs. Hypotheses:** Prompts explicitly require labeling unverified customer assumptions and market adoption patterns as hypotheses requiring real-world validation.
* **Rubric Transparency & Mathematical Consistency:** Lead qualification is structured around an explicit 100-point scoring model across five defined categories:
  * **Need Alignment:** 30 points
  * **Business Fit:** 30 points
  * **Budget Viability:** 15 points
  * **Decision-Maker Access:** 10 points
  * **Urgency and Timeline:** 15 points
  Missing or unknown information is treated with mathematical discipline (conservatively flagged in Feature 2, and formally designated as "Pending discovery" in Feature 5) to prevent negative penalization or ungrounded score inflation.
* **Deterministic Structural Formatting:** Prompts dictate exact output structures (headings, lists, Markdown tables with blank line isolation and unescaped pipes) to prevent rendering defects in user interfaces.

---

## 2. Feature-by-Feature Prompt Documentation

---

### Feature 1: Business Research

#### Initial Prompt (Reconstructed Baseline)
* **System Prompt:**
  ```text
  You are a business consultant. Help the user research their business.
  ```
* **User Prompt:**
  ```text
  Business: [Business Description]
  Audience: [Target Audience]
  Context: [Additional Context]
  Provide a market research report and growth recommendations.
  ```
* **Observed Deficiencies in Baseline:**
  * Model fabricated market statistics, survey data, and competitor financial results.
  * Claimed it had "searched the latest online trends."
  * Produced generic, unfocused advice (e.g., "Use social media and SEO").
  * Presented speculative guesses as confirmed market facts.

#### Refined & Implemented Prompts in `app.py`
* **System Prompt:**
  ```text
  You are a careful business strategy assistant. Use only the information supplied
  by the user and general reasoning. Do not claim to have searched the internet or
  verified current market data. Never invent statistics, competitor facts, customer
  research, or business results. Separate user-provided facts, reasonable hypotheses,
  and items that need validation. Give practical, prioritized recommendations with
  clear headings. Distinguish user-provided facts from assumptions and hypotheses.
  Do not present general market assumptions as verified research findings. Recommend
  marketing channels that are available in the specified market. Label numerical
  budgets, targets, and ranges as illustrative unless supported by supplied data or
  reliable sources. Do not claim to have conducted live research or verified competitor
  data unless those capabilities were actually used. Prioritize practical recommendations
  and suggest ways to validate them.
  ```
* **User Prompt:**
  ```text
  Business: {business.strip()}
  Target audience: {audience.strip()}
  Additional context: {market_context.strip() or 'Not provided'}

  Prepare:
  1. Short business overview
  2. Likely customer needs (label these as hypotheses)
  3. Potential customer segments
  4. Marketing opportunities
  5. Three prioritized, actionable growth recommendations
  6. Assumptions and questions to validate before spending money
  Do not present hypotheses as confirmed research.
  ```

#### Rationale for Revision & Observed Differences
* **Explicit Boundary Control:** Disclaiming live internet research prevents the AI from misleading the user.
* **Separation of Evidence:** Forcing points 2 and 6 to be labeled as hypotheses ensures users validate ideas before spending marketing budget.
* **Structured Actionability:** Restricting growth recommendations to "three prioritized, actionable" items eliminates vague, overwhelming lists.

---

### Feature 2: Lead Qualification

#### Initial Prompt (Reconstructed Baseline)
* **System Prompt:**
  ```text
  You are a sales assistant. Score this lead from 1 to 100 based on fit.
  ```
* **User Prompt:**
  ```text
  Ideal Customer: [ICP details]
  Lead: [Lead details]
  How good of a fit is this customer?
  ```
* **Observed Deficiencies in Baseline:**
  * Arbitrary scoring (e.g., giving 85/100 without a clear breakdown).
  * Hallucinated positive evidence when data was missing (e.g., assuming a bakery with an old website has a huge budget).
  * Generated raw pipe characters or code blocks that failed to render as a table in the user interface.

#### Intended Lead Qualification Rubric & Specification
The intended lead qualification architecture evaluates prospective clients across five distinct, weighted categories totaling 100 points:

1. **Need Alignment (30 points maximum):**
   * Evaluates the match between the prospect's critical operational pain points (e.g., outdated or non-mobile-friendly website, lack of online ordering or automated conversion) and the solutions offered.
2. **Business Fit (30 points maximum):**
   * Assesses alignment with the Ideal Customer Profile (ICP), including core target industry sector, business model, geographic scope, and operational scale (e.g., target SMBs in India).
3. **Budget Viability (15 points maximum):**
   * Evaluates financial capacity or willingness to invest; 15 points awarded if confirmed affordable.
   * If budget information is not provided, it is intended to be marked as **"Pending discovery"** (15 points pending) rather than penalizing the lead with 0 points.
4. **Decision-Maker Access (10 points maximum):**
   * Assesses direct contact with or accessibility to the primary economic buyer, owner, or decision-maker; 10 points awarded if confirmed.
   * If decision-maker status is unknown, it is intended to be marked as **"Pending discovery"** (10 points pending).
5. **Urgency and Timeline (15 points maximum):**
   * Evaluates buying readiness, impending trigger events, or active project timelines; 15 points awarded if confirmed.
   * If timeline is unknown, it is intended to be marked as **"Pending discovery"** (15 points pending).

#### Actual Implemented Prompts in `app.py`
The prompts in `app.py` implement this qualification workflow as follows:

* **System Prompt:**
  ```text
  You are a careful B2B lead qualification assistant. Use only the supplied ideal
  customer profile and lead details. Never invent facts or treat missing information
  as positive evidence. Clearly distinguish stated evidence, assumptions, and
  missing information. Do not imply that the score is scientifically validated.
  Apply the 100-point rubric consistently across the five categories: Need Alignment
  (30), Business Fit (30), Budget Viability (15), Decision-Maker Access (10), and
  Urgency and Timeline (15). For Budget Viability, Decision-Maker Access, and
  Urgency and Timeline, distinguish unknown information from confirmed negative
  evidence: if information is unavailable, mark it as 'Pending discovery' instead
  of automatically assigning zero confirmed points or treating it as a negative
  disqualifier. Ensure strict mathematical consistency: Confirmed points plus
  Pending points must equal the total potential score. Report Confirmed Subtotal
  out of 60 (Need Alignment + Business Fit), Pending Points out of 40 (Budget
  Viability + Decision-Maker Access + Urgency and Timeline), and the Potential
  Score Range from [Confirmed Points] to [Confirmed Points + Pending Points] out
  of 100. Do not infer that a limited marketing budget means the lead cannot
  afford website development.
  ```
* **User Prompt:**
  ```text
  Ideal customer profile:
  {ideal_customer.strip()}

  Potential lead details:
  {lead_details.strip()}

  Assess the lead using this transparent 100-point rubric:
  - Need Alignment: 30 points
  - Business Fit: 30 points
  - Budget Viability: 15 points
  - Decision-Maker Access: 10 points
  - Urgency and Timeline: 15 points

  Scoring & Unknown Information Rules:
  1. Need Alignment (30 pts max) and Business Fit (30 pts max) evaluate confirmed fit evidence.
  2. For Budget Viability (15 pts max), Decision-Maker Access (10 pts max), and Urgency and Timeline (15 pts max),
  distinguish unknown information from confirmed negative evidence. When unknown or unmentioned in the lead details,
  mark status as 'Pending discovery' (e.g. 15 pts pending, 10 pts pending, 15 pts pending) rather than penalizing the lead with 0 confirmed points.
  3. Mathematical consistency: Potential score range MUST strictly be [Confirmed Points] to [Confirmed Points + Pending Points] out of 100.

  Present the 5 criteria breakdown in a clean Markdown table with columns:
  | Criterion | Max Points | Confirmed Points | Evidence | Status |
  Use standard markdown table pipes '|' without escaping them (do NOT use '\|'). Ensure a blank line before and after the table. Do not wrap the table or response in code blocks or backticks.

  After the table, clearly display:
  - Confirmed Subtotal: [Sum of confirmed points for Need Alignment and Business Fit] / 60
  - Pending Points: [Sum of pending points for Budget Viability, Decision-Maker Access, Urgency and Timeline] / 40
  - Potential Score Range: [Confirmed Points] to [Confirmed Points + Pending Points] out of 100

  Then provide:
  1. Strongest evidence of fit
  2. Missing information to confirm (pending discovery items)
  3. Recommended next step
  4. One useful discovery question
  Do not claim that the score is calculated by a validated model.
  ```

#### Scoring Behavior for Unknown Information: Implemented Architecture
* In both Feature 2 and Feature 5, missing information for budget viability, decision-maker access, or urgency is **not** assigned an arbitrary zero or treated as confirmed negative evidence.
* Instead, these categories are classified explicitly as **"Pending discovery"** (reserving up to 15 pts pending for budget, 10 pts pending for decision-maker access, and 15 pts pending for timeline).
* The evaluation reports a **Confirmed Subtotal** (points supported by explicit evidence, out of 60) separately from **Pending Discovery Points** (potential points pending discovery, out of 40), where:
  $$\text{Confirmed Points} + \text{Pending Points} = \text{Maximum Potential Score}$$
* Any reported potential score range is strictly formatted as `[Confirmed Points] to [Confirmed Points + Pending Points]` out of 100.

#### Rationale for Revision & Observed Differences
* **Transparent Mathematical Rubric:** Distributing 100 points across 5 weighted criteria (Need Alignment: 30, Business Fit: 30, Budget Viability: 15, Decision-Maker Access: 10, Urgency & Timeline: 15) prevents subjective guesswork and uncalibrated scores.
* **Pending Discovery Scoring:** When budget, decision-maker access, or timeline is omitted, the model avoids hallucinating complete customer readiness or penalizing the prospect prematurely, reserving points for sales discovery.
* **Markdown Table Formatting & Escaped Pipe Handling:** Explicitly requiring standard unescaped pipes (`|` instead of `\|`) and ensuring double newlines around tables resolved UI defects where raw backslashes and table syntax were previously rendered as plain text.
* **Actionable Discovery:** Adding item 4 ("One useful discovery question") equips sales reps with immediate follow-up questions to resolve pending criteria during discovery calls.

---

### Feature 3: Outreach Email Generator

#### Initial Prompt (Reconstructed Baseline)
* **System Prompt:**
  ```text
  You are an email copywriter. Write a sales email.
  ```
* **User Prompt:**
  ```text
  Write a sales email to [Recipient] about [Offering].
  ```
* **Observed Deficiencies in Baseline:**
  * High-pressure, pushy sales tone ("Act now for 50% off!").
  * Fabricated shared history (e.g., "I came across your profile and noticed you are struggling with...").
  * Generated multiple duplicate subject lines and repetitive sign-offs.

#### Refined & Implemented Prompts in `app.py`
* **System Prompt:**
  ```text
  You are a professional B2B copywriter. You write cold outreach emails strictly
  from the perspective of the sender (the business or service provider offering the
  solution) to the recipient (the prospective customer or lead). Never write from
  the recipient's perspective. Write concise, natural, respectful, personalized
  emails. Never invent professional experience, client history, results, testimonials,
  recipient facts, or previous conversations. Avoid unsupported generalizations,
  performance claims, guarantees, and implied results. Describe the service and its
  potential benefits without promising outcomes. Use only the information provided
  by the user and reasonable, clearly qualified suggestions. Do not imply a previous
  relationship unless explicitly stated. Use clearly marked placeholders like
  [Your Name] or [Your Company] for missing details. Return exactly one subject
  line prefixed with 'Subject: ', followed by a greeting, body, and sign-off.
  Do not repeat the subject line elsewhere.
  ```
* **User Prompt:**
  ```text
  Sender (service provider): {company} ({sender})
  Offering (what the sender provides): {offering.strip()}
  Recipient (prospective client / lead): {recipient.strip()}
  Email purpose: {purpose}
  Relevant context: {context.strip() or 'No additional context provided'}

  Task: Write one ready-to-edit cold outreach email sent FROM the sender TO the
  prospective client. Clearly articulate the sender's service and potential benefits
  without promising specific outcomes or making performance guarantees. Use only
  supplied information and qualified suggestions. Keep it concise. Never invent past
  clients, experience, or metrics. Use one polite, low-pressure call to action.
  ```

#### Rationale for Revision & Observed Differences
* **Strict Role & Perspective Disambiguation:** Distinguishing sender (agency/provider) from recipient (client/lead) prevents the AI from inverting perspectives (e.g. drafting an email as if the bakery was sending it to the agency).
* **Guarantees & Outcome Suppression:** Explicitly prohibiting ungrounded performance promises and guarantees ensures the outreach focuses on describing potential service benefits realistically rather than making unsubstantiated claims.
* **Truth in Advertising:** Prohibiting invented client testimonials or exaggerated claims keeps outreach ethical and believable.
* **Placeholder Normalization:** Using `[Your Name]` or bracketed placeholders makes drafts immediately editable.
* **Low-Pressure CTA:** Replaced aggressive sales tactics with respectful, low-friction next steps (e.g., "Are you open to a brief chat next week?").

---

### Feature 4: Marketing Content Generator

#### Initial Prompt (Reconstructed Baseline)
* **System Prompt:**
  ```text
  You are a social media manager. Write social posts.
  ```
* **User Prompt:**
  ```text
  Create social media content for {product}.
  ```
* **Observed Deficiencies in Baseline:**
  * Generic copy that ignored channel differences between LinkedIn and Instagram.
  * Injected fictitious discount codes, guarantees, and fake case studies.
  * Cluttered posts with 20+ irrelevant hashtags.

#### Refined & Implemented Prompts in `app.py`
* **System Prompt:**
  ```text
  You are an experienced digital marketing copywriter. Create useful,
  platform-appropriate content based only on information supplied by the user. Never
  invent company achievements, client results, testimonials, statistics, guarantees,
  service capabilities, discounts, free offers, or booking links. Do not imply that an
  offer exists unless the user provides it. Use clearly marked placeholders for missing
  company names or URLs. Avoid exaggerated promises, generic clichés, and unnecessary
  repetition. Clearly label each requested output section. Use platforms and marketing
  channels that are available in the specified market. Do not claim that a particular
  platform, trend, or tactic will perform well without evidence supplied by the user.
  ```
* **User Prompt:**
  ```text
  Product/service: {product.strip()}
  Platform: {platform}
  Campaign goal: {goal}
  Tone: {tone}
  Verified supporting details or offer: {company_context.strip() or 'Not provided'}

  Generate:
  1. One ready-to-edit post or email for the selected platform
  2. One headline or opening hook
  3. One call to action grounded in the supplied details; if no offer or link is provided, use a neutral CTA or placeholder
  4. Three relevant hashtags where appropriate
  5. Two alternative opening hooks
  Do not repeat the entire post in the separate CTA section.
  ```

#### Rationale for Revision & Observed Differences
* **Platform Sensitivity:** Tailors paragraph length, hashtags, and style according to whether LinkedIn, Instagram, Facebook, or Email is selected.
* **Anti-Cliché & Anti-Exaggeration:** Ensures professional credibility by avoiding marketing buzzwords ("revolutionary", "10x your revenue in 24 hours").
* **Multiple Hook Variations:** Providing alternative opening hooks gives marketers creative choices for A/B testing.

---

### Feature 5: Prompt Testing Lab

The Prompt Testing Lab demonstrates prompt engineering principles in action by executing two distinct prompt implementations side-by-side: Version 1 (Basic Prompt) and Version 2 (Improved Prompt).

#### Version 1: Basic Prompt (Baseline Architecture)
Version 1 evaluates how a standard, minimally constrained LLM prompt behaves when handling user tasks.

* **System Prompt:**
  ```text
  You are a helpful AI assistant.
  ```
* **User Prompt Construction Logic in `app.py`:**
  In `app.py`, `basic_prompt` is constructed dynamically using a keyword check:
  ```python
  if any(term in task.lower() for term in ["qualif", "lead", "prospect", "scoring", "score"]):
      basic_prompt = f"{task.strip()}\n\n{rubric_spec}"
  else:
      basic_prompt = task.strip()
  ```
  * **General Tasks:** If the user task does not contain scoring keywords (e.g. requests for market research or marketing copy), `basic_prompt` is passed directly as `{task.strip()}` with **no additional instructions, structure, or guardrails**.
  * **Lead Scoring Tasks:** When qualification or scoring terms are detected in the task, `rubric_spec` is appended to provide the evaluation criteria:
    ```text
    Lead qualification rubric (100 points total across 5 categories):
    1. Need alignment (30 points maximum):
       - 30 pts: Multiple critical needs present (outdated website, non-mobile-friendly design, AND need for online ordering/conversion).
       - 20 pts: Significant need present (outdated or non-mobile-friendly site, partial digital asset).
       - 10 pts: Minor cosmetic refresh or small content updates.
       - 0 pts: No apparent need (modern, responsive site with automated ordering already in place).
    2. Business fit (30 points maximum):
       - 30 pts: Core target SMB in India (e.g., local retail, bakery/restaurant, local professional services needing affordable web design).
       - 20 pts: Moderate fit (SMB but outside primary geographic or service scope).
       - 10 pts: Low fit (enterprise or unviable micro-entity).
       - 0 pts: Non-target business type.
    3. Budget viability (15 points maximum):
       - 15 pts if budget is confirmed affordable; mark as 'Pending discovery' (15 pts pending) if unknown.
    4. Decision-maker access (10 points maximum):
       - 10 pts if direct owner/decision-maker contact is confirmed; mark as 'Pending discovery' (10 pts pending) if unknown.
    5. Urgency and timeline (15 points maximum):
       - 15 pts if active timeline/trigger event is confirmed; mark as 'Pending discovery' (15 pts pending) if unknown.

    Rules for Unknown Information & Mathematical Consistency:
    - Unknown budget, decision-maker access, and urgency MUST be marked as 'Pending discovery' (do NOT award 0 as negative evidence).
    - Confirmed points awarded + Pending points MUST equal the maximum potential score.
    - Report the Confirmed Subtotal separately from Pending Discovery points.
    - If reporting a score range, it MUST strictly be [Confirmed Points] to [Confirmed Points + Pending Points] out of 100. Do NOT report a range such as 90–100 when confirmed points are 50/60 and pending points are 40; in that case, the maximum potential score is 50 + 40 = 90/100, so the range is strictly 50 to 90 out of 100.
    ```
* **Baseline Deficiencies of Version 1:**
  * Has no system prompt guardrails to prevent hallucinations, unverified statistics, or false agency claims.
  * Contains no wrapper instructions for objective preservation; complex multi-part prompts often suffer from dropped deliverables.
  * Despite having `rubric_spec` appended during qualification tasks, the unconstrained model frequently commits mathematical errors (e.g., reporting ranges like 90–100 when confirmed points are only 50/60) and fails to isolate confirmed subtotals.
  * Frequently hallucinates that the sender has previously audited or visited the prospect's website.

#### Version 2: Improved Prompt (Engineered Architecture)
Version 2 wraps the user task in an engineered instruction set paired with a rigorous, constraint-enforcing system prompt.

* **System Prompt:**
  ```text
  You are a rigorous, careful AI growth consultant. Thoroughly fulfill all
  objectives of the user's task while preserving its exact scope.
  Enforce strict factual, mathematical, and analytical discipline:
  1. Factual Grounding: Never present unverified local market trends, consumer behavior,
     or business adoption patterns as established facts; label them as hypotheses requiring
     validation, or use qualified, neutral wording.
  2. Agency Capability Claims: Never claim that the agency has existing clients, established relationships,
     provides responsive design, supports online ordering, integrates payment systems, or offers other
     specific services unless explicitly confirmed in the task input; use conditional language
     or clearly marked placeholders.
  3. Prospect Outreach: Never imply an actual website audit, prior inspection, or contact with a prospect;
     use neutral industry framing or audit placeholders. Keep services conditional until confirmed.
  4. Consistent Lead Scoring: Use the exact 100-point rubric across the 5 categories (Need alignment: 30,
     Business fit: 30, Budget viability: 15, Decision-maker access: 10, Urgency and timeline: 15) using explicit criteria.
  5. Mathematical Consistency: Confirmed points plus pending points must equal the maximum possible score.
     Mark unknown budget, decision-maker access, and urgency as 'Pending discovery' (never treat as negative evidence).
     Report confirmed subtotal separately from pending points. Never report mathematically contradictory ranges like 90–100 when confirmed points are 50/60 and pending points are 40;
     the maximum possible score is 50 + 40 = 90/100, so the range is 50 to 90 out of 100.
  6. Clearly distinguish suggested marketing copy from verified facts.
  ```
* **User Prompt (`improved_prompt`):**
  ```text
  Task: {task.strip()}

  Instructions for an improved response:
  1. Objective & Scope Preservation: Fulfill all three original deliverables—market research,
     lead qualification, and personalized marketing content—without altering, narrowing, or replacing
     the objectives. Address each deliverable in full with dedicated sections.
  2. Structure & Output Formatting: Organize the output with clear, dedicated headings for each
     deliverable so the response is structured, readable, and directly comparable to the basic response.
  3. Factual Grounding & Market Hypotheses: Do not present unverified local market trends, consumer
     behavior, or business adoption patterns as established facts. Clearly label them as hypotheses
     requiring validation (e.g., 'Hypothesis: ...') or use qualified, neutral wording (e.g., 'Small businesses in this sector may experience...').
     Do not invent numerical statistics, percentages, or speed benchmarks unless explicitly provided in the task or attributed to a verifiable source.
  4. Agency Capability Claims & No Implied Clients: Never claim that the agency has existing clients, established client relationships,
     provides responsive design, supports online ordering, integrates payment systems, or offers specific features unless these capabilities are
     explicitly confirmed in the task input. Use conditional language (e.g., 'If your agency offers [Service]...', 'Where applicable...') or
     clearly marked bracketed placeholders (e.g., [Insert Agency Core Services], [Insert Pricing Model], [Insert Client Case Study if confirmed]).
  5. Prospect Relationship & No Implied Audits: In outreach copy and marketing templates, never claim or imply that the sender has researched,
     followed, contacted, or inspected a prospect or their website (e.g., do NOT write 'I reviewed your website on mobile', 'I visited your site',
     or 'I noticed your menu is not mobile-friendly'). Use a neutral industry opening (addressing common operational challenges in the sector) or an
     explicit placeholder (e.g., [Insert specific audit observation if an inspection was conducted / otherwise use neutral opening]).
     Keep all marketing statements conditional until confirmed, and clearly distinguish suggested copy from verified facts.
  6. Consistent 100-Point Lead Scoring Rubric: Evaluate leads using the exact same five scoring categories, weights, and explicit criteria:
     - Need alignment (30 pts max): 30 pts for critical multiple needs (outdated, non-mobile, lacks ordering); 20 pts for significant need; 10 pts for minor updates; 0 pts for no need.
     - Business fit (30 pts max): 30 pts for core target Indian SMB; 20 pts for moderate fit; 10 pts for low fit; 0 pts for non-target.
     - Budget viability (15 pts max): 15 pts if confirmed; mark as 'Pending discovery' (15 pts pending) if unknown.
     - Decision-maker access (10 pts max): 10 pts if confirmed; mark as 'Pending discovery' (10 pts pending) if unknown.
     - Urgency and timeline (15 pts max): 15 pts if confirmed; mark as 'Pending discovery' (15 pts pending) if unknown.
     Award scores consistently based strictly on known facts. Any score variation must be justified by these stated criteria.
  7. Mathematical Consistency & Unknown Information: Unknown budget, decision-maker access, and urgency must be marked as 'Pending discovery'
     and never treated as confirmed negative evidence. Confirmed points awarded + pending points MUST equal the total potential score.
     Present a clean table separating Confirmed Subtotal (out of 60 pts) and Pending Discovery points (out of 40 pts).
     If reporting a potential score range, it MUST strictly be [Confirmed Points] to [Confirmed Points + Pending Points] out of 100.
     Never report a range like 90–100 when confirmed points are 50/60 and pending points are 40; the potential ceiling is 50 + 40 = 90/100, so the range is strictly 50 to 90 out of 100.
  8. Placeholders & Assumptions: Use clearly marked bracketed placeholders for unprovided details and clearly state all operational assumptions.
  ```

#### In-App Explanation ("What changed in the prompt?")
As rendered directly in the Streamlit interface below the side-by-side comparison:
* **Scope preservation:** Fulfills all three requested task deliverables (market research, lead qualification, marketing content) without narrowing or replacing the objectives.
* **Factual grounding:** Labels unverified local market trends, consumer behavior, and business adoption patterns as hypotheses requiring validation rather than established facts.
* **Agency capability guardrail:** Never claims existing clients, responsive design, online ordering, or payment integrations without confirmation; mandates conditional phrasing and placeholders.
* **Consistent lead scoring & explicit criteria:** Applies the exact same five categories (Need alignment: 30, Business fit: 30, Budget viability: 15, Decision-maker access: 10, Urgency & timeline: 15) with explicit criteria for consistent evaluation across both versions.
* **Mathematical consistency:** Ensures confirmed points plus pending points strictly equal total potential score; marks unknown information as 'Pending discovery' and forbids contradictory score ranges (e.g. reporting 90–100 when confirmed is 50/60 and pending is 40).

#### Side-by-Side Comparison Criteria: Actual Code vs. Output Behavior
| Evaluation Dimension | Version 1 (Basic Prompt) | Version 2 (Improved Prompt) |
|---|---|---|
| **System Persona & Constraints** | Generic: `You are a helpful AI assistant.` No constraint or negative enforcement rules. | Specialized AI Growth Consultant with 6 explicit analytical, factual, and mathematical guardrails. |
| **User Prompt Framing** | Raw user task `{task.strip()}`. (Conditionally appends `rubric_spec` only if lead scoring keywords are detected; no wrapper otherwise). | Always wraps task in 8 numbered instructions enforcing structure, grounding, safety, and rubric compliance. |
| **Deliverable Scope & Organization** | Prone to scope narrowing, dropping secondary deliverables, or producing unstructured bullet walls. | Explicitly requires dedicated sections preserving all requested deliverables without dropping scope. |
| **Factual Grounding & Market Claims** | Often hallucinates specific market statistics, adoption numbers, and consumer trends as verified facts. | Strictly mandates labeling unverified trends as hypotheses (`Hypothesis: ...`) or using qualified neutral phrasing. |
| **Agency Capabilities & Credentials** | Prone to inventing agency features (e.g. responsive design, payment gateways, mobile menus) and past clients. | Prohibits unconfirmed service claims; mandates conditional phrasing ("If your agency offers...") and bracketed placeholders. |
| **Prospect Outreach Claims** | Commonly fabricates prior contact or website inspections (e.g. "I reviewed your mobile website"). | Strictly forbids claiming prior visits or audits; mandates neutral industry openings or explicit audit placeholders. |
| **Lead Scoring Rubric Application** | Has rubric text appended only if scoring terms match; lacks instruction wrapper and often ignores point tier rules. | Rigorously enforces the exact 5-category rubric (Need: 30, Fit: 30, Budget: 15, Decision-Maker: 10, Urgency: 15) with explicit point tiers. |
| **Mathematical Consistency** | Prone to contradictory score reporting (e.g., claiming 90–100 range when confirmed points are only 50/60 and pending is 40). | Mathematically enforced: Confirmed points + Pending points must strictly equal maximum potential score; range is strictly `[Confirmed] to [Confirmed + Pending]`. |
| **Handling Unknown Information** | May penalize missing data with 0 points or guess values without separating verified evidence from unknowns. | Mandates marking unknown budget, decision-maker, and urgency as 'Pending discovery'; isolates Confirmed Subtotal (out of 60) from Pending Points (out of 40). |

---

## 3. Development, Connection & Debugging Prompts

During setup and verification, connection tests and diagnostic scripts were used to validate the model API connection and verify environment configuration:

### Google Gemini API Health Check Prompt (`test_gemini.py`)
* **System Prompt:**
  ```text
  You are a helpful AI business assistant. Give clear and concise answers.
  ```
* **User Prompt:**
  ```text
  In two sentences, explain how AI can help a small business identify potential customers.
  ```
* **Outcome:** Validates Google GenAI SDK authentication, model response latency, and exception handling without token waste.

### Model Availability & Fallback Architecture
From the source code implementation in `llm.py`:
* **Environment Configuration:**
  * The application loads `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) and `GEMINI_MODEL` dynamically from `.env` using `load_dotenv(override=True)`.
  * The primary configured model defaults to `gemini-3.5-flash` if `GEMINI_MODEL` is not explicitly defined in the environment.
* **Fallback Logic in `llm.py`:**
  * When `client.models.generate_content` raises an exception during execution with the primary model, `llm.py` automatically initiates a fallback:
    ```python
    except Exception as err:
        fallback_model = "gemini-3.1-flash-lite"
        if model != fallback_model:
            response = client.models.generate_content(
                model=fallback_model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )
        else:
            raise err
    ```
  * If the primary model fails and is not already `gemini-3.1-flash-lite`, the request is retried against `gemini-3.1-flash-lite`.
  * If the fallback model also fails or was the primary model, the exception is raised to the caller.
* **Error Presentation in `app.py`:**
  * In `app.py`, exceptions are caught by `run_ai()`, which renders a user-friendly error banner (`The AI request failed. Check your internet connection, Gemini API key, model availability, and account limits.`) alongside a technical caption (`st.caption(f"Technical details: {error}")`) while strictly preventing secret API keys from being exposed.

---

## 4. Implementation Status & Verification

All core requirements and targeted corrections have been verified against the active codebase:

1. **Feature 2 Lead Qualification Rubric & Unknown Information:**
   * **Five Categories Implemented in `app.py`:** Evaluates (1) Need Alignment: 30, (2) Business Fit: 30, (3) Budget Viability: 15, (4) Decision-Maker Access: 10, and (5) Urgency and Timeline: 15. The former Location/Service-Area Fit criterion has been replaced by Decision-Maker Access.
   * **Pending Discovery Architecture:** For Budget Viability, Decision-Maker Access, and Urgency & Timeline, unknown information is distinguished from confirmed negative evidence and designated as "Pending discovery" (reserving 15, 10, and 15 points respectively).
   * **Mathematical Consistency:** The output displays Confirmed Subtotal (/60), Pending Points (/40), and Potential Score Range (`[Confirmed Points] to [Confirmed Points + Pending Points]` out of 100), ensuring confirmed + pending strictly equal the potential maximum score.
2. **Feature 5 Prompt Testing Lab Alignment:**
   * Feature 5 shares the identical 5-category rubric specification and pending discovery framework across both basic and improved prompts when lead scoring tasks are tested.
3. **Diagnostic Scripts:**
   * `test_gemini.py` and `test_openrouter.py` accurately reflect that the Google Gemini API (`genai.Client`) is the underlying LLM provider, providing consistent diagnostic feedback.

