import requests
from django.http import JsonResponse

from .jira_configs import JIRA_API_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY

HEADERS = {"Content-Type": "application/json"}
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)


def get_all_issues(request):
    """Fetch all issues from the Jira project."""
    url = f"{JIRA_API_URL}/project/search"
    params = {
        "jql": f"project={JIRA_PROJECT_KEY} ORDER BY created DESC",
        "maxResults": 100,  # Adjust as needed
        "fields": "summary,status,assignee,description"
    }
    response = requests.get(url, headers=HEADERS, auth=AUTH, params=params)

    print(response.content)
    # return response.json() if response.status_code == 200 else {"error": response.text}
    return JsonResponse({})
