from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Union

class Employee(BaseModel):
    name: str
    nickname: Optional[str] = None
    department: str = "General"
    skills: list[str] = Field(default_factory=list)
    manager_id: Union[int, str, None] = None

def main():
    # Minimal required data only
    e1 = Employee(name="Meera")
    print("Defaults applied:", e1)
 
    # Providing everything
    e2 = Employee(
        name="Kabir",
        nickname="Kabo",
        department="Engineering",
        skills=["python", "sql"],
        manager_id=101,
    )
    print("\nFully specified:", e2)
 
    # department is NOT nullable even though it has a default
    try:
        Employee(name="X", department=None)
    except ValidationError as e:
        print("\nExpected failure (department can't be None):")
        print(e.errors()[0]["msg"])
 
    # Two separate instances don't share the default list (no mutable-default bug)
    a = Employee(name="A")
    b = Employee(name="B")
    a.skills.append("leadership")
    print("\nMutable defaults are independent:")
    print("a.skills:", a.skills)
    print("b.skills:", b.skills)
 
 
if __name__ == "__main__":
    main()

