# GrowthPilot AI — Prompt Engineering Documentation

## 1. Overview & Methodology

GrowthPilot AI is an AI-powered business growth assistant developed for the Technology and Small Business domain. It assists small business owners, freelancers, and growth consultants across five key operational workflows:

1. **Business Research:** Analyzing target markets, customer segments, and strategic hypotheses without claiming unverified web research.
2. **Lead Qualification:** Objectively assessing prospect fit using a transparent 100-point rubric and structured Markdown tables.
3. **Outreach Email Generation:** Drafting personalized, professional B2B outreach without fabricating relationship history or company claims.
4. **Marketing Content Generation:** Producing multi-channel marketing copy tailored to platform, tone, and campaign goals without making false promises.
5. **Prompt Testing Lab:** Demonstrating side-by-side iterative prompt optimization to evaluate AI responses against clear evaluation criteria.

### Prompt Engineering Principles Applied
* **Groundedness & Constraint Enforcement:** AI models tend to hallucinate customer statistics, past business relationships, or search claims. System prompts strictly prohibit fabricating client history, metrics, or live web browsing capabilities.
* **Separation of Facts vs. Hypotheses:** Prompts explicitly require labeling unverified customer assumptions as hypotheses requiring real-world validation.
* **Rubric Transparency & Mathematical Consistency:** Lead qualification uses an explicit 100-point scoring model across 5 fixed criteria with explicit instructions to avoid inflating scores for missing data.
* **Deterministic Structural Formatting:** Prompts dictate exact output structures (headings, lists, Markdown tables with blank line isolation) to prevent rendering defects in user interfaces.

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

#### Refined & Implemented Prompts in `app.py`
* **System Prompt:**
  ```text
  You are a careful B2B lead qualification assistant. Use only the supplied ideal
  customer profile and lead details. Never invent facts or treat missing information
  as positive evidence. Be conservative when information is unknown. Clearly
  distinguish stated evidence, assumptions, and missing information. Do not imply
  that the score is scientifically validated. Apply the rubric consistently: the
  points awarded across the five criteria must add up to the final score and must
  not exceed each criterion's maximum. If a criterion is unknown, award only the
  points supported by available evidence and explain the uncertainty. Do not infer
  that a limited marketing budget means the lead cannot afford website development.
  ```
* **User Prompt:**
  ```text
  Ideal customer profile:
  {ideal_customer.strip()}

  Potential lead details:
  {lead_details.strip()}

  Assess the lead using this transparent 100-point rubric:
  - Business/customer type match: 30 points
  - Match between stated need and the offered solution/profile: 30 points
  - Budget fit: 15 points
  - Location or service-area fit: 10 points
  - Buying readiness or urgency: 15 points

  Present the 5 criteria breakdown in a clean Markdown table with columns:
  | Criterion | Max Points | Awarded Points | Evidence | Unknown/Unverified |
  Use standard markdown table pipes '|' without escaping them (do NOT use '\|'). Ensure a blank line before and after the table. Do not wrap the table or response in code blocks or backticks.

  For each criterion, show the maximum points, awarded points, evidence from the input,
  and whether the criterion is unknown. Do not award full points for unknown information;
  use a conservative score and mark it as unverified. Explain the total score and its
  limitations. Then provide:
  1. Overall fit score out of 100
  2. Strongest evidence of fit
  3. Missing information to confirm
  4. Recommended next step
  5. One useful discovery question
  Do not claim that the score is calculated by a validated model.
  ```

#### Rationale for Revision & Observed Differences
* **Transparent Mathematical Rubric:** Distributing 100 points across 5 weighted criteria prevents subjective guesswork.
* **Conservative Unknown Scoring:** When budget or timeline is omitted, the model awards 0–5 points rather than guessing full points.
* **Markdown Table Formatting & Escaped Pipe Handling:** Explicitly requiring standard unescaped pipes (`|` instead of `\|`) and ensuring double newlines around tables resolved the UI defect where raw backslashes and table syntax were previously rendered.
* **Actionable Discovery:** Adding item 5 ("One useful discovery question") equips sales teams with immediate follow-up utility.

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

The Prompt Testing Lab allows users to see prompt engineering principles in action by comparing a naive user prompt against an engineered prompt side-by-side.

#### Version 1: Basic Prompt
* **System Prompt:**
  ```text
  You are a helpful AI assistant.
  ```
* **User Prompt:**
  ```text
  {task.strip()}
  ```

#### Version 2: Improved Prompt
* **System Prompt:**
  ```text
  You are a careful assistant. Follow the supplied requirements, avoid
  unsupported claims, and be clear about uncertainty.
  ```
* **User Prompt:**
  ```text
  Task: {task.strip()}

  Requirements:
  - Identify the intended audience using only information in the task.
  - Follow the requested format, platform, and goal.
  - Use clear, specific, actionable language.
  - Never invent company achievements, customer results, statistics, testimonials, offers, guarantees, or service capabilities.
  - Do not present assumptions about the audience as confirmed facts.
  - Use placeholders only for details essential to the task that have not been provided.
  - Avoid unnecessary placeholders and repetitive content.
  - Make the output practical and easy to edit before use.
  - Briefly identify important information that should be verified before publishing.
  ```

#### Side-by-Side Comparison Criteria
| Evaluation Dimension | Version 1 (Basic Prompt) | Version 2 (Improved Prompt) |
|---|---|---|
| **Factual Reliability** | High risk of hallucinated stats & fake guarantees | Strictly bounded to input data |
| **Actionability** | Often vague and broad | Specific, structured, ready to execute |
| **Audience Alignment** | Assumes generic audience | Directly tailored to supplied constraints |
| **Verification Guidance** | No disclaimers or validation cues | Identifies assumptions requiring verification |
| **Format Consistency** | Freeform output | Structured sections with clean formatting |

---

## 3. Development, Connection & Debugging Prompts

During setup and verification, connection tests and diagnostic scripts were used to validate the OpenRouter API:

### OpenRouter Health Check Prompt (`test_openrouter.py`)
* **System Prompt:**
  ```text
  You are a helpful AI business assistant. Give clear and concise answers.
  ```
* **User Prompt:**
  ```text
  In two sentences, explain how AI can help a small business identify potential customers.
  ```
* **Outcome:** Confirmed API authentication, model response handling, and latency.

### Rate Limiting & Model Fallback Handling
* When upstream providers encounter temporary rate limits (such as HTTP 429), the LLM client properly captures error details:
  * Application displays a user-friendly error in the Streamlit UI.
  * Technical error strings are surfaced cleanly in captions without leaking secret API tokens.
