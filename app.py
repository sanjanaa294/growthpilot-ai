import re
import streamlit as st
from llm import generate_text


# -----------------------------
# Page setup and shared helpers
# -----------------------------
st.set_page_config(
    page_title="GrowthPilot AI",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 GrowthPilot AI")
st.subheader("Your AI-powered business growth assistant")
st.write(
    "Research your market, qualify potential customers, "
    "and create personalized marketing content using AI."
)

st.sidebar.title("GrowthPilot AI")
feature = st.sidebar.selectbox(
    "Choose a tool",
    [
        "Business Research",
        "Lead Qualification",
        "Email Generator",
        "Marketing Content",
        "Prompt Testing Lab",
    ],
)
st.sidebar.info(
    "GrowthPilot AI turns business information into practical "
    "growth ideas. AI-generated recommendations should be reviewed "
    "before use."
)


def clean_escaped_pipes(text: str) -> str:
    """
    Unescape escaped pipe characters (\\|) outside inline code spans (`...`).
    Preserves inline code and normal text.
    """
    lines = text.splitlines()
    processed_lines = []

    for line in lines:
        if r"\|" in line:
            # Split by inline code spans `...`
            parts = re.split(r"(`[^`]+`)", line)
            new_parts = []
            for part in parts:
                if part.startswith("`") and part.endswith("`") and len(part) >= 2:
                    new_parts.append(part)
                else:
                    new_parts.append(part.replace(r"\|", "|"))
            line = "".join(new_parts)

        processed_lines.append(line)

    return "\n".join(processed_lines)


def format_ai_markdown(result: str) -> str:
    """Format and clean markdown so tables and sections render properly in Streamlit."""
    if not result:
        return result

    cleaned = result.strip()

    # Unwrap if the entire output was accidentally enclosed in markdown code fences
    if (
        cleaned.startswith("```markdown")
        or cleaned.startswith("```md")
        or cleaned.startswith("```")
    ) and cleaned.endswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()

    # 1. Unescape any escaped pipe characters (\|) outside inline code
    cleaned = clean_escaped_pipes(cleaned)

    # 2. Unwrap any table accidentally enclosed in code fences like ```markdown\n| ... |\n```
    table_fence_pattern = (
        r"```(?:markdown|md)?\s*?\n"
        r"((?:\|[^\n]+\|\s*?\n)+)"
        r"```"
    )
    cleaned = re.sub(table_fence_pattern, r"\n\1\n", cleaned)

    # 3. Ensure a blank line before any markdown table header row if preceded by non-newline
    cleaned = re.sub(
        r"([^\n])\n(\|[^\n]+\|\s*?\n\|[-: |]+\|)",
        r"\1\n\n\2",
        cleaned,
    )

    # 4. Ensure a blank line after any markdown table if followed immediately by non-table text
    cleaned = re.sub(
        r"(\|[^\n]+\|)\n([^\n|])",
        r"\1\n\n\2",
        cleaned,
    )

    # 5. Normalize excessive newlines
    cleaned = re.sub(r"\n{3,}", r"\n\n", cleaned)

    return cleaned


def show_ai_result(result: str):
    if not result or not result.strip():
        st.warning("No result was generated. Please try again.")
        return

    st.markdown(format_ai_markdown(result))


def run_ai(system_prompt: str, user_prompt: str) -> str | None:
    """Call the shared LLM helper and show a user-friendly error."""
    try:
        return generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
    except Exception as error:
        st.error(
            "The AI request failed. Check your internet connection, "
            "OpenRouter API key, model availability, and account limits."
        )
        # The details are useful while developing; they do not reveal the API key.
        st.caption(f"Technical details: {error}")
        return None


st.divider()


# -----------------------------
# 1. Business Research
# -----------------------------
if feature == "Business Research":
    st.header("🔎 AI Business Research")
    st.write(
        "Explore potential customer needs and practical growth ideas. "
        "This tool does not perform live web research."
    )

    business = st.text_input(
        "Business name or description",
        placeholder="Example: An online clothing store selling affordable outfits",
    )
    audience = st.text_input(
        "Target audience",
        placeholder="Example: College students in India aged 18–25",
    )
    market_context = st.text_area(
        "Additional context (optional)",
        placeholder="Add location, price range, competitors, or known challenges.",
    )

    if st.button("Research Business", type="primary"):
        if business.strip() and audience.strip():
            with st.spinner("Analyzing your business..."):
                result = run_ai(
                    system_prompt=(
                        "You are a careful business strategy assistant. "
                        "Use only the information supplied by the user and general "
                        "reasoning. Do not claim to have searched the internet or "
                        "verified current market data. Never invent statistics, "
                        "competitor facts, customer research, or business results. "
                        "Separate user-provided facts, reasonable hypotheses, and "
                        "items that need validation. Give practical, prioritized "
                        "recommendations with clear headings. Distinguish user-provided "
                        "facts from assumptions and hypotheses. Do not present general "
                        "market assumptions as verified research findings. Recommend "
                        "marketing channels that are available in the specified market. "
                        "Label numerical budgets, targets, and ranges as illustrative "
                        "unless supported by supplied data or reliable sources. Do not "
                        "claim to have conducted live research or verified competitor "
                        "data unless those capabilities were actually used. Prioritize "
                        "practical recommendations and suggest ways to validate them."
                    ),
                    user_prompt=(
                        f"Business: {business.strip()}\n"
                        f"Target audience: {audience.strip()}\n"
                        f"Additional context: {market_context.strip() or 'Not provided'}\n\n"
                        "Prepare:\n"
                        "1. Short business overview\n"
                        "2. Likely customer needs (label these as hypotheses)\n"
                        "3. Potential customer segments\n"
                        "4. Marketing opportunities\n"
                        "5. Three prioritized, actionable growth recommendations\n"
                        "6. Assumptions and questions to validate before spending money\n"
                        "Do not present hypotheses as confirmed research."
                    ),
                )
            if result:
                st.subheader("Research Results")
                show_ai_result(result)
        else:
            st.warning("Please enter the business description and target audience.")


# -----------------------------
# 2. Lead Qualification
# -----------------------------
elif feature == "Lead Qualification":
    st.header("🎯 AI Lead Qualification")
    st.write(
        "Estimate how closely a potential customer matches your ideal customer "
        "profile. The score is an AI-assisted estimate, not a verified prediction."
    )

    ideal_customer = st.text_area(
        "Describe your ideal customer",
        placeholder=(
            "Example: Small businesses that need affordable, modern websites "
            "and want to generate online enquiries."
        ),
    )
    lead_details = st.text_area(
        "Enter potential customer details",
        placeholder=(
            "Example: A local bakery has an outdated website and wants to accept "
            "online orders, but has a limited marketing budget."
        ),
    )

    if st.button("Qualify Lead", type="primary"):
        if ideal_customer.strip() and lead_details.strip():
            with st.spinner("Evaluating lead against the profile..."):
                result = run_ai(
                    system_prompt=(
                        "You are a careful B2B lead qualification assistant. "
                        "Use only the supplied ideal customer profile and lead "
                        "details. Never invent facts or treat missing information "
                        "as positive evidence. Be conservative when information is "
                        "unknown. Clearly distinguish stated evidence, assumptions, "
                        "and missing information. Do not imply that the score is "
                        "scientifically validated. Apply the rubric consistently: "
                        "the points awarded across the five criteria must add up to "
                        "the final score and must not exceed each criterion's maximum. "
                        "If a criterion is unknown, award only the points supported "
                        "by available evidence and explain the uncertainty. Do not "
                        "infer that a limited marketing budget means the lead cannot "
                        "afford website development."
                    ),
                    user_prompt=(
                        f"Ideal customer profile:\n{ideal_customer.strip()}\n\n"
                        f"Potential lead details:\n{lead_details.strip()}\n\n"
                        "Assess the lead using this transparent 100-point rubric:\n"
                        "- Business/customer type match: 30 points\n"
                        "- Match between stated need and the offered solution/profile: 30 points\n"
                        "- Budget fit: 15 points\n"
                        "- Location or service-area fit: 10 points\n"
                        "- Buying readiness or urgency: 15 points\n\n"
                        "Present the 5 criteria breakdown in a clean Markdown table with columns:\n"
                        "| Criterion | Max Points | Awarded Points | Evidence | Unknown/Unverified |\n"
                        "Use standard markdown table pipes '|' without escaping them (do NOT use '\\|'). "
                        "Ensure a blank line before and after the table. Do not wrap the table or response in code blocks or backticks.\n\n"
                        "For each criterion, show the maximum points, awarded points, "
                        "evidence from the input, and whether the criterion is unknown. "
                        "Do not award full points for unknown information; use a "
                        "conservative score and mark it as unverified. Explain the "
                        "total score and its limitations. Then provide:\n"
                        "1. Overall fit score out of 100\n"
                        "2. Strongest evidence of fit\n"
                        "3. Missing information to confirm\n"
                        "4. Recommended next step\n"
                        "5. One useful discovery question\n"
                        "Do not claim that the score is calculated by a validated model."
                    ),
                )
            if result:
                st.subheader("Lead Assessment")
                show_ai_result(result)
        else:
            st.warning("Please complete both fields.")


# -----------------------------
# 3. Email Generator
# -----------------------------
elif feature == "Email Generator":
    st.header("✉️ Personalized Outreach Email")
    st.write(
        "Create an editable email without inventing sender experience or recipient facts."
    )

    recipient = st.text_input(
        "Recipient or business type",
        placeholder="Example: Owner of a local bakery",
    )
    offering = st.text_input(
        "Product or service you offer",
        placeholder="Example: Affordable website design with online ordering",
    )
    purpose = st.selectbox(
        "Email purpose",
        ["Introduction", "Sales Outreach", "Follow-up", "Meeting Request"],
    )
    context = st.text_area(
        "Relevant context",
        placeholder=(
            "Include genuine details about the recipient, offer, prior contact, "
            "or desired next step. Do not include confidential information."
        ),
    )
    sender_name = st.text_input("Your name (optional)")
    company_name = st.text_input("Your company (optional)")

    if st.button("Generate Email", type="primary"):
        if recipient.strip() and offering.strip():
            sender = sender_name.strip() or "[Your Name]"
            company = company_name.strip() or "[Your Company]"
            with st.spinner("Writing personalized email..."):
                result = run_ai(
                    system_prompt=(
                        "You are a professional B2B copywriter. You write cold outreach "
                        "emails strictly from the perspective of the sender (the business or "
                        "service provider offering the solution) to the recipient (the prospective "
                        "customer or lead). Never write from the recipient's perspective. Write concise, "
                        "natural, respectful, personalized emails. Never invent professional experience, "
                        "client history, results, testimonials, recipient facts, or previous conversations. "
                        "Avoid unsupported generalizations, performance claims, guarantees, and implied "
                        "results. Describe the service and its potential benefits without promising outcomes. "
                        "Use only the information provided by the user and reasonable, clearly qualified "
                        "suggestions. Do not imply a previous relationship unless explicitly stated. Use "
                        "clearly marked placeholders like [Your Name] or [Your Company] for missing details. "
                        "Return exactly one subject line prefixed with 'Subject: ', followed by a greeting, "
                        "body, and sign-off. Do not repeat the subject line elsewhere."
                    ),
                    user_prompt=(
                        f"Sender (service provider): {company} ({sender})\n"
                        f"Offering (what the sender provides): {offering.strip()}\n"
                        f"Recipient (prospective client / lead): {recipient.strip()}\n"
                        f"Email purpose: {purpose}\n"
                        f"Relevant context: {context.strip() or 'No additional context provided'}\n\n"
                        "Task: Write one ready-to-edit cold outreach email sent FROM the sender "
                        "TO the prospective client. Clearly articulate the sender's service and potential "
                        "benefits without promising specific outcomes or making performance guarantees. "
                        "Use only supplied information and qualified suggestions. Keep it concise. "
                        "Never invent past clients, experience, or metrics. Use one polite, low-pressure "
                        "call to action."
                    ),
                )
            if result:
                st.subheader("Generated Email")
                show_ai_result(result)
        else:
            st.warning("Please enter the recipient and your offering.")


# -----------------------------
# 4. Marketing Content
# -----------------------------
elif feature == "Marketing Content":
    st.header("📣 AI Marketing Content Generator")
    st.write(
        "Generate draft content for a selected platform and campaign goal. "
        "Review claims and placeholders before publishing."
    )

    product = st.text_input(
        "Product or service",
        placeholder="Example: Affordable website design for small businesses",
    )
    platform = st.selectbox(
        "Content platform",
        ["Instagram", "LinkedIn", "Facebook", "Email Campaign"],
    )
    goal = st.selectbox(
        "Campaign goal",
        ["Brand Awareness", "Lead Generation", "Engagement", "Sales"],
    )
    tone = st.selectbox(
        "Writing tone",
        ["Professional", "Friendly", "Creative", "Persuasive"],
    )
    company_context = st.text_area(
        "Supporting details or offer (optional)",
        placeholder=(
            "Add verified features, target audience, actual offer, website link, "
            "or CTA. Leave blank if these details are not available."
        ),
    )

    if st.button("Generate Content", type="primary"):
        if product.strip():
            with st.spinner("Creating marketing content..."):
                result = run_ai(
                    system_prompt=(
                        "You are an experienced digital marketing copywriter. "
                        "Create useful, platform-appropriate content based only "
                        "on information supplied by the user. Never invent company "
                        "achievements, client results, testimonials, statistics, "
                        "guarantees, service capabilities, discounts, free offers, "
                        "or booking links. Do not imply that an offer exists unless "
                        "the user provides it. Use clearly marked placeholders for "
                        "missing company names or URLs. Avoid exaggerated promises, "
                        "generic clichés, and unnecessary repetition. Clearly label "
                        "each requested output section. Use platforms and marketing "
                        "channels that are available in the specified market. Do not "
                        "claim that a particular platform, trend, or tactic will "
                        "perform well without evidence supplied by the user."
                    ),
                    user_prompt=(
                        f"Product/service: {product.strip()}\n"
                        f"Platform: {platform}\n"
                        f"Campaign goal: {goal}\n"
                        f"Tone: {tone}\n"
                        f"Verified supporting details or offer: "
                        f"{company_context.strip() or 'Not provided'}\n\n"
                        "Generate:\n"
                        "1. One ready-to-edit post or email for the selected platform\n"
                        "2. One headline or opening hook\n"
                        "3. One call to action grounded in the supplied details; "
                        "if no offer or link is provided, use a neutral CTA or placeholder\n"
                        "4. Three relevant hashtags where appropriate\n"
                        "5. Two alternative opening hooks\n"
                        "Do not repeat the entire post in the separate CTA section."
                    ),
                )
            if result:
                st.subheader("Your Marketing Content")
                show_ai_result(result)
        else:
            st.warning("Please enter a product or service.")


# -----------------------------
# 5. Prompt Testing Lab
# -----------------------------
elif feature == "Prompt Testing Lab":
    st.header("🧪 Prompt Testing & Optimization Lab")
    st.write(
        "Compare a simple prompt with a more detailed prompt. This is a side-by-side "
        "experiment; it does not automatically prove which answer is better."
    )

    task = st.text_area(
        "Task for the AI",
        placeholder=(
            "Example: Write a LinkedIn post promoting affordable website design "
            "for small businesses. The goal is lead generation."
        ),
    )

    if st.button("Compare Prompts", type="primary"):
        if task.strip():
            basic_prompt = task.strip()
            improved_prompt = (
                f"Task: {task.strip()}\n\n"
                "Instructions for an improved response:\n"
                "1. Objective & Scope Preservation: Fulfill all components and intended deliverables of the original task without altering, narrowing, or replacing the objective. If the task asks for multiple deliverables (such as market research, lead qualification, and marketing content), address each one in full.\n"
                "2. Structure & Output Formatting: Organize the output with clear, dedicated headings for each part of the task so the response is structured, readable, and directly comparable to the basic response.\n"
                "3. Specificity & Context: Provide clear, practical, and actionable steps rather than generic generalizations.\n"
                "4. Factual Grounding & Constraints: Rely strictly on information provided in the task and sound general reasoning. Never invent company metrics, audience demographics, customer results, statistics, guarantees, or testimonials.\n"
                "5. Hypotheses vs. Stated Facts: Clearly distinguish stated facts from assumptions, hypotheses, or suggestions that require real-world validation.\n"
                "6. Placeholders: Use bracketed placeholders (such as [Business Name] or [Target Audience]) only for essential details not supplied in the task."
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Version 1: Basic Prompt")
                with st.spinner("Testing basic prompt..."):
                    basic_result = run_ai(
                        system_prompt="You are a helpful AI assistant.",
                        user_prompt=basic_prompt,
                    )
                if basic_result:
                    show_ai_result(basic_result)

            with col2:
                st.subheader("Version 2: Improved Prompt")
                with st.spinner("Testing improved prompt..."):
                    improved_result = run_ai(
                        system_prompt=(
                            "You are a rigorous, careful AI assistant. Thoroughly fulfill all "
                            "objectives of the user's task while preserving its exact scope. "
                            "Provide clear structure, actionable detail, and strong factual discipline "
                            "without inventing unprovided data or making unsupported claims."
                        ),
                        user_prompt=improved_prompt,
                    )
                if improved_result:
                    show_ai_result(improved_result)

            st.divider()
            st.subheader("What changed in the prompt?")
            st.markdown(
                "- **Scope preservation:** explicitly instructs the AI to fulfill all requested task deliverables without narrowing or altering the objective.\n"
                "- **Structure & formatting:** organizes output into dedicated, readable sections for each part of the task.\n"
                "- **Factual constraints:** strictly prohibits invented metrics, testimonials, or guarantees, and flags hypotheses for validation.\n"
                "- **Actionability & placeholders:** replaces vague generalities with specific steps and uses clear bracketed placeholders for missing details."
            )
            st.caption(
                "Compare both outputs for factual reliability, relevance, clarity, "
                "format, and usefulness. The improved prompt is a hypothesis to test, "
                "not a guaranteed improvement."
            )
        else:
            st.warning("Please describe the task you want to test.")


st.divider()
st.caption(
    "GrowthPilot AI | AI-assisted business growth and marketing | "
    "Review AI-generated content before using it in real business decisions."
)
