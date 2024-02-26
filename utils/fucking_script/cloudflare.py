"""IMPORTS"""
import requests
import json


"""GLOBAL VARS"""
API_base_url = f'https://api.cloudflare.com/client/v4/'

# To make requests more readable
requests_headers = {
    "Authorization": "Bearer 98_GC0fWd9qsA_8lRkDp6aQVkgQrWk4STUPxxHFp",
    "Content-Type": "application/json"
}
requests_URL = "https://api.cloudflare.com/client/v4/zones/fa0c29fb12a1e4c7b505fe000aebd454/dns_records"


"""CODE"""
# Basically API calls
def create_subdomain(ja_name, target_ip):
    response = (
        requests.post
        (
            url=requests_URL,
            headers=requests_headers,
            data=json.dumps
            ({
                "content": target_ip,
                "name": ja_name,
                "type": "A",
                "proxied": True
            })
        )
    )
    print(response.json())


def list_subdomains():
    response = requests.get(url=requests_URL, headers=requests_headers)
    return response.json()


# Idk why this is here but timtonix put it her so it must be for a reason
"""
curl --request GET \
  --url https://api.cloudflare.com/client/v4/zones/zone_id/dns_records \
  --header 'Content-Type: application/json' \
  --header 'X-Auth-Email: '
https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records

:return:
"""
