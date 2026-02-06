from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile, SearchField
)
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

EMBEDDING_DIM = 1536  # text-embedding-ada-002 dimension

def create_index_if_missing(endpoint: str, api_key: str, index_name: str):
    cred = AzureKeyCredential(api_key)
    index_client = SearchIndexClient(endpoint=endpoint, credential=cred)

    existing = [i.name for i in index_client.list_indexes()]
    if index_name in existing:
        return

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="doc_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="filename", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chunk_index", type=SearchFieldDataType.Int32, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIM,
            vector_search_profile_name="vprofile"
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[VectorSearchProfile(name="vprofile", algorithm_configuration_name="hnsw")]
    )

    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    index_client.create_index(index)

def get_search_client(endpoint: str, api_key: str, index_name: str) -> SearchClient:
    return SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))

def upsert_chunks(search_client: SearchClient, records: list[dict]):
    # records: {id, doc_id, filename, chunk_index, content, contentVector}
    search_client.upload_documents(documents=records)
