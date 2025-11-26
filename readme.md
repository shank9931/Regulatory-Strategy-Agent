# Regulatory Strategy Agents
### Automating Medical Device Regulatory Intelligence with Google ADK

Competition Track: Enterprise Agents \
Model: Gemini 2.5 Flash \
Framework: Google Agent Development Kit (ADK)

## The Pitch
### Problem
Bringing a new medical device to market requires navigating a labyrinth of complex, region-specific regulations. Regulatory professionals spend hunderds of hours searching for guidelines, assessing applicability, and double-checking their work. Missed regulations can lead to costly delays or rejections.

### Solution
The Regulatory Strategy Agents is a multi agent AI pipeline designed to automate the initial phase of regulatory scopig. Instead of a generic chat, it employs a strict, 4 step "assembly line" to:

1. Plan the research strategy based on the device description.
2. Retrieve actual regulatory texts using specialized toosl.
3. Analyze the applicability of each regulation with probabilistic scoring.
4. Critique the findings to prevent AI hallucinations and overconfidence.

### Value
* Consistency - Eliminates initial human error in initial scoping
* Speed - Reduces days of reasearch into minutes of processing
* Traceability - Every step is logged and auditable via the ADK trace view

## Architecture
This project uses a Sequential workflow pattern orchestrated by a director agent. Unlike a chatty bot, this system enforces a strict chain of custody of data.

### Agent workflow
The pipeline consists of four specialized agents working in series:
1. Planner agent:
    * Role: Strategy formulation
    * Action: Deconstructs the user's product description (e.g., "AI pacemaker") into specific regulatory search terms and lifecycle stages.

2. Retriever Agent (The tool user):
    * Role: Data fetcher
    * Action: Strictly madated to use the *search_guidelines* tool. It cannot answer from its own training data; it must fetch external context.

3. Analyzer Agent:
    * Role: Probability scorer
    * Action: Reads the raw retrieved documents and assigns an "Applicability Score" (0.0 - 1.0) with justification.

4. Critc Agent:
    * Role: Quality Assurance
    * Action: Reviews the analysis for overconfidence (>0.8 score without strong evidence) and creates the final report.

## Technical Implementation
1. Multi Agent Systems (Sequential): Implemented in `orchestrator.py` using a director agent pattern that routes work through sub-agents via *output_key* context chaining.
2. Custom Tools: A python based *search_guidelines* tool in `tools.py` that performs keyword/region scoring on a local regulatory database.
3. Deployment: The tool has been implemented using `adk deploy cloud_run` to Google Cloud Run. You can access the build at `https://regulatoryintelagent-164343554530.us-central1.run.app`

### File Structure
* `agents.py`: Definitions of the 4 agents and their strict system instructions
* `orchestrator.py`: Logic that wires the agents into a sequential pipeline.
* `tools.py`: The search engine logic and JSON database loader
* `guidelines.json`: The tiny database with medical device guideline mapping (dummy data mimicking real guidelines)

## Setup & Usage
### Prerequisites
* Python 3.10+
* A Google Cloud Project with a Gemini API key (Google Studio)

### Installation
1. Clone this repository.
2. Install the dependencies: `pip install google-adk`
3. Set your API key either in the terminal when prompted or by `echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env`

### Running the agent
* Option 1: The Visual Web UI (Recommended for Debugging): This launches the ADK developer UI where you can see the "Trace" of the 4 step process. \
Run from the parent directory: `adk web --port 8000 --log_level debug`

* Option 2: The Command Line Tool: `adk run my_agent`


## Example Output
Input: "Help me file for my AI based diagnostic software for radiologists" 

Final Strategy (Critic Output):

Final Verified Regulatory Strategy:

Based on the analysis, here are the applicable guidelines and their verified probabilities:

Guideline: ICH Q9(R1) – Quality Risk Management (Global)
Applicability Probability: 0.9
Reasoning: Quality Risk Management (QRM) is a foundational principle for medical devices, including software. While not explicitly named by the planner, it is critical for addressing uncertainties in "Software Development & AI/ML Specifics" (V&V, continuous learning) and "Data Management, Security & Privacy" (cybersecurity risks), ensuring product quality and patient safety throughout the lifecycle. Its global applicability to devices makes it highly relevant.

*Built for the Kaggle Agents Intensive Capstone 2025.*
