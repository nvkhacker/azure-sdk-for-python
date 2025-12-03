# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_semantic_search.py
DESCRIPTION:
    This sample demonstrates how to use semantic search.
USAGE:
    python sample_semantic_search.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import os


def speller():
    # [START speller]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    results = list(client.search(search_text="luxury", query_language="en-us", query_speller="lexicon"))

    for result in results:
        print("{}\n{}\n)".format(result["HotelId"], result["HotelName"]))
    # [END speller]


def semantic_ranking():
    # [START semantic_ranking]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    key = os.environ["AZURE_SEARCH_API_KEY"]

    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    results = list(
        client.search(
            search_text="luxury",
            query_type="semantic",
            semantic_configuration_name="semantic_config_name",
            query_language="en-us",
        )
    )

    for result in results:
        print("{}\n{}\n)".format(result["HotelId"], result["HotelName"]))
    # [END semantic_ranking]


if __name__ == "__main__":
    speller()
    semantic_ranking()
