import pymongo
import random
import datetime
from faker import Faker

# Initialize Faker for realistic data
fake = Faker()

# MongoDB connection details
# Ensure this is your writable cluster connection string
MONGO_CONNECTION_STRING = "mongodb+srv://main_user:AdminAdmin1@cluster1.fgc5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
DB_NAME = "credit_card"  # Your database name
COLLECTION_NAME = "accounts" # New collection name for accounts

def generate_account_document(document_id):
    """
    Generates a single account document with random data.
    Takes a document_id for the _id field.
    """
    # --- HIERARCHY ID AND ROOT NODE ID LOGIC ---
    cli_num = random.randint(0, 100)
    root_node_id_value = f"CLI_{cli_num:06d}"

    ban_num = random.randint(0, 100)
    age_num = random.randint(0, 100)
    com_num = random.randint(0, 100)
    div_num = random.randint(0, 100)
    dep_num = random.randint(0, 100)
    hierarchy_id_value = (f"{root_node_id_value}-BAN_{ban_num:06d}-AGE_{age_num:06d}-"
                          f"COM_{com_num:06d}-DIV_{div_num:06d}-DEP_{dep_num:06d}")

    # --- FINAL DOCUMENT STRUCTURE ---
    account_document = {
        "_id": document_id,
        "hierarchy_id": hierarchy_id_value,
        "root_node_id": root_node_id_value,
        "account_number": fake.bban(),
        "account_type_code": random.choice(["CHQ", "SAV", "CRD", "LOC"]),
        "account_name": fake.company(),
        "load_date": fake.date_time_between(start_date="-30d", end_date="now", tzinfo=datetime.timezone.utc),
        "data_source_name": random.choice(["Issuer1", "Issuer2", "PartnerAPI", "BatchUpload"])
    }
    return account_document

def main():
    client = None
    try:
        # --- CONFIGURATION ---
        TOTAL_DOCUMENTS = 1_000_000
        BATCH_SIZE = 5_000 # Process 5,000 documents at a time

        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = client[DB_NAME]
        accounts_collection = db[COLLECTION_NAME]

        print(f"Connected to MongoDB database: '{DB_NAME}'")

        # Drop the collection if it exists to ensure a clean slate
        if COLLECTION_NAME in db.list_collection_names():
            accounts_collection.drop()
            print(f"Dropped existing collection: '{COLLECTION_NAME}'")

        print(f"Preparing to insert {TOTAL_DOCUMENTS:,} documents in batches of {BATCH_SIZE:,}...")

        # --- BATCH PROCESSING LOOP ---
        documents_batch = []
        for i in range(1, TOTAL_DOCUMENTS + 1):
            doc = generate_account_document(i)
            documents_batch.append(doc)

            # When the batch is full, insert it and clear the list
            if i % BATCH_SIZE == 0:
                accounts_collection.insert_many(documents_batch)
                print(f"-> Inserted batch {i // BATCH_SIZE}. Total documents: {i:,}")
                documents_batch = [] # Reset for the next batch

        # Insert any remaining documents that didn't make a full batch
        if documents_batch:
            accounts_collection.insert_many(documents_batch)
            print(f"-> Inserted final batch. Total documents: {TOTAL_DOCUMENTS:,}")

        print("\nSuccessfully inserted all documents.")

    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    main()