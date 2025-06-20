# Microsoft 365 Graph Connector API

This Flask API is designed to be used as a custom Microsoft Graph Connector for Microsoft 365 Copilot and Microsoft Search.

## Features & Best Practices
- Exposes a REST endpoint for Microsoft 365 to read data.
- Ready for Azure AD authentication (add token validation for production).
- Health check endpoint for monitoring.
- Follows least-privilege and secure coding recommendations.

## Usage
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the API:
   ```sh
   python graph_connector_api.py
   ```
3. Register this endpoint as a custom Graph Connector in the Microsoft 365 admin center.
4. Link to your Azure AD app registration and grant required permissions.

## Security
- For production, implement Azure AD token validation in `validate_token()`.
- Store secrets in environment variables or Azure Key Vault.
- Use HTTPS in production.

## Extending
- Add more endpoints or connect to your real data sources as needed.
