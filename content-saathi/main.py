from openai import OpenAI
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

api_key = os.getenv("GROQ_API_KEY")

print("Key loaded:", api_key is not None)

if not api_key:
    print("GROQ_API_KEY not found")
    exit()


# ==========================================
# GROQ CLIENT
# ==========================================

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# ==========================================
# LOAD SHOP JSON
# ==========================================

with open(SHOP_FILE, "r", encoding="utf-8") as file:
    shop = json.load(file)


# ==========================================
# DATE AND DAY
# ==========================================

today = datetime.now()

date = today.strftime("%d-%m-%Y")
day = today.strftime("%A")


# ==========================================
# FESTIVAL
# ==========================================

festival = shop["calendar"].get(
    date,
    "No major festival today"
)


print("\n========================================")
print("CONTENT SAATHI")
print("========================================")

print("Today's Date:", date)
print("Today's Day:", day)
print("Today's Festival:", festival)


# ==========================================
# AI PROMPT
# ==========================================

prompt = f"""
You are a content writer for a local shop.

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
- Friendly local tone.
- Mention the shop name naturally.
- Mention relevant products.
- Use simple Hindi-English.
- Add suitable emojis.
- Make it copy-paste ready.
- Do not invent prices.
- Do not invent discounts.
- Do not invent opening hours.
- Do not invent festival information.
- Do not make false claims.
- Return only the final post.
"""


# ==========================================
# GENERATE POST
# ==========================================

print("\nGenerating today's post...\n")

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# ==========================================
# GET GENERATED POST
# ==========================================

generated_post = response.choices[0].message.content.strip()


print("\nGenerated Post:\n")
print("----------------------------------------")
print(generated_post)
print("----------------------------------------")


# ==========================================
# CREATE DATABASE FOLDER
# ==========================================

if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)


# ==========================================
# CONNECT DATABASE
# ==========================================

print("\nDatabase path:")
print(DATABASE_FILE)

con = sqlite3.connect(DATABASE_FILE)

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
# COMMIT
# ==========================================

con.commit()


# ==========================================
# VERIFY DATABASE
# ==========================================

cursor.execute("""
SELECT COUNT(*) FROM posts
""")

total_posts = cursor.fetchone()[0]


print("\nPost saved successfully in database.")
print("Status: DRAFT")
print("Total posts in database:", total_posts)


# ==========================================
# CLOSE DATABASE
# ==========================================

con.close()


print("\n========================================")
print("CONTENT SAATHI PROCESS COMPLETED")
print("========================================")