# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to authenticate with the Azure AI Search service.

USAGE:
    python sample_authentication.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the admin key for your search service
"""

import os


def authentication_with_api_key_credential():
    # [START create_search_client_with_key]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    # [END create_search_client_with_key]

    document_count = search_client.get_document_count()

    print(f"There are {document_count} documents in the '{index_name}' search index.")


def authentication_service_client_with_api_key_credential():
    # [START create_search_service_client_with_key]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    search_index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    # [END create_search_service_client_with_key]

    result = search_index_client.list_indexes()
    names = [x.name for x in result]
    print(f"Found {len(names)} search indexes: {', '.join(names)}")


def authentication_with_aad():
    # [START authentication_with_aad]
    from azure.identity import DefaultAzureCredential
    from azure.search.documents import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    credential = DefaultAzureCredential()

    search_client = SearchClient(service_endpoint, index_name, credential)
    # [END authentication_with_aad]

    document_count = search_client.get_document_count()

    print(f"There are {document_count} documents in the '{index_name}' search index.")


def authentication_service_client_with_aad():
    # [START authentication_service_client_with_aad]
    from azure.identity import DefaultAzureCredential
    from azure.search.documents.indexes import SearchIndexClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    credential = DefaultAzureCredential()

    search_index_client = SearchIndexClient(service_endpoint, credential)
    # [END authentication_service_client_with_aad]

    result = search_index_client.list_indexes()
    names = [x.name for x in result]
    print(f"Found {len(names)} search indexes: {', '.join(names)}")


if __name__ == "__main__":
    authentication_with_api_key_credential()
    authentication_service_client_with_api_key_credential()
    authentication_with_aad()
    authentication_service_client_with_aad()
