# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import os
import boto3

migrate_from = "https://debian-pingfed:9999/pf-admin-api/v1"

#Pull secret from secrets manager
def get_secret(secret_name):
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    secret_response = client.get_secret_value(
        SecretId=secret_name
    )
    secrets = json.loads(secret_response['SecretString'])
    return secrets


with open("apiCalls.json") as f:
    endpoint = json.load(f)

session = requests.Session()
secrets = get_secret('debian-pf-api-secret')
session.auth = (secrets["username"], secrets["pass"])
session.headers.update({'X-XSRF-Header': 'PingFederate'})
session.headers.update({'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br'})
session.verify = False
#Create a directory for the artifacts in the current working directory
file_path = os.getcwd()
final_path = os.path.join(file_path, r'artifactsPull')
cert_path = os.path.join(final_path, r'certs')
if not os.path.exists(final_path):
    os.makedirs(os.path.join(file_path, r'artifactsPull'))

if not os.path.exists(cert_path):
    os.makedirs(os.path.join(final_path, f'certs'))
def make_calls():
    global clients, spConnections, authPolicies, authenticationPolicyFragments, idpAdapters, passwordCVs, accessTokenManagers, accessTokenMappings,\
        authPolicyContracts, dataStores, keyPairs
    get_secret('debian-pf-api-secret')
    clients = session.get(migrate_from + endpoint["oauthClients"]["endpoint"]).json()
    spConnections = session.get(migrate_from + endpoint["spConnections"]["endpoint"]).json()
    authPolicies = session.get(migrate_from + endpoint["authPolicies"]["endpoint"]).json()
    idpAdapters = session.get(migrate_from + endpoint["idpAdapters"]["endpoint"]).json()
    passwordCVs = session.get(migrate_from + endpoint["passwordCredentialValidators"]["endpoint"]).json()
    accessTokenManagers = session.get(migrate_from + endpoint["accessTokenManagers"]["endpoint"]).json()
    accessTokenMappings = session.get(migrate_from + endpoint["accessTokenMappings"]["endpoint"]).json()
    authPolicyContracts = session.get(migrate_from + endpoint["authPolicyContracts"]["endpoint"]).json()
    dataStores = session.get(migrate_from + endpoint["dataStores"]["endpoint"]).json()
    keyPairs = session.get(migrate_from + endpoint["keyPairs"]["endpoint"]).json()
    authenticationPolicyFragments = session.get(migrate_from +
                                                endpoint["authenticationPolicyFragments"]["endpoint"]).json()

def write_to_file():
    list_thing = [clients, spConnections, authPolicies, authenticationPolicyFragments, idpAdapters, passwordCVs, accessTokenManagers,
                  accessTokenMappings, authPolicyContracts, dataStores, keyPairs]
    file_names = ["clients", "spConnections", "authPolicies", "authenticationPolicyFragments", "idpAdapters", "passwordCredentialValidators",
                  "accessTokenManagers", "accessTokenMappings", "authPolicyContracts", "dataStores", "keyPairs"]
    for name, obj in zip(file_names, list_thing):
        f = open(f"{final_path}/{name}.json", 'w+')
        f.write(json.dumps(obj, indent=3))
        f.close()

make_calls()
write_to_file()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
