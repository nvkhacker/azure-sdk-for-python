# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to get, create, update, or delete a Synonym Map.
USAGE:
    python sample_index_synonym_map_crud_async.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import asyncio
import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
key = os.environ["AZURE_SEARCH_API_KEY"]


async def create_synonym_map():
    # [START create_synonym_map_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient
    from azure.search.documents.indexes.models import SynonymMap

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    synonyms = [
        "USA, United States, United States of America",
        "Washington, Wash. => WA",
    ]
    synonym_map = SynonymMap(name="test-syn-map", synonyms=synonyms)
    async with index_client:
        result = await index_client.create_synonym_map(synonym_map)
    print(f"Create new Synonym Map '{result.name}' succeeded")
    # [END create_synonym_map_async]


async def get_synonym_maps():
    # [START get_synonym_maps_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    async with index_client:
        result = await index_client.get_synonym_maps()
    names = [x.name for x in result]
    print(f"Found {len(result)} Synonym Maps in the service: {', '.join(names)}")
    # [END get_synonym_maps_async]


async def get_synonym_map():
    # [START get_synonym_map_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    async with index_client:
        result = await index_client.get_synonym_map("test-syn-map")
    print("Retrived Synonym Map 'test-syn-map' with synonyms")
    if result:
        for syn in result.synonyms:
            print(f"    {syn}")
    # [END get_synonym_map_async]


async def delete_synonym_map():
    # [START delete_synonym_map_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    async with index_client:
        await index_client.delete_synonym_map("test-syn-map")
    print("Synonym Map 'test-syn-map' deleted")
    # [END delete_synonym_map_async]


async def main():
    await create_synonym_map()
    await get_synonym_maps()
    await get_synonym_map()
    await delete_synonym_map()


if __name__ == "__main__":
    asyncio.run(main())
