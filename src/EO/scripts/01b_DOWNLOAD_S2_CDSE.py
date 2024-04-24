'''
Name: DOWNLOAD_S2_CDSE.py
Author: Alessio Di Lorenzo
Description: 
    Download S2 sample data from the Copernicus Data Space Ecosystem
    https://dataspace.copernicus.eu/
'''

import os
import requests
import json
from datetime import datetime
from GENERAL_CONFIG import download_dir

# Create download_dir if not exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Supply Copernicus Data Space Ecosystem credentials
username = input("Enter your CDSE username: ")
password = input("Enter your CDSE password: ")

# Auth token generation
auth_server_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
data = {
    "client_id": "cdse-public",
    "grant_type": "password",
    "username": username,
    "password": password,
}
response = requests.post(auth_server_url, data=data, verify=True, allow_redirects=False)
access_token = json.loads(response.text)["access_token"]

print('Access granted using CDSE token')

# Download Sample product using productId 
url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products(d4faeb89-2588-5423-806b-750e32b58257)/$value"
headers = {"Authorization": f"Bearer {access_token}"}
session = requests.Session()
session.headers.update(headers)
response = session.get(url, headers=headers, stream=True)

# Save as zipped archive
with open(os.path.join(download_dir, "S2A_MSIL2A_20220701T095041_N0400_R079_T33TVG_20220701T141709.zip"), "wb") as file:
    print('{}: Downloading sample Sentinel-2 archive from CDSE. Be patient, it might take a while...'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    file.write(response.content)
    print('{}: Download finished'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))