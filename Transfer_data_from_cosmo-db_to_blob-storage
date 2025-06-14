from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta
import json

# Configs
cosmos_uri = "<cosmos-uri>"
cosmos_key = "<cosmos-key>"
database_name = "<db-name>"
container_name = "<container-name>"
blob_connection_string = "<blob-conn-str>"
hot_container = "billing-hot"
cold_container = "billing-cold"

# Setup clients
cosmos_client = CosmosClient(cosmos_uri, credential=cosmos_key)
database = cosmos_client.get_database_client(database_name)
container = database.get_container_client(container_name)

blob_service = BlobServiceClient.from_connection_string(blob_connection_string)

# Time thresholds
now = datetime.utcnow()
one_month_ago = now - timedelta(days=30)
three_months_ago = now - timedelta(days=90)

query = f"SELECT * FROM c WHERE c.createdAt < '{one_month_ago.isoformat()}'"

# Process records
for item in container.query_items(query=query, enable_cross_partition_query=True):
    record_id = item["id"]
    created_at = datetime.fromisoformat(item["createdAt"])
    
    # Determine tier
    if created_at > three_months_ago:
        target_container = hot_container
    else:
        target_container = cold_container

    # Write to Blob
    blob_client = blob_service.get_blob_client(container=target_container, blob=f"{record_id}.json")
    blob_client.upload_blob(json.dumps(item), overwrite=True)

    # Optional: delete from Cosmos DB
    # container.delete_item(item=record_id, partition_key=item["partitionKey"])

    print(f"Archived record {record_id} to {target_container}")
