# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to get, create, update, or delete an alias for an Azure AI Search index.

USAGE:
    python sample_index_alias_crud_async.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
        (e.g., https://<your-search-service-name>.search.windows.net)
    2) AZURE_SEARCH_API_KEY - the admin key for your search service
    3) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
"""


import asyncio
import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]
alias_name = "motels"

async def create_alias():
    # [START create_alias_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient
    from azure.search.documents.indexes.models import SearchAlias

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    alias = SearchAlias(name=alias_name, indexes=[index_name])
    async with index_client:
        result = await index_client.create_alias(alias)
    print(f"Created alias '{result.name}' pointing to index '{index_name}'")
    # [END create_alias_async]


async def get_alias():
    # [START get_alias_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    async with index_client:
        result = await index_client.get_alias(alias_name)
    print(f"Retrieved alias '{result.name}'")
    # [END get_alias_async]


async def update_alias():
    # [START update_alias_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient
    from azure.search.documents.indexes.models import (
        ComplexField,
        CorsOptions,
        ScoringProfile,
        SearchAlias,
        SearchIndex,
        SimpleField,
        SearchableField,
        SearchFieldDataType,
    )

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    new_index_name = "hotels-v2"
    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SimpleField(name="BaseRate", type=SearchFieldDataType.Double),
        SearchableField(name="Description", type=SearchFieldDataType.String, collection=True),
        SearchableField(name="HotelName", type=SearchFieldDataType.String),
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
    index = SearchIndex(
        name=new_index_name, fields=fields, scoring_profiles=[scoring_profile], cors_options=cors_options
    )

    async with index_client:
        await index_client.create_or_update_index(index=index)
        print(f"Created/Updated index '{new_index_name}'")

        alias = SearchAlias(name=alias_name, indexes=[new_index_name])
        result = await index_client.create_or_update_alias(alias)
    print(f"Updated alias '{result.name}' to point to index '{new_index_name}'")
    # [END update_alias_async]


async def delete_alias():
    # [START delete_alias_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes.aio import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    async with index_client:
        await index_client.delete_alias(alias_name)
    print(f"Deleted alias '{alias_name}'")
    # [END delete_alias_async]


async def main():
    await create_alias()
    await get_alias()
    await update_alias()
    await delete_alias()


if __name__ == "__main__":
    asyncio.run(main())


async def main():
    await create_alias()
    await get_alias()
    await update_alias()
    await delete_alias()
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
