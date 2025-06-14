"""Descarga eventos usando Meetup api usando la api graphql"""

import os
import json
import jwt
import requests
from lektor.utils import slugify
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
CLIENT_ID = os.getenv("MEETUP_CLIENT_ID")
AUTHORIZED_MEMBER_ID = os.getenv("MEETUP_MEMBER_ID")
SIGNING_KEY_ID = os.getenv("MEETUP_SIGNING_KEY_ID")
MEETUP_API_URL = "https://api.meetup.com/gql-ext"
GROUP_URLNAME = os.getenv("MEETUP_GROUP_URLNAME")
PRIVATE_KEY = os.getenv("MEETUP_PRIVATE_KEY")

# Load from .pem if ENV variable MEETUP_PRIVATE_KEY does not exists
if PRIVATE_KEY is None:
    with(open('private_key.pem', "r", encoding='UTF-8')) as file:
        PRIVATE_KEY = file.read()

# Generate JWT Token
payload = {
    "iss": CLIENT_ID,
    "sub": AUTHORIZED_MEMBER_ID,
    "aud": "api.meetup.com",
    "exp": 120
}

JWT_TOKEN = jwt.encode(
    payload,
    PRIVATE_KEY,
    algorithm="RS256",
    headers={"kid": SIGNING_KEY_ID}
)

with(open('scripts/get_events.graphql', "r", encoding='UTF-8')) as file:
    query = file.read()

# Send Request to Meetup API
headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
payload = {"query": query, "variables": {"group": GROUP_URLNAME}}
response = requests.post(MEETUP_API_URL, json=payload, headers=headers, timeout=20000)
data = response.json()

# Print Fetched Event Data (Instead of Writing to Files)
for event in data["data"]["groupByUrlname"]["past_events"]["edges"]:
    event_data = event["node"]
    slug = f"{event_data['dateTime'][:10]}-{slugify(event_data['title'])}"
    print(f"https://pybaq.co/eventos/{slug}")
    print(f"Slug: {slug}")
    print(f"Event ID: {event_data['id']}")
    print(f"Titulo: {event_data['title']}")
    print(f"Fecha: {event_data['dateTime']}")
    print(f"URL: {event_data['eventUrl']}")
    print(f"Imagen: {event_data['featuredEventPhoto']}")
    print(f"Descripción: {event_data['description']}")
    print(f"Lugar: {event_data['venues']}")
    print("-" * 40)  # Separator for readability

with open("databags/meetup_gql.json", "w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data))
