# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to get, create, update, or delete an index in Azure AI Search.

USAGE:
    python sample_index_crud_async.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_API_KEY - the admin key for your search service
"""


import os
import asyncio
from typing import List

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
key = os.environ["AZURE_SEARCH_API_KEY"]

async def create_index():
    # [START create_index_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient
    from azure.search.documents.indexes.models import (
        ComplexField,
        CorsOptions,
        SearchIndex,
        ScoringProfile,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
    )

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    name = "hotels"
    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="HotelName", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="BaseRate", type=SearchFieldDataType.Double),
        SearchableField(name="Description", type=SearchFieldDataType.String, collection=True),
        ComplexField(
            name="Address",
            fields=[
                SimpleField(name="StreetAddress", type=SearchFieldDataType.String),
                SimpleField(name="City", type=SearchFieldDataType.String),
            ],
            collection=True,
        ),
    ]

    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles: List[ScoringProfile] = []
    index = SearchIndex(name=name, fields=fields, scoring_profiles=scoring_profiles, cors_options=cors_options)

    async with index_client:
        result = await index_client.create_index(index)
    print(f"Created index '{result.name}'")
    # [END create_index_async]


async def get_index():
    # [START get_index_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    name = "hotels"
    async with index_client:
        result = await index_client.get_index(name)
    print(f"Retrieved index '{result.name}'")
    # [END get_index_async]


async def update_index():
    # [START update_index_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient
    from azure.search.documents.indexes.models import (
        ComplexField,
        CorsOptions,
        SearchIndex,
        ScoringProfile,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
    )

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    name = "hotels"
    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="HotelName", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="BaseRate", type=SearchFieldDataType.Double),
        SearchableField(name="Description", type=SearchFieldDataType.String, collection=True),
        ComplexField(
            name="Address",
            fields=[
                SimpleField(name="StreetAddress", type=SearchFieldDataType.String),
                SimpleField(name="City", type=SearchFieldDataType.String),
                SimpleField(name="state", type=SearchFieldDataType.String),
            ],
            collection=True,
        ),
    ]

    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profile = ScoringProfile(name="MyProfile")
    scoring_profiles = []
    scoring_profiles.append(scoring_profile)
    index = SearchIndex(name=name, fields=fields, scoring_profiles=scoring_profiles, cors_options=cors_options)

    async with index_client:
        result = await index_client.create_or_update_index(index=index)
    print(f"Updated index '{result.name}'")
    # [END update_index_async]


async def delete_index():
    # [START delete_index_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    name = "hotels"
    async with index_client:
        await index_client.delete_index(name)
    print(f"Deleted index '{name}'")
    # [END delete_index_async]


async def main():
    await create_index()
    await get_index()
    await update_index()
    await delete_index()


if __name__ == "__main__":
    asyncio.run(main())
