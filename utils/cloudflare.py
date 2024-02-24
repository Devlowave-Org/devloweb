import requests
import json

class CloudFlareApi:
    def __init__(self):
        self.base = f'https://api.cloudflare.com/client/v4/'

    def creer_sous_domaine(self, name, ip):
        response = requests.post(url="https://api.cloudflare.com/client/v4/zones/fa0c29fb12a1e4c7b505fe000aebd454/dns_records",
                                 headers={"Authorization": "Bearer 98_GC0fWd9qsA_8lRkDp6aQVkgQrWk4STUPxxHFp", "Content-Type": "application/json"},
                                 data=json.dumps({"content": ip,
                                       "name": name,
                                       "type": "A"}))
        print(response.json())


    def liste_sous_domaines(self):
        """
        curl --request GET \
          --url https://api.cloudflare.com/client/v4/zones/zone_id/dns_records \
          --header 'Content-Type: application/json' \
          --header 'X-Auth-Email: '
        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records

        :return:
        """
        response = requests.get(url="https://api.cloudflare.com/client/v4/zones/fa0c29fb12a1e4c7b505fe000aebd454"
                                "/dns_records", headers={"Authorization": "Bearer 98_GC0fWd9qsA_8lRkDp6aQVkgQrWk4STUPxxHFp",
                                                         "Content-Type": "application/json"})
        return response.json()


if __name__ == '__main__':
    cloudflare = CloudFlareApi()
    cloudflare.liste_sous_domaines()
    cloudflare.creer_sous_domaine("pipi", "127.0.0.1")
