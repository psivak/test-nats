# Initialization Scripts and Secrets

## .env Template
```env
DB_USER=postgres
DB_PASSWORD=secure_password_here
DB_NAME=app_db
DATABASE_URL=postgresql://postgres:secure_password_here@db:5432/app_db
```

## Python Init Script (init_db.py)
If the user describes an initial state, generate a script like this:
```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    # Create schema
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        );
    """)
    
    # Insert seed data
    cur.execute("INSERT INTO items (name, description) VALUES (%s, %s)", ("Seed Item", "Initial data"))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
```

## Docker Compose Mount
Ensure this script is mounted or executed during container startup, or triggered via `postCreateCommand`.
For PostgreSQL, you can also use SQL files in `init-db/` folder mounted to `/docker-entrypoint-initdb.d`.
