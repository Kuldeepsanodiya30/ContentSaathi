import sqlite3
import os


# Database folder
database_folder = "database"
database_file = os.path.join(
    database_folder,
    "content_saathi.db"
)


# Create database folder if it does not exist
if not os.path.exists(database_folder):
    os.makedirs(database_folder)


# Connect to database
con = sqlite3.connect(database_file)

cursor = con.cursor()


# Create posts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_name TEXT,
    generated_date TEXT,
    day TEXT,
    festival TEXT,
    content TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


# Save changes
con.commit()

print("Database and posts table created successfully.")


# Close database
con.close()