import requests
import os
import json

TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

def post_issue(hash_value):
    url = f"https://api.github.com/repos/{REPO}/issues"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "title": f"Anchor: {hash_value[:12]}",
        "body": f"Immutable anchor hash:\n\n{hash_value}"
    }

    requests.post(url, headers=headers, json=data)
