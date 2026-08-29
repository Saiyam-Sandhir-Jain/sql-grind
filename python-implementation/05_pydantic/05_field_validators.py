from pydantic import BaseModel, field_validator, ValidationError

class SignupForm(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

    # "after" mode (default): runs AFTER pydantic's own type validation.
    # Receives the already-typed value.
    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, value: str) -> str:
        if " " in value:
            raise ValueError("username must not contain spaces")
        return value.lower()

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain '@'")
        return value

    # "before" mode: runs BEFORE type coercion, receives the raw input.
    # Useful for cleaning up input like stripping whitespace before parsing.
    @field_validator("password", mode="before")
    @classmethod
    def strip_password(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, value: str, info) -> str:
        # `info.data` holds previously-validated fields (declared earlier in class)
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwords do not match")
        return value

def main():
    form = SignupForm(
        username="Ada Lovelace".replace(" ", ""),  # avoid space example below
        email="ada@example.com",
        password="  secret123  ",
        confirm_password="secret123",
    )
    print("Valid signup:", form)
 
    try:
        SignupForm(username="ada lovelace", email="ada@example.com",
                    password="x", confirm_password="x")
    except ValidationError as e:
        print("\nSpace in username rejected:", e.errors()[0]["msg"])
 
    try:
        SignupForm(username="ada", email="ada-example.com",
                    password="x", confirm_password="x")
    except ValidationError as e:
        print("\nBad email rejected:", e.errors()[0]["msg"])
 
    try:
        SignupForm(username="ada", email="ada@example.com",
                    password="secret123", confirm_password="different")
    except ValidationError as e:
        print("\nMismatched passwords rejected:", e.errors()[0]["msg"])
 
 
if __name__ == "__main__":
    main()