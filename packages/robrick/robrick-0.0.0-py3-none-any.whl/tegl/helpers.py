import ast

from collections import namedtuple
from datetime import datetime
from typing import List


Slot = namedtuple("Slot", ["number", "id", "project_id", "name", "created_at", "updated_at"])


def get_slots(payload: bytes) -> List[Slot]:
    """
    Get the slot information from the LEGO `.slots` file output.
    """

    slots = []

    for slot, data in ast.literal_eval(payload.decode()).items():
        slots.append(
            Slot(
                slot,
                data["id"],
                data["project_id"],
                data["name"],
                datetime.fromtimestamp(data["created"] / 1000.0),
                datetime.fromtimestamp(data["modified"] / 1000.0),
            )
        )

    return sorted(slots, key=lambda s: s.number)
