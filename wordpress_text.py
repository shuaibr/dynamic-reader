# import requests

# # Define the base URL of your WordPress site
# base_url = 'https://reeyaz.ca/wp-json/wp/v2/'

# # Define your API token (JWT token or other authentication method)
# api_token = 'your-api-token'

# # Set the headers for the API request
# headers = {
#     'Authorization': 'Bearer ' + api_token,
#     'Content-Type': 'application/json',
# }

# # Define the endpoint you want to access, e.g., 'posts' for blog posts
# endpoint = 'posts'

# # Make a GET request to retrieve data
# response = requests.get(base_url + endpoint, headers=headers)

# # Check the response status code
# if response.status_code == 200:
#     # Request was successful
#     data = response.json()
#     # Process the data here
#     for item in data:
#         print(item)
# else:
#     # Request failed
#     print(f"Request failed with status code: {response.status_code}")

import requests
import os

api_url = 'https://reeyaz.ca/wp-json'
token_url = f'{api_url}/jwt-auth/v1/token'

WP_USER = os.getenv('WP_USER')
WP_PASS = os.getenv('WP_PASS')

data = {
    'username': WP_USER,
    'password': WP_PASS
}

try:
    response = requests.post(token_url, json=data)
    response.raise_for_status()  # Check for HTTP errors

    token_data = response.json()
    print(token_data)
except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
