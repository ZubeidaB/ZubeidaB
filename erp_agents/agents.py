"""Agent definitions for the ERP prototype."""

from crewai import Agent

from tools import read_inventory_data


# Agent 1: Sales Agent
sales_agent = Agent(
    role="Sales Agent",
    goal=(
        "Understand user purchase requests, coordinate with the Inventory Agent, "
        "and give clear recommendations to the customer."
    ),
    backstory=(
        "You are a friendly ERP sales coordinator. You collect product requests "
        "from users, ask inventory for stock validation, and summarize answers "
        "in plain language."
    ),
    verbose=True,
    allow_delegation=True,
)


# Agent 2: Inventory Agent
inventory_agent = Agent(
    role="Inventory Agent",
    goal=(
        "Check inventory levels using local data and classify each requested "
        "item as Available, Partially Available, or Out of Stock."
    ),
    backstory=(
        "You manage warehouse stock records. You carefully inspect the inventory "
        "database and report stock status, partial delivery options, and restock "
        "timelines in structured format."
    ),
    verbose=True,
    tools=[read_inventory_data],
)
