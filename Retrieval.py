def get_billing_record(record_id):
    # Check Cosmos DB
    try:
        item = cosmos_container.read_item(item=record_id, partition_key=record_id)
        return item  # Found in Cosmos DB
    except exceptions.CosmosResourceNotFoundError:
        pass  # Not found, fallback to blob

    # Check Hot Blob Storage
    for tier in ["billing-hot", "billing-cold"]:
        blob_client = blob_service.get_blob_client(container=tier, blob=f"{record_id}.json")
        if blob_client.exists():
            blob_data = blob_client.download_blob().readall()
            record = json.loads(blob_data)

            # Optional: Rehydrate to Cosmos
            # cosmos_container.upsert_item(record)

            return record  # Found in blob

    # If not found anywhere
    return None
