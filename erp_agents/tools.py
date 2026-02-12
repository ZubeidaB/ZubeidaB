"""Tools used by ERP agents.

This module contains simple CrewAI tools for reading inventory data.
"""

from __future__ import annotations

import json
from pathlib import Path

from crewai.tools import tool


# Inventory file is stored in the same folder as this script.
INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"


@tool("Read Inventory Database")
def read_inventory_data() -> str:
    """Read local inventory.json and return it as a JSON string.

    Returns:
        str: JSON string with product names, stock quantities, and restock days.
    """
    if not INVENTORY_FILE.exists():
        return "{}"

    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return json.dumps(data)
