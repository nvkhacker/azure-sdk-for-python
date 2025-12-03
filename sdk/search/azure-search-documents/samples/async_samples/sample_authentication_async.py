# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_authentication_async.py
DESCRIPTION:
    This sample demonstrates how to authenticate with the Azure Congnitive Search
    service with an API key. See more details about authentication here:
    https://learn.microsoft.com/azure.search.documents/search-security-api-keys
USAGE:
    python sample_authentication_async.py
    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import asyncio
import os


async def authentication_with_api_key_credential_async():
    # [START create_search_client_with_key_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    # [END create_search_client_with_key_async]

    async with search_client:
        result = await search_client.get_document_count()

    print("There are {} documents in the {} search index.".format(result, index_name))


async def authentication_service_client_with_api_key_credential_async():
    # [START create_search_service_with_key_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    # [END create_search_service_with_key_async]


async def authentication_with_aad():
    # [START authentication_with_aad]
    from azure.identity.aio import DefaultAzureCredential
    from azure.search.documents.aio import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    credential = DefaultAzureCredential()

    search_client = SearchClient(service_endpoint, index_name, credential)
    # [END authentication_with_aad]

    async with search_client:
        result = await search_client.get_document_count()

    print("There are {} documents in the {} search index.".format(result, index_name))


async def authentication_service_client_with_aad():
    # [START authentication_service_client_with_aad]
    from azure.identity.aio import DefaultAzureCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    credential = DefaultAzureCredential()

    client = SearchIndexClient(service_endpoint, credential)
    # [END authentication_service_client_with_aad]


if __name__ == "__main__":
    asyncio.run(authentication_with_api_key_credential_async())
    asyncio.run(authentication_service_client_with_api_key_credential_async())
    asyncio.run(authentication_with_aad())
    asyncio.run(authentication_service_client_with_aad())
