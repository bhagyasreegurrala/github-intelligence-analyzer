import requests

def get_user_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None


def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return []