
from google import genai
from dotenv import load_dotenv
import os
import json
import sqlite3
from datetime import datetime


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, ".env")
SHOP_FILE = os.path.join(BASE_DIR, "data", "shop.json")

DATABASE_FOLDER = os.path.join(BASE_DIR, "database")
DATABASE_FILE = os.path.join(
    DATABASE_FOLDER,
    "content_saathi.db"
)


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

print("Gemini API key loaded:", bool(api_key))


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"


# ==========================================
# LOAD SHOP JSON
# ==========================================

try:
    with open(SHOP_FILE, "r", encoding="utf-8") as file:
        shop = json.load(file)

except FileNotFoundError as exc:
    raise FileNotFoundError(
        f"Shop configuration not found: {SHOP_FILE}"
    ) from exc

except json.JSONDecodeError as exc:
    raise ValueError(
        "Invalid JSON format in data/shop.json"
    ) from exc


# ==========================================
# DATE AND DAY
# ==========================================

today = datetime.now()

date = today.strftime("%d-%m-%Y")
day = today.strftime("%A")


# ==========================================
# FESTIVAL
# ==========================================

festival = shop.get("calendar", {}).get(
    date,
    "No major festival today"
)


print("\n========================================")
print("CONTENT SAATHI - GEMINI")
print("========================================")

print("Today's Date:", date)
print("Today's Day:", day)
print("Today's Festival:", festival)


# ==========================================
# AI PROMPT
# ==========================================

prompt = f"""
You are Content Saathi, a content writer for a local shop.

Shop Name: {shop["shop_name"]}
Business Type: {shop["business_type"]}
Location: {shop["location"]}
Products: {", ".join(shop["products"])}
Tone: {shop["tone"]}
Language: {shop["language"]}

Today's Date: {date}
Today's Day: {day}
Today's Festival/Calendar Event: {festival}

Write a short Good Morning promotional post for this shop.

Requirements:
- Keep it short and punchy.
- Suitable for Telegram and Instagram.
- Use a friendly local tone.
- Mention the shop name naturally.
- Mention relevant products.
- Use simple Hindi-English.
- Add suitable emojis.
- Make it copy-paste ready.
- Do not invent prices or discounts.
- Do not invent opening hours.
- Do not invent festival information.
- Do not make false claims.
- Return only the final post.
"""


# ==========================================
# GENERATE POST USING GEMINI
# ==========================================

print("\nGenerating today's post using Gemini...\n")

try:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "temperature": 0.7
        }
    )

    generated_post = (response.text or "").strip()

    if not generated_post:
        raise RuntimeError("Gemini returned an empty response.")

except Exception as exc:
    raise RuntimeError(
        f"Gemini post generation failed: {exc}"
    ) from exc


# ==========================================
# DISPLAY GENERATED POST
# ==========================================

print("\nGenerated Post:\n")
print("----------------------------------------")
print(generated_post)
print("----------------------------------------")


# ==========================================
# CREATE DATABASE FOLDER
# ==========================================

os.makedirs(DATABASE_FOLDER, exist_ok=True)


# ==========================================
# CONNECT DATABASE
# ==========================================

print("\nDatabase path:")
print(DATABASE_FILE)

con = sqlite3.connect(DATABASE_FILE)

try:
    cursor = con.cursor()

    # ==========================================
    # CREATE POSTS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts
    (
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

    # ==========================================
    # SAVE POST
    # ==========================================

    cursor.execute("""
    INSERT INTO posts
    (
        shop_name,
        generated_date,
        day,
        festival,
        content,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        shop["shop_name"],
        date,
        day,
        festival,
        generated_post,
        "DRAFT"
    ))

    # ==========================================
    # COMMIT CHANGES
    # ==========================================

    con.commit()

    # ==========================================
    # VERIFY DATABASE
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]

    print("\nPost saved successfully in database.")
    print("Status: DRAFT")
    print("Total posts in database:", total_posts)

except Exception:
    con.rollback()
    raise

finally:
    con.close()


print("\n========================================")
print("CONTENT SAATHI PROCESS COMPLETED")
print("========================================")
