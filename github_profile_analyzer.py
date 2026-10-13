
import requests
from datetime import datetime

API_URL = "https://api.github.com"
TIMEOUT = 15


def fetch_github_data(username):
    """Fetch a public GitHub profile and its repositories."""
    headers = {
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(
            f"{API_URL}/users/{username}",
            headers=headers,
            timeout=TIMEOUT
        )

        if response.status_code == 404:
            print("GitHub username not found.")
            return None, None

        response.raise_for_status()
        profile = response.json()

        response = requests.get(
            f"{API_URL}/users/{username}/repos",
            headers=headers,
            params={
                "sort": "updated",
                "per_page": 100,
                "type": "owner"
            },
            timeout=TIMEOUT
        )

        response.raise_for_status()
        repositories = response.json()

        return profile, repositories

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print("Connection failed. Check your internet.")
    except requests.exceptions.HTTPError as error:
        print(f"GitHub returned an HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
    except ValueError:
        print("GitHub returned invalid JSON data.")

    return None, None


def display_profile(profile, repositories):
    """Display profile details and repository statistics."""
    print("\n========== GITHUB PROFILE ==========")
    print(f"Username: {profile.get('login', 'N/A')}")
    print(f"Name: {profile.get('name') or 'Not provided'}")
    print(f"Bio: {profile.get('bio') or 'Not provided'}")
    print(f"Location: {profile.get('location') or 'Not provided'}")
    print(f"Public repositories: {profile.get('public_repos', 0)}")
    print(f"Followers: {profile.get('followers', 0)}")
    print(f"Following: {profile.get('following', 0)}")

    created = profile.get("created_at")
    if created:
        date = datetime.fromisoformat(
            created.replace("Z", "+00:00")
        )
        print(f"Account created: {date:%d %B %Y}")

    print("\n========== TOP REPOSITORIES ==========")

    if not repositories:
        print("No public repositories found.")
        return

    # Sort repositories by star count.
    popular = sorted(
        repositories,
        key=lambda repo: repo.get("stargazers_count", 0),
        reverse=True
    )

    for number, repo in enumerate(popular[:10], start=1):
        print(f"\n{number}. {repo['name']}")
        print(f"   Stars: {repo.get('stargazers_count', 0)}")
        print(f"   Language: {repo.get('language') or 'Not specified'}")
        print(f"   Forks: {repo.get('forks_count', 0)}")
        print(f"   URL: {repo['html_url']}")

        description = repo.get("description")
        if description:
            print(f"   Description: {description}")

    print("\nNote: Only the first 100 repositories are fetched.")
    print("====================================")


def main():
    print("===== GITHUB PROFILE ANALYZER =====")

    username = input("Enter a GitHub username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    profile, repositories = fetch_github_data(username)

    if profile is not None and repositories is not None:
        display_profile(profile, repositories)


if __name__ == "__main__":
    main()
