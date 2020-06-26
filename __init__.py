# Import standard libraries
import os
import sys
import re
import logging
import requests

# Import third-party libraries
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from msal import ConfidentialClientApplication
from azure.identity import DefaultAzureCredential

# Configure the key variables
TENANT_NAME =  # YOUR TENANT NAME
CLIENT_ID =  # CLIENT ID OF YOUR SERVICE PRINCIPAL
SCOPES = ['https://management.azure.com//.default']
PRIVATE_KEY_LOCATION =  # THE FULL PATH OF YOUR PRIVATE KEY
CERTIFICATE_LOCATION =  # THE FULL PATH OF YOUR CERTIFICATE

# Create a logging mechanism
def enable_logging():
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

# obtain an access token
def get_sp_access_token(client_id, client_credential, tenant_name, scopes):
    logging.info('Attempting to obtain an access token...')
    result = None
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_credential,
        authority=f"https://login.microsoftonline.com/{tenant_name}"
    )
    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        logging.info('Access token successfully acquired')
        return result['access_token']
    else:
        logging.error('Unable to obtain access token')
        logging.error(f"Error was: {result['error']}")
        logging.error(f"Error description was: {result['error_description']}")
        logging.error(f"Error correlation_id was: {result['correlation_id']}")
        raise Exception('Failed to obtain access token')


def main():
    try:
        # Enable logging
        enable_logging()

        # Read in the private key and certificate
        with open(PRIVATE_KEY_LOCATION) as file:
            private_key = file.read()

        with open(CERTIFICATE_LOCATION) as file:
            public_certificate = file.read()

        # Create an X509 object and calculate the thumbprint
        cert = load_pem_x509_certificate(data=bytes(
            public_certificate, 'UTF-8'), backend=default_backend())
        thumbprint = (cert.fingerprint(hashes.SHA1()).hex())

        # Obtain an access token using MSAL
        mytoken = get_sp_access_token(
            client_id=CLIENT_ID,
            client_credential={
                "private_key": private_key,
                "thumbprint": thumbprint,
                "public_certificate": public_certificate
            },
            tenant_name=TENANT_NAME,
            scopes=SCOPES
        )

    print(mytoken)

    except Exception:
        logging.error('Execution error: ', exc_info=True)


if __name__ == "__main__":
    main()
