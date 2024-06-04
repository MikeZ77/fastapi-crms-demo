import os


def get_postgres_uri():
    password = os.getenv("DB_PASSWORD", "postgres")
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "postgres")
    db_name = os.getenv("DB_NAME", "crms")
    port = os.getenv("DB_PORT", "5432")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
