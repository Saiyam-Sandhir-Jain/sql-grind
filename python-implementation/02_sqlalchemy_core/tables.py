from sqlalchemy import (
    create_engine, 
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    CheckConstraint
)

from config import DATABASE_URL
metadata = MetaData()


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    department = Table("department", metadata, autoload_with=engine)

    project = Table(
        "project",
        metadata,

        Column(
            "project_id",
            Integer,
            primary_key=True,
        ),

        Column(
            "name",
            String(150),
            nullable=False,
            unique=True,
        ),

        Column(
            "cost",
            Numeric(14, 2),
        ),

        Column(
            "dept_id",
            Integer,
            ForeignKey("department.dept_id"),
            nullable=False
        ),

        CheckConstraint(
            "cost >= 0",
            name="ck_project_cost_nonnegative",
        ),
    )

    project.drop(engine, checkfirst=True)
    project.create(engine, checkfirst=True)

    # metadata.drop_all(engine)
    # metadata.create_all(engine)

    print("Project table created.")