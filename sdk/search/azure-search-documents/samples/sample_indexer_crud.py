# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to create, get, update, and delete an indexer.

USAGE:
    python sample_indexer_crud.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_API_KEY - the admin key for your search service
    3) AZURE_STORAGE_CONNECTION_STRING - connection string for the Azure Storage account
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
key = os.environ["AZURE_SEARCH_API_KEY"]
connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
container_name = "hotels-sample-container"
index_name = "sample-index"
data_source_name = "sample-datasource"
indexer_name = "sample-indexer"

def create_indexer():
    # [START create_indexer]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
    from azure.search.documents.indexes.models import (
        SearchIndexerDataContainer,
        SearchIndexerDataSourceConnection,
        SearchIndex,
        SearchIndexer,
        SimpleField,
        SearchFieldDataType,
    )

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))
    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    # create an index
    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="BaseRate", type=SearchFieldDataType.Double),
    ]
    index = SearchIndex(name=index_name, fields=fields)
    index_client.create_index(index)

    # create a datasource
    container = SearchIndexerDataContainer(name=container_name)
    data_source_connection = SearchIndexerDataSourceConnection(
        name=data_source_name, type="azureblob", connection_string=connection_string, container=container
    )
    indexer_client.create_data_source_connection(data_source_connection)

    # create an indexer
    indexer = SearchIndexer(
        name=indexer_name, data_source_name=data_source_name, target_index_name=index_name
    )
    result = indexer_client.create_indexer(indexer)
    print(f"Create new Indexer - {result.name}")
    # [END create_indexer]


def list_indexers():
    # [START list_indexer]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    result = indexer_client.get_indexers()
    names = [x.name for x in result]
    print(f"Found {len(result)} Indexers in the service: {', '.join(names)}")
    # [END list_indexer]


def get_indexer():
    # [START get_indexer]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    result = indexer_client.get_indexer(indexer_name)
    print(f"Retrieved Indexer '{result.name}'")
    return result
    # [END get_indexer]


def get_indexer_status():
    # [START get_indexer_status]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    result = indexer_client.get_indexer_status(indexer_name)
    print(f"Retrieved Indexer status for '{indexer_name}'")
    return result
    # [END get_indexer_status]


def run_indexer():
    # [START run_indexer]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))

    indexer_client.run_indexer(indexer_name)
    print(f"Ran the Indexer '{indexer_name}'")
    # [END run_indexer]


def reset_indexer():
    # [START reset_indexer]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))
    result = indexer_client.reset_indexer(indexer_name)
    print(f"Reset the Indexer '{indexer_name}'")
    return result
    # [END reset_indexer]


def clean_up_resources():
    # [START clean_up_resources]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexerClient, SearchIndexClient

    indexer_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))
    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    indexer_client.delete_indexer(indexer_name)
    print(f"Indexer '{indexer_name}' successfully deleted")

    indexer_client.delete_data_source_connection(data_source_name)
    print(f"Data Source '{data_source_name}' successfully deleted")

    index_client.delete_index(index_name)
    print(f"Index '{index_name}' successfully deleted")
    # [END clean_up_resources]


if __name__ == "__main__":
    create_indexer()
    list_indexers()
    get_indexer()
    get_indexer_status()
    run_indexer()
    reset_indexer()
    clean_up_resources()
