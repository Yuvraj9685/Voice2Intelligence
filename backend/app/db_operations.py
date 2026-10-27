```python
import json
import os
import psycopg2
from psycopg2 import OperationalError, DatabaseError


def save_call_analysis(data: dict, transcript, audio_file: str):
    """
    Store call transcript and AI analysis in PostgreSQL.
    Uses DATABASE_URL from the environment.
    """
    query = """
        INSERT INTO calls (
            audio_file,
            transcript,
            analysis_json
        )
        VALUES (%s, %s, %s);
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured"
        )

    conn = None

    try:
        conn = psycopg2.connect(database_url)

        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    audio_file,
                    json.dumps(transcript, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False),
                ),
            )

        conn.commit()

    except (OperationalError, DatabaseError) as db_err:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Database error: {db_err}") from db_err

    finally:
        if conn:
            conn.close()
```
