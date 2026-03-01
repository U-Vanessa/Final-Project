from sqlalchemy import inspect, text


def run_startup_migrations(engine) -> None:
    inspector = inspect(engine)

    if "users" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}

    required_user_columns = {
        "username": "ALTER TABLE users ADD COLUMN username VARCHAR",
        "full_name": "ALTER TABLE users ADD COLUMN full_name VARCHAR",
        "department": "ALTER TABLE users ADD COLUMN department VARCHAR",
        "station": "ALTER TABLE users ADD COLUMN station VARCHAR",
        "updated_at": "ALTER TABLE users ADD COLUMN updated_at DATETIME",
    }

    with engine.begin() as connection:
        for column_name, ddl in required_user_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(ddl))
