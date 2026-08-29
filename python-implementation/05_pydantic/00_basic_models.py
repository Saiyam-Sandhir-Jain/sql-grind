from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    is_active: bool

def main():
    # 1. Valid data: pydantic parses/validates it for you
    user = User(id=1, name="Asha", is_active=True)
    print("Created user:", user)
    print("Access like a normal object:", user.name, user.id)

    # 2. Pydantic performs type coercion for compatible types
    # "42" (a string) is coerced into an int automatically.
    user2 = User(id="42", name="Rohan", is_active="true")
    print("\nCoerced user:", user2, "  id type:", type(user2.id))

    # 3. Invalid data raises a ValidationError with clear details
    try:
        User(id="not-a-number", name="Bad", is_active=True)
    except ValidationError as e:
        print("\nValidation failed as expected:")
        print(e)

    # 4. Models behave like dataclasses but with runtime validation
    print("\nEquality check:", User(id=1, name="Asha", is_active=True) == user)

if __name__ == "__main__":
    main()