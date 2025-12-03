# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_autocomplete.py
DESCRIPTION:
    This sample demonstrates how to obtain autocompletion suggestions from an
    Azure Search index.
USAGE:
    python sample_autocomplete.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def autocomplete_query():
    # [START autocomplete_query]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    results = search_client.autocomplete(search_text="bo", suggester_name="sg")

    print("Autocomplete suggestions for 'bo'")
    for result in results:
        print("    Completion: {}".format(result["text"]))
    # [END autocomplete_query]


if __name__ == "__main__":
    autocomplete_query()
