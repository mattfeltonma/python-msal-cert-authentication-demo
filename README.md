# Python MSAL Certificate Authentication
This solution demonstrates how to use a client certificate stored with the [Microsoft Authentication Library (MSAL)](https://docs.microsoft.com/en-us/azure/active-directory/develop/msal-overview).  It is coded in Python 3.

## What problem does this solve?
Azure AD Service Principals are used for non-human access to Microsoft Azure resources.  A client secret (or password) is often used as the means to authenticate the service principal to Azure AD.  Client secrets are often mistakenly published in code or shared among developers.  Azure AD also supports using client certificates to authenticate a service principal.  This can provide a higher level of assurance of the service principal's identity and address the risks of traditional password-based authentication.

## Requirements

### Resources
* A standard Azure AD [service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals) which has been configured to use the (certificate for authentication)[https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#certificates-and-secrets].
* A locally stored private key and certificate

## Setup
1. Use pip to install the required libraries.
2. Modify __init__.py to provide the required variables.
3. Run the solution.
