from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
import urllib.parse
import requests

# Scope of permission for ServiceM8
SCOPE = ["read_customers", "read_jobs"]


# region OAuth2 View
def servicem8_login(request):
    auth_url = settings.SERVICEM8_AUTH_URL

    params = {
        "client_id": settings.SERVICEM8_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SERVICEM8_REDIRECT_URI,
        "scope": " ".join(SCOPE),
    }
    print(settings.SERVICEM8_REDIRECT_URI)


    # print(f"{auth_url}?{urllib.parse.urlencode(params)}")
    # return JsonResponse({})
    return redirect(f"{auth_url}?{urllib.parse.urlencode(params)}")


def servicem8_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    token_url = settings.SERVICEM8_TOKEN_URL
    data = {
        "client_id": settings.SERVICEM8_CLIENT_ID,
        "client_secret": settings.SERVICEM8_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SERVICEM8_REDIRECT_URI,
    }

    response = requests.post(token_url, data=data)

    print(response.content)

    if response.status_code == 200:
        token_data = response.json()
        request.session["servicem8_access_token"] = token_data["access_token"]
        return JsonResponse({"message": "OAuth2 Success", "token_data": token_data})
    else:
        return JsonResponse({"error": "Failed to get access token", "response": response.json()}, status=400)


# endregion

def get_servicem8_jobs(request):
    access_token = request.session.get("servicem8_access_token")

    if not access_token:
        print('no access token')
        return JsonResponse({"error": "Unauthorized"}, status=401)
    print(access_token)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.servicem8.com/api_1.0/Job.json", headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch jobs", "response": response.json()}, status=400)
