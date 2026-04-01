# Updated analyzer.py
from collections import Counter
from datetime import datetime

def analyze_repos(repos, followers):
    total_repos = len(repos)
    total_stars = sum(repo["stargazers_count"] for repo in repos)
    total_forks = sum(repo["forks_count"] for repo in repos)

    languages = [repo["language"] for repo in repos if repo["language"]]
    language_count = Counter(languages)
    skills = list(language_count.keys())
    
    # NEW: Determine primary language
    primary_lang = language_count.most_common(1)[0][0] if languages else "N/A"
    
    # NEW: Popularity ratio
    avg_stars = round(total_stars / total_repos, 2) if total_repos > 0 else 0

    score = (total_repos * 1) + (total_stars * 2) + (total_forks * 1.5) + (followers * 0.5)

    if score < 15:
        level = "Emerging Talent"
    elif score < 75:
        level = "Profound Developer"
    else:
        level = "Open Source Veteran"

    top_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:5]

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
        "primary_lang": primary_lang, # New
        "avg_stars": avg_stars,       # New
        "followers": followers,       # New
        "score": score,
        "level": level,
        "top_repos": top_repos,
        "dates": creation_dates
    }