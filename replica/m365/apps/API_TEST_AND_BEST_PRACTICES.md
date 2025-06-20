# Azure AD App Credentials and API Test Instructions (Best Practices)

## Credentials (Do NOT commit this file to source control)
- **Tenant ID:** [YOUR_TENANT_ID]
- **Client ID:** [YOUR_CLIENT_ID]
- **Client Secret:** [YOUR_CLIENT_SECRET]

## Usage
These credentials are for local testing only. Store secrets securely (e.g., Azure Key Vault) in production. Rotate secrets regularly.

## PowerShell Script to Test API
```powershell
$tenantId = "[YOUR_TENANT_ID]"
$clientId = "[YOUR_CLIENT_ID]"
$clientSecret = "[YOUR_CLIENT_SECRET]"
$scope = "api://[YOUR_CLIENT_ID]/.default"
$apiUrl = "https://boopas-graph-connector-api.azurewebsites.net/"

$body = @{
    client_id     = $clientId
    scope         = $scope
    client_secret = $clientSecret
    grant_type    = "client_credentials"
}
$tokenResponse = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" -Body $body
$accessToken = $tokenResponse.access_token

$response = Invoke-RestMethod -Uri $apiUrl -Headers @{ Authorization = "Bearer $accessToken" }
$response
```

## Best Practices for Production
1. Use Azure Key Vault for secrets
2. Implement proper error handling and logging
3. Use managed identities where possible
4. Rotate credentials regularly
5. Monitor API usage and authentication failures
