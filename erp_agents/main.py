"""Entry point for ERP agentic AI prototype with CrewAI."""

import os

from crewai import Crew, Process
from dotenv import load_dotenv

from agents import inventory_agent, sales_agent
from tasks import create_tasks


def run():
    """Run the ERP workflow in terminal."""
    load_dotenv()

    # Validate API key setup before running the crew.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to .env before running this program."
        )

    print("\n=== ERP Sales & Inventory Assistant ===")
    user_request = input(
        "Enter your product request (example: I need 3 Laptops and 2 Mouse):\n> "
    )

    # Create tasks for current user request.
    tasks = create_tasks(user_request, sales_agent, inventory_agent)

    # Build and run crew workflow (sequential for clarity).
    crew = Crew(
        agents=[sales_agent, inventory_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\n=== Final Result ===")
    print(result)


if __name__ == "__main__":
    run()
