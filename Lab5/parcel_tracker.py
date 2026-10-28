"""Track parcel bookings and delivery progress for a courier service."""

import secrets
import tempfile
from datetime import date
from typing import TypedDict

STATUS_FLOW = ["Booked", "Picked Up", "In Transit", "Out for Delivery", "Delivered"]


class Parcel(TypedDict):
    """Details recorded for one parcel."""

    sender: str
    receiver: str
    weight: float
    status: int
    booked: str


parcels: dict[str, Parcel] = {}


def book_parcel(sender: str, receiver: str, weight_kg: float, history: list[str] | None = None) -> str:
    """Book a parcel and optionally append its ID to a caller-provided history."""
    tracking_id = f"TRK{10001 + len(parcels)}"
    parcels[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }
    if history is not None:
        history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id: str) -> str:
    """Move a parcel forward one delivery stage, stopping at Delivered."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg: float) -> float:
    """Return the shipping cost for a parcel's weight in kilograms."""
    cost=50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id: str) -> str:
    """Return a parcel's route and status, or an unknown-ID message."""
    parcel = parcels.get(tracking_id)
    if parcel is None:
        return f"Unknown tracking id {tracking_id}"
    route = f"{parcel['sender']} -> {parcel['receiver']}"
    return f"{route}: {STATUS_FLOW[parcel['status']]}"


def is_with_courier(tracking_id: str) -> bool:
    """Return whether a parcel is in a courier-controlled delivery stage."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status == "Picked Up" or status == "In Transit"


def label_path() -> str:
    """Create a unique, empty temporary label file and return its path."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as label_file:
        return label_file.name


def main() -> None:
    """Run a short parcel-tracking demonstration."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000")) # unknown id
    delivery_otp = secrets.randbelow(9000) + 1000
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:",len(parcels))


if __name__ == "__main__":
    main()
