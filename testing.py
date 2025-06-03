import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",       # or your DB host
    database="cervical_pg",     # your DB name
    user="paardarshee",       # your DB username
    password="postgres"    # your DB password
)

# Create a cursor to run SQL commands
cur = conn.cursor()

# Example: Create a table
cur.execute("""
    CREATE TABLE IF NOT EXISTS CPG_users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

# Example: Insert data
cur.execute("""
    INSERT INTO CPG_users (name, email) VALUES (%s, %s)
""", ("Alice", "alice@example.com"))

# Commit changes
conn.commit()

# Example: Query data
cur.execute("SELECT * FROM CPG_users")
rows = cur.fetchall()
for row in rows:
    print(row)

# Clean up
cur.close()
conn.close()
