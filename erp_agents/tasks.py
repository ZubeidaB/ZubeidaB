"""Task definitions for the ERP CrewAI workflow."""

from crewai import Task


def create_tasks(user_request: str, sales_agent, inventory_agent):
    """Create an ordered list of tasks for the ERP agent workflow.

    Args:
        user_request: Raw terminal input from the user.
        sales_agent: Sales Agent object.
        inventory_agent: Inventory Agent object.

    Returns:
        list[Task]: Tasks used by the crew.
    """

    # Task 1: Sales agent extracts requested products and quantities.
    parse_request_task = Task(
        description=(
            "Read this user order request and extract products with quantities:\n"
            f"{user_request}\n\n"
            "Return ONLY valid JSON using this schema:\n"
            "{\n"
            '  "requests": [\n'
            "    {\"product\": \"ProductName\", \"requested_quantity\": 1}\n"
            "  ]\n"
            "}\n"
            "If quantity is missing, assume quantity = 1."
        ),
        expected_output="A JSON object named requests with product and requested_quantity fields.",
        agent=sales_agent,
    )

    # Task 2: Inventory agent checks stock and partial delivery options.
    inventory_check_task = Task(
        description=(
            "Use the parsed request from the previous task and the inventory tool to evaluate stock.\n"
            "For each product, calculate status using these rules:\n"
            "- Available: stock >= requested_quantity\n"
            "- Partially Available: 0 < stock < requested_quantity\n"
            "- Out of Stock: stock = 0 OR product does not exist\n\n"
            "Also determine partial_delivery_possible:\n"
            "- true for Partially Available\n"
            "- false otherwise\n\n"
            "Return ONLY valid JSON in this schema:\n"
            "{\n"
            '  "results": [\n'
            "    {\n"
            '      "product": "Laptop",\n'
            '      "requested_quantity": 2,\n'
            '      "available_quantity": 1,\n'
            '      "availability_status": "Partially Available",\n'
            '      "partial_delivery_possible": true,\n'
            '      "restock_days": 7\n'
            "    }\n"
            "  ]\n"
            "}"
        ),
        expected_output="Structured JSON with availability analysis for each requested item.",
        agent=inventory_agent,
        context=[parse_request_task],
    )

    # Task 3: Sales agent produces final user-facing summary.
    final_response_task = Task(
        description=(
            "Use inventory analysis from the previous task to create a customer-friendly response.\n"
            "For each item include:\n"
            "- Product\n"
            "- Requested Quantity\n"
            "- Availability Status\n"
            "- Restock Timeline (in days)\n"
            "- Final Recommendation\n\n"
            "If item is Partially Available, suggest partial delivery now and remaining units after restock.\n"
            "If item is Out of Stock, suggest waiting until restock or replacing with another available item.\n"
            "Keep the answer easy to read with bullet points."
        ),
        expected_output="Readable final sales response with recommendations for each requested product.",
        agent=sales_agent,
        context=[parse_request_task, inventory_check_task],
    )

    return [parse_request_task, inventory_check_task, final_response_task]
