# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to perform vector search.
USAGE:
    python sample_query_vector.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
    4) OpenAIEndpoint - the endpoint for your OpenAI service
    5) OpenAIKey - the API key for your OpenAI service
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def get_embeddings(text: str):
    # There are a few ways to get embeddings. This is just one example.
    import openai

    open_ai_endpoint = os.getenv("OpenAIEndpoint")
    open_ai_key = os.getenv("OpenAIKey")

    client = openai.AzureOpenAI(
        azure_endpoint=open_ai_endpoint,
        api_key=open_ai_key,
        api_version="2023-09-01-preview",
    )
    embedding = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return embedding.data[0].embedding


def get_hotel_index(name: str):
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SearchField,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
        VectorSearch,
        VectorSearchProfile,
        HnswAlgorithmConfiguration,
    )

    fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SearchableField(
            name="HotelName",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
        ),
        SearchableField(name="Description", type=SearchFieldDataType.String),
        SearchField(
            name="descriptionVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="my-vector-config",
        ),
        SearchableField(
            name="Category",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
    ]
    vector_search = VectorSearch(
        profiles=[VectorSearchProfile(name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
        algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
    )
    return SearchIndex(name=name, fields=fields, vector_search=vector_search)


def get_hotel_documents():
    docs = [
        {
            "HotelId": "1",
            "HotelName": "Fancy Stay",
            "Description": "Best hotel in town if you like luxury hotels.",
            "descriptionVector": get_embeddings("Best hotel in town if you like luxury hotels."),
            "Category": "Luxury",
        },
        {
            "HotelId": "2",
            "HotelName": "Roach Motel",
            "Description": "Cheapest hotel in town. Infact, a motel.",
            "descriptionVector": get_embeddings("Cheapest hotel in town. Infact, a motel."),
            "Category": "Budget",
        },
        {
            "HotelId": "3",
            "HotelName": "EconoStay",
            "Description": "Very popular hotel in town.",
            "descriptionVector": get_embeddings("Very popular hotel in town."),
            "Category": "Budget",
        },
        {
            "HotelId": "4",
            "HotelName": "Modern Stay",
            "Description": "Modern architecture, very polite staff and very clean. Also very affordable.",
            "descriptionVector": get_embeddings(
                "Modern architecture, very polite staff and very clean. Also very affordable."
            ),
            "Category": "Luxury",
        },
        {
            "HotelId": "5",
            "HotelName": "Secret Point",
            "Description": "One of the best hotel in town. The hotel is ideally located on the main commercial artery of the city in the heart of New York.",
            "descriptionVector": get_embeddings(
                "One of the best hotel in town. The hotel is ideally located on the main commercial artery of the city in the heart of New York."
            ),
            "Category": "Boutique",
        },
    ]
    return docs


def single_vector_search():
    # [START single_vector_search]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import VectorizedQuery

    query = "Top hotels in town"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")

    results = search_client.search(
        vector_queries=[vector_query],
        select=["HotelId", "HotelName"],
    )

    for result in results:
        print(result)
    # [END single_vector_search]


def single_vector_search_with_filter():
    # [START single_vector_search_with_filter]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import VectorizedQuery

    query = "Top hotels in town"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")

    results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        filter="category eq 'Luxury'",
        select=["HotelId", "HotelName"],
    )

    for result in results:
        print(result)
    # [END single_vector_search_with_filter]


def simple_hybrid_search():
    # [START simple_hybrid_search]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import VectorizedQuery

    query = "Top hotels in town"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["HotelId", "HotelName"],
    )

    for result in results:
        print(result)
    # [END simple_hybrid_search]


if __name__ == "__main__":
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient

    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(service_endpoint, credential)
    index = get_hotel_index(index_name)
    index_client.create_index(index)
    search_client = SearchClient(service_endpoint, index_name, credential)
    hotel_docs = get_hotel_documents()
    search_client.upload_documents(documents=hotel_docs)

    single_vector_search()
    single_vector_search_with_filter()
    simple_hybrid_search()
