# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    Demonstrates how to create, get, update, and delete a synonym map.
USAGE:
    python sample_index_synonym_map_crud.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def create_synonym_map(name):
    # [START create_synonym_map]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import SynonymMap

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    synonyms = [
        "USA, United States, United States of America",
        "Washington, Wash. => WA",
    ]
    synonym_map = SynonymMap(name=name, synonyms=synonyms)
    result = index_client.create_synonym_map(synonym_map)
    print(f"Create new Synonym Map '{result.name}' succeeded")
    # [END create_synonym_map]


def create_synonym_map_from_file(name):
    # [START create_synonym_map_from_file]
    from pathlib import Path
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import SynonymMap

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    file_path = Path(__file__).resolve().parent / "data" / "synonym_map.txt"
    with open(file_path, "r") as f:
        solr_format_synonyms = f.read()
        synonyms = solr_format_synonyms.split("\n")
        synonym_map = SynonymMap(name=name, synonyms=synonyms)
        result = index_client.create_synonym_map(synonym_map)
        print(f"Create new Synonym Map '{result.name}' succeeded")
    # [END create_synonym_map_from_file]


def get_synonym_maps():
    # [START get_synonym_maps]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    result = index_client.get_synonym_maps()
    names = [x.name for x in result]
    print(f"Found {len(result)} Synonym Maps in the service: {', '.join(names)}")
    # [END get_synonym_maps]


def get_synonym_map(name):
    # [START get_synonym_map]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    result = index_client.get_synonym_map(name)
    print(f"Retrived Synonym Map '{name}' with synonyms")
    if result:
        for syn in result.synonyms:
            print(f"    {syn}")
    # [END get_synonym_map]


def delete_synonym_map(name):
    # [START delete_synonym_map]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient

    index_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    index_client.delete_synonym_map(name)
    print(f"Synonym Map '{name}' deleted")
    # [END delete_synonym_map]


if __name__ == "__main__":
    map1 = "sample-synonym-map"
    map2 = "sample-synonym-map-file"

    create_synonym_map(map1)
    create_synonym_map_from_file(map2)
    get_synonym_maps()
    get_synonym_map(map1)
    delete_synonym_map(map1)
    delete_synonym_map(map2)
