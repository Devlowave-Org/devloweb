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

funasitien_token = "ezguCO13VxsWexqZBqbwVPCS0pzz2DGI5XrtWuCH"
devlowave_token = "98_GC0fWd9qsA_8lRkDp6aQVkgQrWk4STUPxxHFp"


def get_domain_id(domain):
    url = f"https://api.cloudflare.com/client/v4/zones"
    response = requests.get(url, headers=requests_headers)
    if response.status_code == 200:
        data = response.json()
        if data["result"]:
            for result in data['result']:
                if result['name'] == domain:
                    return result['id']
    return None

def create_subdomain(ja_name, target_ip, domain):
    domainid = get_domain_id(domain)
    url = f"https://api.cloudflare.com/client/v4/zones/{domainid}/dns_records"
    response = (
        requests.post(
            url=url,
            headers=requests_headers,
            data=json.dumps(
                {
                    "content": target_ip,
                    "name": ja_name,
                    "type": "A",
                    "proxied": True
                }
            )
        )
    )
    if response.status_code == 200:
        return True
    else:
        return response.json()
    
def list_subdomains(id):
    response = requests.get(url=f"https://api.cloudflare.com/client/v4/zones/{id}/dns_records", headers=requests_headers)
    return response.json()

def subdomain_exist(subdomain_name, domain):
    subdomains = list_subdomains(get_domain_id(domain))
    for subdomain in subdomains['result']:
        if subdomain['name'] == f"{subdomain_name.lower()}.{domain.lower()}":
            return True
    return False


def delete_subdomain(name, domain):
    domainid = get_domain_id(domain)
    subdomains = list_subdomains(domainid)
    url = f"https://api.cloudflare.com/client/v4/zones/{domainid}/dns_records"
    # Check if the name = an id and use the id to send a delete request.
    for i in range(len(subdomains)):
        if subdomains['result'][i]['name'] == f"{name.lower()}.{domain.lower()}":
            response = requests.delete(url=url,
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
