# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to analyze text.
USAGE:
    python sample_analyze_text.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def simple_analyze_text():
    # [START simple_analyze_text]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import AnalyzeTextOptions

    client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    analyze_request = AnalyzeTextOptions(text="One's <two/>", analyzer_name="standard.lucene")

    result = client.analyze_text(index_name, analyze_request)
    print(result.as_dict())
    # [END simple_analyze_text]


if __name__ == "__main__":
    simple_analyze_text()
