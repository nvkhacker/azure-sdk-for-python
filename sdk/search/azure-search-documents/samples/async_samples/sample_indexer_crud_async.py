# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to get, create, update, or delete an Indexer in Azure AI Search.

USAGE:
    python sample_indexers_operations_async.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_API_KEY - the admin key for your search service
    3) AZURE_STORAGE_CONNECTION_STRING - connection string for the Azure Storage account
"""

import asyncio
import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
key = os.environ["AZURE_SEARCH_API_KEY"]
connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
container_name = "hotels-sample-container"

async def create_indexer():
    # [START create_indexer_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.models import (
        SearchIndexerDataContainer,
        SearchIndexerDataSourceConnection,
        SearchIndex,
        SearchIndexer,
        SimpleField,
        SearchFieldDataType,
    )
    from azure.search.documents.indexes.aio import SearchIndexerClient, SearchIndexClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))
    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    # create an index
    index_name = "async-indexer-hotels"
    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="BaseRate", type=SearchFieldDataType.Double),
    ]
    index = SearchIndex(name=index_name, fields=fields)
    async with index_client:
        await index_client.create_index(index)

    # create a datasource
    container = SearchIndexerDataContainer(name=container_name)
    data_source_connection = SearchIndexerDataSourceConnection(
        name="async-indexer-datasource", type="azureblob", connection_string=connection_string, container=container
    )
    async with indexer_client:
        await indexer_client.create_data_source_connection(data_source_connection)

        # create an indexer
        indexer = SearchIndexer(
            name="async-sample-indexer",
            data_source_name="async-indexer-datasource",
            target_index_name="async-indexer-hotels",
        )
        result = await indexer_client.create_indexer(indexer)
        print(f"Create new Indexer - {result.name}")
    # [END create_indexer_async]


async def list_indexers():
    # [START list_indexer_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        result = await indexer_client.get_indexers()
    names = [x.name for x in result]
    print(f"Found {len(result)} Indexers in the service: {', '.join(names)}")
    # [END list_indexer_async]


async def get_indexer():
    # [START get_indexer_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        result = await indexer_client.get_indexer("async-sample-indexer")
    print(f"Retrieved Indexer '{result.name}'")
    return result
    # [END get_indexer_async]


async def get_indexer_status():
    # [START get_indexer_status_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        result = await indexer_client.get_indexer_status("async-sample-indexer")
    print(f"Retrieved Indexer status for 'async-sample-indexer'")
    return result
    # [END get_indexer_status_async]


async def run_indexer():
    # [START run_indexer_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        await indexer_client.run_indexer("async-sample-indexer")
    print("Ran the Indexer 'async-sample-indexer'")
    # [END run_indexer_async]
    return
    # [END run_indexer_async]


async def reset_indexer():
    # [START reset_indexer_async]
    await indexers_client.reset_indexer("async-sample-indexer")
    print("Reset the Indexer 'async-sample-indexer'")
    return
    # [END reset_indexer_async]


async def delete_indexer():
    # [START delete_indexer_async]
    await indexers_client.delete_indexer("async-sample-indexer")
    print("Indexer 'async-sample-indexer' successfully deleted")
    # [END delete_indexer_async]


async def main():
    await create_indexer()
    await list_indexers()
    await get_indexer()
    await get_indexer_status()
    await run_indexer()
    await reset_indexer()
    await delete_indexer()
    await indexers_client.close()


if __name__ == "__main__":
    asyncio.run(main())
