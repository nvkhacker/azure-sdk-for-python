# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to upload, merge, get, and delete documents in an Azure AI Search index.

USAGE:
    python sample_documents_crud_async.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the admin key for your search service
"""

import os
import asyncio

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

async def upload_document():
    # [START upload_document_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    document = {
        "HotelId": "1000",
        "HotelName": "Azure Inn",
    }

    async with search_client:
        result = await search_client.upload_documents(documents=[document])

    print(f"Upload of new document succeeded: {result[0].succeeded}")
    # [END upload_document_async]


async def merge_document():
    # [START merge_document_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    async with search_client:
        result = await search_client.merge_documents(documents=[{"HotelId": "1000", "HotelName": "Renovated Ranch"}])

    print(f"Merge into new document succeeded: {result[0].succeeded}")
    # [END merge_document_async]


async def get_document():
    # [START get_document_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    async with search_client:
        result = await search_client.get_document(key="1000")

        print("Details for hotel '1000' are:")
        print(f"        Name: {result['HotelName']}")
    # [END get_document_async]


async def delete_document():
    # [START delete_document_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    async with search_client:
        result = await search_client.delete_documents(documents=[{"HotelId": "1000"}])

    print(f"Delete new document succeeded: {result[0].succeeded}")
    # [END delete_document_async]


async def main():
    await upload_document()
    await merge_document()
    await get_document()
    await delete_document()


if __name__ == "__main__":
    asyncio.run(main())
