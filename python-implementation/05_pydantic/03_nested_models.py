from pydantic import BaseModel, ValidationError

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    order_id: int
    shipping_address: Address
    items: list[OrderItem]

    @property
    def total(self) -> float:
        return sum(item.quantity * item.unit_price for item in self.items)

def main():
    order = Order(
        order_id=1001,
        shipping_address={
            "street": "12 MG Road",
            "city": "Ahmedabad",
            "zip_code": "380001",
        },
        items=[
            {"product_name": "Keyboard", "quantity": 2, "unit_price": 1500.0},
            {"product_name": "Mouse", "quantity": 1, "unit_price": 500.0},
        ],
    )
    print("Order:", order)
    print("Order total:", order.total)
    print("\nNested access:", order.shipping_address.city)
 
    # Errors report the exact nested path where validation failed
    try:
        Order(
            order_id=1002,
            shipping_address={"street": "1 Main St", "city": "Delhi", "zip_code": "110001"},
            items=[{"product_name": "Monitor", "quantity": "two", "unit_price": 8000.0}],
        )
    except ValidationError as e:
        print("\nNested validation error (note the 'loc' path):")
        for err in e.errors():
            print(" ->", err["loc"], err["msg"])
 
    # model_dump() recursively converts nested models to plain dicts
    print("\nAs plain dict:")
    print(order.model_dump())
 
 
if __name__ == "__main__":
    main()