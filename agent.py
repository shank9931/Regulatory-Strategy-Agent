from google.adk.agents import Agent
from .tools import search_guidelines
from .orchestrator import create_regulatory_pipeline

# ==========================================
# 1. PLANNER AGENT
# ==========================================
# Identifies what we need to look for based on the product description.
planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.5-flash",
    description="Identifies regulatory uncertainty areas.",
    output_key="plan_output",
    instruction=(
        "You are a Regulatory Strategy Planner.\n"
        "Your Goal: Given a product description, identify key regulatory uncertainty areas "
        "(e.g., clinical, quality, classification, labeling).\n"
        "Output: A concise plan listing the specific 'uncertainty_areas' and "
        "'suggested_lifecycle_stages' to investigate."
    )
)

# ==========================================
# 2. RETRIEVER AGENT
# ==========================================
# Dedicated to using the tool. It receives the Plan and calls the search.
retriever_agent = Agent(
    name="retriever_agent",
    model="gemini-2.5-flash",
    description="Fetches guidelines using search tools.",
    tools=[search_guidelines],
    output_key="retrieved_docs",
       instruction=(
        "You are a strict Retrieval Engine. You are NOT a chat assistant.\n"
        "You have NO internal knowledge. You CANNOT answer questions directly.\n"
        "Input Plan: {plan_output}\n\n"
        "MANDATORY EXECUTION PROTOCOL:\n"
        "1. You MUST call the tool `search_guidelines` using keywords from the Input Plan.\n"
        "2. If you do not call the tool, the workflow fails.\n"
        "3. Once the tool returns data, simply output that raw data as your final answer.\n"
        "4. DO NOT summarize. DO NOT say 'I found this'. Just output the content."
    )
)

# ==========================================
# 3. ANALYZER AGENT
# ==========================================
# Takes the retrieved guidelines and assigns probabilities.
analyzer_agent = Agent(
    name="analyzer_agent",
    model="gemini-2.5-flash",
    description="Assigns applicability probabilities.",
    output_key="analysis_draft",
    instruction=(
        "You are a Regulatory Intelligence Analyst.\n"
        "Context: You will receive a history containing a Product Description, a Plan, "
        "and a set of Retrieved Guidelines.\n"
        "Input Guidelines: {retrieved_docs}\n\n"
        "Task: For EACH guideline found in the context:\n"
        "1. Estimate applicability probability (0.0 to 1.0).\n"
        "2. Provide short reasoning based on 'Applies if' criteria.\n"
        "3. List uncertainty factors.\n"
        "Output: A structured analysis draft."
    )
)

# ==========================================
# 4. CRITIC AGENT
# ==========================================
# Reviews the work for overconfidence.
critic_agent = Agent(
    name="critic_agent",
    model="gemini-2.5-flash",
    description="Reviews analysis for overconfidence.",
    output_key="final_strategy",
    instruction=(
        "You are a Critical Regulatory Reviewer.\n"
        "Input Analysis: {analysis_draft}\n\n"
        "Task: Review the previous analysis for overconfident probabilities (>0.8) "
        "that lack strong justification.\n"
        "Action: If you find issues, propose revised probabilities. If the analysis is sound, "
        "endorse it.\n"
        "Final Output: Present the final, verified Regulatory Strategy to the user."
    )
)

# ==========================================
# ROOT AGENT
# ==========================================
# This is the entry point that ADK Web will load.
root_agent = create_regulatory_pipeline(
    planner=planner_agent,
    retriever=retriever_agent,
    analyzer=analyzer_agent,
    critic=critic_agent
)