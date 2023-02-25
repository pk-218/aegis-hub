import requests

print(requests.get("https://www.abuseipdb.com/check/142.250.192.110/json?key=aa2e90299f95874a4325793eb2316b7c94f24044ff2dbc6edb75f14c26ebc4fbe8ed136750c3ca64&days=1").content)