
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def generate_post(daily_context):

    prompt = f"""
You are Content Saathi, an AI social media content writer
for a local Indian business.

Create today's social media post using ONLY the information provided below.

SHOP INFORMATION
----------------
Shop Name: {daily_context["shop_name"]}
Business Type: {daily_context["business_type"]}
Location: {daily_context["location"]}

CONTENT STYLE
-------------
Language: {daily_context["language"]}
Tone: {daily_context["tone"]}
Audience: {daily_context["audience"]}

TODAY'S INFORMATION
-------------------
Date: {daily_context["date"]}
Day: {daily_context["day"]}
Weather: {daily_context["weather"]}
Temperature: {daily_context["temperature"]} °C
Festival: {daily_context["festival"]}
Offer: {daily_context["offer"]}

IMPORTANT RULES
---------------
- Use Marathi + Hinglish naturally.
- Keep the language simple and easy to understand.
- Make the post friendly, local, energetic and attractive.
- The business is a Ladies Clothing Store, so talk about ladies fashion,
  clothes, festive collection, shopping or related products.
- Mention "Shree Collection" naturally in the caption.
- Mention Parbhani naturally when appropriate.
- Mention the Ganesh Festival naturally.
- Mention the offer ONLY if an actual offer is provided.
- If the offer is "No offer available", do not create or invent any discount.
- Do NOT add unrelated things such as tea, food, restaurants or other products.
- Use the weather only when it makes sense.
- Make the caption suitable for local women and families.
- Do not make false claims about products, prices or discounts.
- Keep the caption short and social-media-ready.
- Create 4-6 relevant hashtags.
- Create an image prompt specifically for a ladies clothing store.
- The image prompt should include festive shopping, ladies clothing/fashion
  and the local Indian atmosphere when appropriate.

RETURN EXACTLY IN THIS FORMAT:

CAPTION:
...

HASHTAGS:
...

IMAGE_PROMPT:
...
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text

