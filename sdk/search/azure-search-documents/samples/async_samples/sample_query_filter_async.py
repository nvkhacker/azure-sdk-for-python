# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to filter and order search results from an Azure AI Search index.

USAGE:
    python sample_query_filter_async.py

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


async def filter_query():
    # [START filter_query_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.aio import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    async with search_client:
        results = await search_client.search(
            search_text="WiFi",
            filter="Address/StateProvince eq 'FL' and Address/Country eq 'USA'",
            select=["HotelName", "Rating"],
            order_by=["Rating desc"],
        )

        print("Florida hotels containing 'WiFi', sorted by Rating:")
        async for result in results:
            print(f"    Name: {result['HotelName']} (rating {result['Rating']})")
    # [END filter_query_async]


if __name__ == "__main__":
    asyncio.run(filter_query())
