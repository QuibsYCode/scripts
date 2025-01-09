import requests
import base64

token_url = "https://api.umbrella.com/auth/v2/token"
client_id = "YOUR_CLIENT_ID"
client_secret =  "YOUR_CLIENT_SECRET"
orgID = [] # List of your organizations, if applicable

domains = "" # Add domains to check as a comma separated list, ex: google.com,youtube.com

credentials = f"{client_id}:{client_secret}"
access_token = base64.b64encode(credentials.encode()).decode()

for organization in orgID:
    # Set the organization name to human readable text
    orgName = ""
    if organization == orgID[0]:
            orgName = "ORG NAME"
    elif organization == orgID[1]:
            orgName = "ORG NAME"
    elif organization == orgID[2]:
            orgName = "ORG NAME"
    else:
        orgName = "Not Found"
    
    # Post the access token for the specific organization and retrieve the bearer token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Umbrella-OrgId': organization,
        'Authorization': f"Basic {access_token}",
    }
    token_url = "https://api.umbrella.com/auth/v2/token"
    response = requests.post(token_url, headers=headers)
    response_data = response.json()
    bearer_token = response_data.get("access_token")

    # Form the request, setting for 30 day history by default
    headers = {
        'Authorization': f"Bearer {bearer_token}",
    }
    params = {
        'to': 'now',
        'from': '-30days',
        'domains': domains,
    }
    url = f"https://reports.api.umbrella.com/v2/organizations/{organization}/summaries-by-destination/dns"
    response = requests.get(url, params=params, headers=headers)

    # Return the results, formatted as I like 
    if response.status_code == 200:
        print()
        print(f"{orgName}\n")
        response_data = response.json()
        for item in response_data['data']:
            domain = item['domain']
            request = item['summary']['requests']
            requestallow = item['summary']['requestsallowed']
            requestblock = item['summary']['requestsblocked']
            if (requestallow > 0 and requestblock == 0):
                domaincheck = f"{domain}: Allowed."
            if (requestallow == 0 and requestblock > 0):
                domaincheck = f"{domain}: Blocked."
            if (requestallow == 0 and requestblock == 0):
                domaincheck = f"{domain}: Selectively Proxied."
            if (requestallow and requestblock > 0):
                domaincheck = f"{domain}: Inconclusive"
            print()
            print(f"\t{domaincheck}")
            print(f"\t\tRequest Count: {request}")
            print(f"\t\tRequests Allowed: {requestallow}")
            print(f"\t\tRequests Blocked: {requestblock}")
            print()
    else:
        print(f"Error {response.status_code}: {response.text}")