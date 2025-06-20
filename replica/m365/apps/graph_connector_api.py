from flask import Flask, jsonify, request
import os
import jwt
import requests
from functools import wraps

app = Flask(__name__)

# Example data to expose to Microsoft 365
DATA = [
    {"id": "1", "title": "Sample Record 1", "description": "This is a test record."},
    {"id": "2", "title": "Sample Record 2", "description": "Another test record."}
]

# Azure AD config (use actual values for deployment)
TENANT_ID = os.environ.get("AZURE_TENANT_ID", "44be3eea-1c8f-4779-a077-0f28cc610be3")
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "724262c0-a25f-4da1-a82e-253c32c3d6c0")
ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL = f"{ISSUER}/discovery/v2.0/keys"

# Cache JWKS keys
def get_jwks():
    if not hasattr(get_jwks, "_jwks"):
        get_jwks._jwks = requests.get(JWKS_URL).json()
    return get_jwks._jwks

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth.split(' ')[1]
        try:
            jwks = get_jwks()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if not rsa_key:
                raise Exception('No matching key found')
            payload = jwt.decode(
                token,
                key=jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key),
                algorithms=['RS256'],
                audience=CLIENT_ID,
                issuer=ISSUER
            )
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

# Endpoint for Microsoft Graph Connector to fetch data
@app.route('/api/items', methods=['GET'])
@token_required
def get_items():
    return jsonify(DATA)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
