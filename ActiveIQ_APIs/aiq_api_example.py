import requests, os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_token = os.getenv("AIQ_API_ACCESS_TOKEN")

# Set up the headers with your API key
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# Base URL for the ActiveIQ API
base_url = 'https://api.activeiq.netapp.com/v1'

# Endpoint to fetch clusters for a specific customer
# Replace 'customer_id' with the actual customer ID
customer_id = urllib.parse.quote('Goldman Sachs')

# Construct the URL for the request
url = f'{base_url}/customers/{customer_id}/clusters'

# Make the request
response = requests.get(url, headers=headers)

# Check the response
# if response.status_code == 200:
#     systems = response.json()
#     for system in systems:
#         print(f"System ID: {system['id']}")
#         print(f"Name: {system['name']}")
#         print(f"Status: {system['status']}")
#         print('---')
# else:
#     print(f'Error: {response.status_code}')
#     print(response.text)

# Check the response
# if response.status_code == 200:
#     clusters = response.json()
#     for cluster in clusters['data']:  # Adjust based on actual response structure
#         print(f"Cluster ID: {cluster['id']}")
#         print(f"Name: {cluster['name']}")
#         print(f"Status: {cluster['status']}")
#         print('---')
# else:
#     print(f'Error: {response.status_code}')
#     print(response.text)

# Check the response
# if response.status_code == 200:
#     clusters = response.json()
#     # Adjust the following line based on the actual response structure
#     for cluster in clusters['data']:
#         print(f"Cluster Name: {cluster['name']}")
# else:
#     print(f'Error: {response.status_code}')
#     print(response.text)

# First, get the list of customers
url = f'{base_url}/customers'
response = requests.get(url, headers=headers)
print(response.json())  # Find the correct customer_id from this output
print(f"Status: {response.status_code}")
