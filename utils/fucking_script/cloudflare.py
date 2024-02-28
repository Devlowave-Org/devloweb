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
def create_subdomains(ja_name, target_ip):
    response1 = (
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
    """
    response2 = (
        requests.post
        (
            url=requests_URL,
            headers=requests_headers,
            data=json.dumps
            ({
                "content": f"{ja_name}.devlowave.fr",
                "name": f"www.{ja_name}",
                "type": "CNAME",
                "proxied": True
            })
        )
    )
    """
    print(response1.json())
    #print(response2.json())


def list_subdomains():
    response = requests.get(url=requests_URL, headers=requests_headers)
    return response.json()
