Best Way for Storage Cost Optimization 

According to the problem, cost optimization can be done by using Blob Storage service of Azure, which provides service to store huge amount of unstructured data at a feasible cost. 

In Blob Storage we can create lifecycle management policy for the data of different duration to cut the cost incurred by the organization.

As of now, if there 2 million records of 300 KB each then organization is paying for 600 GB of data which will cost around $150/per month. Data can be divided in different storage according to the lifecycle policy.

Lifecycle Management Policy

First of all, talking about the whole data, if all data is 3 months old, organization can follow lifecycle policy if new data is also there then following steps:
Upto 1 month: Data upto 1 month can be stored in Cosmo DB, as person needs fast access for that to see the cost every month. 

>1 month – 3 month: Then data older than 1 month but not 3 months will be stored in hot tier, so that it can be accessed easily and little frequently.

> 3 month: Data older than 3 months will be stored in cold tier, as it will be accessed but not frequently.

We are not using archive tier since data will be retrieved eventhough rarely, and retrieval cost is higher in archive tier.

Process to be Done

It can be through automation scripts or through UI (if someone not comfortable with code)

1. Setup Azure Blob Storage
Go to Azure Portal > Storage Accounts > +Create
Choose Hot and Cold access tiers enabled
Create 2 containers:
o	billing-hot
o	billing-cold

2. Create a Data Archival Pipeline (Azure Data Factory)
Go to Azure Portal > Azure Data Factory > +Create
After deployment, open Author & Monitor
Create a new pipeline:
o	Source: Cosmos DB query (records older than 1 month)
o	Sink (Destination): Azure Blob Storage (container = billing-hot)
Use Mapping Data Flow for transformation if needed
Schedule pipeline to run daily or weekly
Sample Query in Cosmos Source:
SELECT * FROM c WHERE c.createdAt < @1MonthAgo
You can pass @1MonthAgo using a parameter that calculates the date.

3.  Set up Blob Lifecycle Rule (Auto-Hot to Cold)
Go to your Blob Storage Account > Data Management > Lifecycle Management
Add a rule:
o	If blob is in billing-hot
o	AND Last Modified > 90 days
o	Then move to Cold tier

4.	Enable Retrieval via Logic App
If wanted to automatically check Blob if data is missing from Cosmos DB:
Go to Azure Portal > Logic Apps > +Create
Choose "When an HTTP request is received"
Add steps:
Check Cosmos DB for the record
If not found, search blob containers (billing-hot, billing-cold)
Return the found record as HTTP response

5.	Update API Internally
If your API reads from Cosmos DB and fails to find a record, it can:
Internally trigger the Logic App
Get the record from Blob Storage
Optionally re-cache it back to Cosmos DB (auto rehydration)
For Automation Script check the files in repository
•	Transfer_data_from_cosmo-db_to_blob-storage.py (for transfer of data)
•	Retrieval.py (for retrieval of data from cosmo db and blob storage)
•	Blob_Storage_Policy.json (Policy for hot -> cold after 90 days)

Note: The logic for the problem is mine, only used chatgpt to give automation scripts and architecture.

Prompt: I want that data of 1 month should be in cosmo db for fast read and write and then, data older than 1 and upto 3 month should be in hot storage and data older than that should go to cold storage as company wants data to be retrieval but it is infrequent after 3 months so it is the best case as cold storage provide good retrieval speed and cost optimization and as company want slowed access so we don't want it to store in archival storage of azure.
