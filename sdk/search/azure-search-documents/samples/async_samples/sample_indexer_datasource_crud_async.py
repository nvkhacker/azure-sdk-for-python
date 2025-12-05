# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to get, create, update, or delete a Data Source Connection in Azure AI Search.

USAGE:
    python sample_indexer_datasource_crud_async.py

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

async def create_data_source_connection():
    # [START create_data_source_connection_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.models import SearchIndexerDataContainer, SearchIndexerDataSourceConnection
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    container = SearchIndexerDataContainer(name=container_name)
    data_source = SearchIndexerDataSourceConnection(
        name="async-sample-data-source-connection",
        type="azureblob",
        connection_string=connection_string,
        container=container,
    )
    async with indexer_client:
        result = await indexer_client.create_data_source_connection(data_source)
    print(f"Create new Data Source Connection - {result.name}")
    # [END create_data_source_connection_async]


async def list_data_source_connections():
    # [START list_data_source_connection_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        result = await indexer_client.get_data_source_connections()
    names = [x.name for x in result]
    print(f"Found {len(result)} Data Source Connections in the service: {', '.join(names)}")
    # [END list_data_source_connection_async]


async def get_data_source_connection():
    # [START get_data_source_connection_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        result = await indexer_client.get_data_source_connection("async-sample-data-source-connection")
    print(f"Retrieved Data Source Connection '{result.name}'")
    return result
    # [END get_data_source_connection_async]


async def delete_data_source_connection():
    # [START delete_data_source_connection_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    async with indexer_client:
        await indexer_client.delete_data_source_connection("async-sample-data-source-connection")
    print("Data Source Connection 'async-sample-data-source-connection' successfully deleted")
    # [END delete_data_source_connection_async]


async def main():
    await create_data_source_connection()
    await list_data_source_connections()
    await get_data_source_connection()
    await delete_data_source_connection()


if __name__ == "__main__":
    asyncio.run(main())
