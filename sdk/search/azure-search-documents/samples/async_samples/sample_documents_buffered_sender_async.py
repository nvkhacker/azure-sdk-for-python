# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates buffering upload, merge, and delete operations with SearchIndexingBufferedSender.

USAGE:
    python sample_documents_buffered_sender_async.py

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

async def sample_batching_client():
    # [START sample_batching_client_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchIndexingBufferedSender

    document = {
        "Category": "Hotel",
        "HotelId": "1000",
        "Rating": 4.0,
        "Rooms": [],
        "HotelName": "Azure Inn",
    }

    async with SearchIndexingBufferedSender(service_endpoint, index_name, AzureKeyCredential(key)) as buffered_sender:
        # add upload actions
        await buffered_sender.upload_documents(documents=[document])
        print(f"Uploaded document {document['HotelId']}")
        
        # add merge actions
        await buffered_sender.merge_documents(documents=[{"HotelId": "1000", "Rating": 4.5}])
        print(f"Merged document {document['HotelId']}")
        
        # add delete actions
        await buffered_sender.delete_documents(documents=[{"HotelId": "1000"}])
        print(f"Deleted document {document['HotelId']}")
    # [END sample_batching_client_async]


async def main():
    await sample_batching_client()


if __name__ == "__main__":
    asyncio.run(main())
