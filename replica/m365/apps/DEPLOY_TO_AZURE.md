# Azure App Service Deployment Instructions

## 1. Prepare for Deployment
- Ensure your code is production-ready and requirements.txt is up to date.
- Set environment variables for AZURE_TENANT_ID and AZURE_CLIENT_ID (and any secrets) in Azure.

## 2. Deploy to Azure App Service

### a. Create a Resource Group (if needed)
```
az group create --name myResourceGroup --location eastus
```

### b. Create an App Service Plan
```
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
```

### c. Create a Web App
```
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name <your-app-name> --runtime "PYTHON|3.11"
```

### d. Deploy Code
```
az webapp deploy --resource-group myResourceGroup --name <your-app-name> --src-path .
```

### e. Set Environment Variables
```
az webapp config appsettings set --resource-group myResourceGroup --name <your-app-name> --settings AZURE_TENANT_ID=your-tenant-id AZURE_CLIENT_ID=your-client-id
```

### f. Configure Authentication (Optional)
- Set up Azure AD authentication in the Azure Portal for your web app for extra security.

## 3. Test Your API
- Visit `https://<your-app-name>.azurewebsites.net/api/health` to check health.
- Use the Power Platform connector or Graph Connector to connect to your deployed API.
