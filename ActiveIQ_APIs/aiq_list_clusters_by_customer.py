import os
import requests
import argparse
from dotenv import load_dotenv
from pprint import pprint


def get_api_token():
    """Retrieve the API token from environment variables."""
    api_token = os.getenv("AIQ_API_ACCESS_KEY")
    if not api_token:
        raise ValueError("API token not found. Please set the AIQ_API_ACCESS_KEY environment variable.")
    return api_token


def search_customers(api_token, search_term):
    """Search for customers using the ActiveIQ API."""
    # Set up the headers with the API token
    headers = {
        'accept': 'application/json',
        'authorizationToken': api_token
    }

    # Base URL for the ActiveIQ API
    base_url = 'https://api.activeiq.netapp.com/v1'

    # Encode the search term and construct the URL
    search_query = urllib.parse.quote(search_term)
    url = f'{base_url}/digital-advisor/customers?search={search_query}'

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}\n{response.text}")


def list_clusters_by_customer(api_token, customer_id):
    """List clusters for a specific customer using the ActiveIQ API."""
    # Set up the headers with the API token
    headers = {
        'accept': 'application/json',
        'authorizationToken': api_token
    }

    # Base URL for the ActiveIQ API
    base_url = 'https://api.activeiq.netapp.com/v1'

    # Construct the URL for the cluster discovery endpoint
    url = f'{base_url}/digital-advisor/cluster_discovery?customer={customer_id}'

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}\n{response.text}")


def main():
    """Main function to execute the script."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="List clusters for a specific customer using the ActiveIQ API.")
    parser.add_argument(
        "customer_id",
        type=str,
        help="The ID of the customer to list clusters for."
    )
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Get the API token
    api_token = get_api_token()

    # List clusters for the customer
    customer_id = args.customer_id
    try:
        clusters = list_clusters_by_customer(api_token, customer_id)
        pprint(clusters)  # Pretty print the response
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()