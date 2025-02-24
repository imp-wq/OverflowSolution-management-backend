import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
import urllib.parse
import requests
from django.views.decorators.csrf import csrf_exempt

# Scope of permission for ServiceM8
SCOPE = ["read_customers", "read_jobs"]


# region OAuth2 View
def servicem8_login(request):
    print(request)
    if request.method == "OPTIONS":
        print(request.method)

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
    oauth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    # response = JsonResponse({"redirect_url": oauth_url})
    response = redirect(oauth_url)
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Credentials"] = "true"
    return redirect(oauth_url)

    # return response


def servicem8_callback(request):
    code = request.GET.get("code")
    redirect_url = request.GET.get("redirect_url")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    token_url = settings.SERVICEM8_TOKEN_URL
    data = {
        "client_id": settings.SERVICEM8_CLIENT_ID,
        "client_secret": settings.SERVICEM8_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        # "redirect_uri": settings.SERVICEM8_REDIRECT_URI,
        "redirect_uri": redirect_url
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
    # access_token = request.session.get("servicem8_access_token")
    access_token = request.headers.get("authorization")
    print(access_token)
    if not access_token:
        print('no access token')
        return JsonResponse({"error": "Unauthorized"}, status=401)
    print(access_token)

    # headers = {"Authorization": f"Bearer {access_token}"}
    headers = {"Authorization": f"{access_token}"}
    response = requests.get("https://api.servicem8.com/api_1.0/Job.json", headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch jobs", "response": response.json()}, status=400)


# region Web Hook
@csrf_exempt  # Disable CSRF for webhook handling
def servicem8_webhook(request):
    print('webhook')
    if request.method == "POST":
        try:
            print(request.POST)
            print(request.body)
            code = request.POST.get("challenge")
            print(code)
            # data = json.loads(request.body.decode("utf-8"))  # Parse JSON payload
            #
            # # Extract relevant information
            # event_type = data.get("event")
            # object_id = data.get("object_id")
            # object_type = data.get("object_type")
            #
            # # Handle different event types
            # if event_type == "job.update":
            #     # Process job update event
            #     print(f"Job Updated: {object_id}")
            #
            # elif event_type == "customer.create":
            #     # Process new customer event
            #     print(f"New Customer Created: {object_id}")

            # Return a success response
            # return JsonResponse({"message": "Webhook received"}, status=200)
            return HttpResponse(code, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
# endregion
