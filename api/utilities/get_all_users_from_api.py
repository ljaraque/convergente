import requests

# Replace this URL with the base URL of your API
base_url = 'http://localhost:8000/api/'

# Replace 'your_username' and 'your_password' with the actual credentials
username = 'Neo1'
password = '1234'

# Replace this URL with the URL of your token authentication endpoint
token_auth_url = 'http://localhost:8000/api/token/'

# Obtain the token
response = requests.post(token_auth_url, data={
    'username': username,
    'password': password,
})

if response.status_code == 200:
    token = response.json()['access']
    print(f'Token: {token}')
    # then get refresh token in case token expires
    refresh_token = response.json()['refresh']
    print(f'Refresh Token:{refresh_token}')

    # Use the token to access the API
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Replace 'your_api_endpoint' with the actual endpoint you want to access
    endpoint = 'usuarios'
    api_url = f'{base_url}{endpoint}/'
    print(api_url)

    # Make a GET request to the API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for element in data:
            print(element['id'], element['username'], element['password'])
    else:
        print(f'Failed to access the API. Status code: {response.status_code}')
else:
    print(f'Failed to obtain token. Status code: {response.status_code}')