import os
import jwt
import requests
import uuid
from datetime import datetime, timezone

# Fetch environment variables
private_key = os.getenv('PRIVATE_KEY')
iss = os.getenv('ISS')
kid = os.getenv('KID')

if not all([private_key, iss, kid]):
    raise EnvironmentError("Ensure all environment variables are set: PRIVATE_KEY, ISS, KID")

timestamp = int(datetime.now(timezone.utc).timestamp())

audience = 'https://test.maskinporten.no/'
token_endpoint = audience + 'token'

jwt_headers = {
    'alg': 'RS256',
    'typ': 'JWT',
    'kid': kid
}

claims = {
    'aud': audience,
    'iss': iss,
    'scope': 'kartverk:nrl.uthenting',
    'iat': timestamp,
    'exp': timestamp + 100,
    'jti': str(uuid.uuid4())
}

# Generate the JWT token
jwt_token = jwt.encode(
    claims,
    private_key,
    algorithm='RS256',
    headers=jwt_headers
)

print("JWT Token:", jwt_token)

# Make the POST request with the JWT token
response = requests.post(
    token_endpoint,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token
    }
)

print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
