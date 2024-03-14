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
    if response.status_code == 200:
        return "200 - Domain created successfully"
    else:
        return f"response : {response}; detailed : {response.json()}"


def list_subdomains():
    response = requests.get(url=requests_URL, headers=requests_headers)
    return response.json()


def delete_subdomain(ja_name):
    subdomains = list_subdomains()

    # Check if the name = an id and use the id to send a delete request.
    for i in range(len(subdomains)):
        if subdomains['result'][i]['name'] == f"{ja_name}.devlowave.fr":
            response = requests.delete(url=f"{requests_URL}/{subdomains['result'][i]['id']}",
                                       headers=requests_headers
                                       )
            if response.status_code == 200:
                return "200 - Domain deleted successfully"
            else:
                return f"response : {response}; detailed : {response.json()}"

    # If no id was found for this name
    return "This name wasn't found in the subdomains"


if __name__ == "__main__":
    response = create_subdomain("rickroll", "82.64.89.33")
    print(response)

    response = delete_subdomain("rickroll")
    print(response)
