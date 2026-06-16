import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN and GITHUB_TOKEN != "your_github_token_here" else {}

def fetch_github_user(username: str) -> dict:
    url = f"https://api.github.com/users/{username}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise ValueError("User not found")
    return resp.json()

def fetch_github_repos(username: str) -> list:
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return []
    return resp.json()
