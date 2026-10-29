"""A research agent with OptimistFi's tools.

Needs OPENAI_API_KEY for the model. The OptimistFi tools themselves need no key.

    pip install agno-optimistfi openai
    python examples/research_agent.py
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agno_optimistfi import OptimistFiTools

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[OptimistFiTools()],
    instructions=[
        "Name the source and the date of each figure you quote.",
        "Treat the data as research context, not as trading advice.",
    ],
    markdown=True,
)

if __name__ == "__main__":
    agent.print_response(
        "Which House members traded NVDA this year, have its insiders been selling, "
        "and where is BTC perp funding highest right now?"
    )
