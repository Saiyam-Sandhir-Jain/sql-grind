from enum import Enum
from typing import Literal
from pydantic import BaseModel, ValidationError
 
 
class OrderStatus(str, Enum):
    """Inheriting from `str` too makes this JSON-serializable as plain text."""
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
 
 
class Shipment(BaseModel):
    tracking_id: str
    status: OrderStatus                       # must be one of the Enum values
    priority: Literal["low", "medium", "high"] = "medium"  # inline fixed choices
 
 
def main():
    s = Shipment(tracking_id="TRK123", status="shipped", priority="high")
    print("Shipment:", s)
    print("status is an Enum member:", s.status, "->", type(s.status))
    print("Compare to enum member:", s.status == OrderStatus.SHIPPED)
 
    # Invalid enum value
    try:
        Shipment(tracking_id="TRK124", status="in_orbit")
    except ValidationError as e:
        print("\nInvalid status rejected:")
        print(e.errors()[0]["msg"])
 
    # Invalid literal value
    try:
        Shipment(tracking_id="TRK125", status="pending", priority="urgent")
    except ValidationError as e:
        print("\nInvalid priority rejected:")
        print(e.errors()[0]["msg"])
 
    # Serializes back to plain strings, not Python Enum repr
    print("\nJSON:", s.model_dump_json())
 
 
if __name__ == "__main__":
    main()