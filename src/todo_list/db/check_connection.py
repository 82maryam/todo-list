from sqlalchemy import text

from .session import engine


def main() -> None:
    print("Trying to connect to the database...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database responded with:", result.scalar_one())


if __name__ == "__main__":
    main()
