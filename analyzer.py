from collections import Counter
from datetime import datetime

def analyze_repos(repos, followers):

    total_repos = len(repos)
    total_stars = sum(repo["stargazers_count"] for repo in repos)
    total_forks = sum(repo["forks_count"] for repo in repos)

    languages = [repo["language"] for repo in repos if repo["language"]]
    language_count = Counter(languages)

    skills = list(language_count.keys())

    avg_stars = total_stars / total_repos if total_repos else 0

    most_starred = None
    if repos:
        most_starred = max(repos, key=lambda x: x["stargazers_count"])["name"]

    score = (total_repos * 2) + total_stars + (total_forks * 1.5) + followers

    if score < 20:
        level = "Beginner"
    elif score < 50:
        level = "Intermediate"
    else:
        level = "Advanced"

    top_repos = sorted(
        repos,
        key=lambda x: x["stargazers_count"],
        reverse=True
    )[:5]

    creation_dates = [
        datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
        for repo in repos
    ]

    return {
        "repos": total_repos,
        "stars": total_stars,
        "forks": total_forks,
        "languages": language_count,
        "skills": skills,
        "avg_stars": avg_stars,
        "most_starred": most_starred,
        "score": score,
        "level": level,
        "top_repos": top_repos,
        "dates": creation_dates
    }