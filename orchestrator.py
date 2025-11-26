from typing import List
from google.adk.agents import Agent, SequentialAgent


def create_regulatory_pipeline(
    planner: Agent,
    retriever: Agent,
    analyzer: Agent,
    critic: Agent,
    model_name: str = 'gemini-2.5-flash'
) -> SequentialAgent:
    """
    Creates a strict sequential workflow:
    Planner -> Retriever -> Analyzer -> Critic
    
    Args:
        planner: The agent responsible for identifying uncertainty.
        retriever: The agent responsible for fetching documents.
        analyzer: The agent responsible for probability scoring.
        critic: The agent responsible for review and verification.
        
    Returns:
        A SequentialAgent that executes these steps in order.
    """
    
    # The SequentialAgent enforces that sub_agents run one after another.
    # The output of the previous agent is automatically appended to the 
    # context/prompt of the next agent.
    
    pipeline = SequentialAgent(
        name="regulatory_pipeline_root",
        description="A strict workflow for regulatory analysis.",
        # The agents will execute in this exact order
        sub_agents=[
            planner,
            retriever,
            analyzer,
            critic
        ]
    )
    
    return pipeline