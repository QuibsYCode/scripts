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
    print(orgName)
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
    for domain in domains:
        params = {
            'to': 'now',
            'from': '-30days',
            'limit': '100',
            'domains': domain,
        }

        response = requests.get('https://api.umbrella.com/reports/v2/activity/dns', params=params, headers=headers)
        if response.status_code == 200:
            request_count = 0
            allowed_verdict = 0
            blocked_verdict = 0
            proxy_verdict = 0
            final_verdict = "No Traffic Found"
            results = []
            abnormal = {}
            response_data = response.json()
            for item in response_data['data']:

                checked_domain = item['domain']
                if checked_domain == domain:
                    request_count += 1
                verdict = item['verdict']
                if verdict == "allowed":
                    allowed_verdict += 1
                if verdict == "blocked":
                    blocked_verdict += 1
                if verdict == "proxied":
                    proxy_verdict += 1
                if (request_count != 0):
                    if (allowed_verdict > 0 and proxy_verdict == 0 and blocked_verdict == 0):
                        final_verdict = f"Allowed. Count: {allowed_verdict}"
                    elif (allowed_verdict == 0 and proxy_verdict == 0 and blocked_verdict > 0):
                        final_verdict = f"Blocked. Count: {blocked_verdict}"
                    elif (allowed_verdict == 0 and proxy_verdict > 0 and blocked_verdict == 0):
                        final_verdict = f"Proxied. Count: {proxy_verdict}"
                    else:
                        final_verdict = f"Undetermined. Allowed Count: {allowed_verdict}, Blocked Count: {blocked_verdict}, Proxied Count: {proxy_verdict}"
            print(f"\t{domain}:\t{final_verdict}")