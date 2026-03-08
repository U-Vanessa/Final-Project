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

    document_columns = set()
    if "documents" in inspector.get_table_names():
        document_columns = {column["name"] for column in inspector.get_columns("documents")}

    required_document_columns = {
        "approval_status": "ALTER TABLE documents ADD COLUMN approval_status VARCHAR DEFAULT 'pending'",
        "approved_by_id": "ALTER TABLE documents ADD COLUMN approved_by_id INTEGER",
        "approved_at": "ALTER TABLE documents ADD COLUMN approved_at DATETIME",
        "approval_note": "ALTER TABLE documents ADD COLUMN approval_note TEXT",
        "disposal_id": "ALTER TABLE documents ADD COLUMN disposal_id INTEGER",
    }

    disposal_columns = set()
    if "disposals" in inspector.get_table_names():
        disposal_columns = {column["name"] for column in inspector.get_columns("disposals")}

    required_disposal_columns = {
        "request_number": "ALTER TABLE disposals ADD COLUMN request_number VARCHAR",
        "document_id": "ALTER TABLE disposals ADD COLUMN document_id INTEGER",
        "status": "ALTER TABLE disposals ADD COLUMN status VARCHAR DEFAULT 'pending'",
    }

    with engine.begin() as connection:
        for column_name, ddl in required_user_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(ddl))

        for column_name, ddl in required_document_columns.items():
            if document_columns and column_name not in document_columns:
                connection.execute(text(ddl))

        for column_name, ddl in required_disposal_columns.items():
            if disposal_columns and column_name not in disposal_columns:
                connection.execute(text(ddl))
