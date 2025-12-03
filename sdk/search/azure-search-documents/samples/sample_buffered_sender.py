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
    python sample_buffered_sender.py

    Set the following environment variables before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - base URL of your Azure AI Search service
    2) AZURE_SEARCH_INDEX_NAME - target search index name (e.g., "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - the primary admin key for your search service
"""

import os

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchIndexingBufferedSender


def sample_batching_client():
    DOCUMENT = {
        "Category": "Hotel",
        "HotelId": "1000",
        "Rating": 4.0,
        "Rooms": [],
        "HotelName": "Azure Inn",
    }

    with SearchIndexingBufferedSender(service_endpoint, index_name, AzureKeyCredential(key)) as batch_client:
        # add upload actions
        batch_client.upload_documents(documents=[DOCUMENT])
        # add merge actions
        batch_client.merge_documents(documents=[{"HotelId": "1000", "Rating": 4.5}])
        # add delete actions
        batch_client.delete_documents(documents=[{"HotelId": "1000"}])


if __name__ == "__main__":
    sample_batching_client()
