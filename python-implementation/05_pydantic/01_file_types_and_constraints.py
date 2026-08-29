from datetime import datetime

from pydantic import BaseModel, Field, ValidationError

class Article(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    views: int = Field(ge=0)
    rating: float = Field(ge=0.0, le=5.0)
    tags: list[str] = Field(min_length=1, max_length=5)
    published_at: datetime
    metadata: dict[str, str] = Field(default_factory=dict)

    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")

def main():
    article = Article(
        title="Learning Pydantic",
        views=120,
        rating=4.5,
        tags=["python", "pydantic"],
        published_at="2025-01-01T10:00:00",
        slug="learning-pydantic",
    )

    print("Valid article:", article)
    print("published_at type:", type(article.published_at))

    # Constraint Violations
    bad_cases = [
        dict(title="ab", views=1, rating=5, tags=["x"], published_at="2025-01-01", slug="ok"),  # title too short
        dict(title="Valid Title", views=-5, rating=5, tags=["x"], published_at="2025-01-01", slug="ok"),  # negative views
        dict(title="Valid Title", views=1, rating=9.9, tags=["x"], published_at="2025-01-01", slug="ok"),  # rating out of range
        dict(title="Valid Title", views=1, rating=5, tags=[], published_at="2025-01-01", slug="ok"),  # empty tags
        dict(title="Valid Title", views=1, rating=5, tags=["x"], published_at="2025-01-01", slug="Not Valid!"),  # bad slug
    ]

    for i, case in enumerate(bad_cases, 1):
        try:
            Article(**case)
        except ValidationError as e:
            print(f"\nCase {i} failed as expected -> {e.errors()[0]['msg']}")

if __name__ == "__main__":
    main()