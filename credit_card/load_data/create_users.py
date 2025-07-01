import pymongo
import random
import datetime
import os
from faker import Faker

# Initialize Faker for realistic data
fake = Faker()

# MongoDB connection details
# Get connection string from environment variable
MONGO_CONNECTION_STRING = os.environ.get('CLUSTER1_URI')
DB_NAME = "credit_card"  # Your database name
COLLECTION_NAME = "users" # Collection name for users

def generate_user_document():
    """Generates a single user document with random data following the new format."""

    # Define all possible hierarchy nodes
    base_com_node = "COM1"
    
    # Generate all possible COM1-DIVx nodes
    possible_div_nodes = [f"COM1-DIV{i}" for i in range(1, 4)] # COM1-DIV1, COM1-DIV2, COM1-DIV3
    
    # Generate all possible COM1-DIVx-DEPy nodes
    possible_dep_nodes = [f"COM1-DIV{i}-DEP{j}" for i in range(1, 4) for j in range(1, 7)] # All 18 combinations

    hierarchy_entitlements_set = set() # Use a set to automatically handle uniqueness

    # --- Hierarchy Entitlements Generation Logic ---

    # Scenario A: User has ONLY "COM1" (10% chance as requested)
    if random.random() < 0.10:
        hierarchy_entitlements_set.add(base_com_node)
    
    # Scenario B: User has "COM1" and/or "COM1-DIVx" nodes (e.g., 30% chance for this pattern emphasis)
    elif random.random() < 0.30:
        hierarchy_entitlements_set.add(base_com_node) # Always include COM1 for this pattern

        # Add 1 to 3 random COM1-DIVx nodes
        num_div_to_add = random.randint(1, min(3, len(possible_div_nodes)))
        sampled_div_nodes = random.sample(possible_div_nodes, num_div_to_add)
        hierarchy_entitlements_set.update(sampled_div_nodes)

        # Small chance to sprinkle in a few DEP nodes even in this scenario, but not as the primary focus
        if random.random() < 0.2: # 20% chance to add 1-2 DEP nodes
            num_dep_to_add = random.randint(1, min(2, len(possible_dep_nodes)))
            sampled_dep_nodes = random.sample(possible_dep_nodes, num_dep_to_add)
            hierarchy_entitlements_set.update(sampled_dep_nodes)

    # Scenario C: General mix of all three levels (the remaining probability)
    else:
        # Start with COM1 for this mixed type (high probability)
        if random.random() < 0.9: # 90% chance to include COM1 in general mixed sets
            hierarchy_entitlements_set.add(base_com_node)

        # Add random DIV nodes (e.g., 0 to all available)
        num_div_to_add = random.randint(0, len(possible_div_nodes))
        sampled_div_nodes = random.sample(possible_div_nodes, num_div_to_add)
        hierarchy_entitlements_set.update(sampled_div_nodes)

        # Add random DEP nodes (e.g., 1 to 5, ensuring at least one if possible)
        num_dep_to_add = random.randint(1, min(5, len(possible_dep_nodes)))
        sampled_dep_nodes = random.sample(possible_dep_nodes, num_dep_to_add)
        hierarchy_entitlements_set.update(sampled_dep_nodes)

    # --- End Hierarchy Entitlements Generation Logic ---

    # Convert the set back to a list, sorting for consistent output
    hierarchy_entitlements = sorted(list(hierarchy_entitlements_set))
    
    # Fallback: Ensure at least 'COM1' if, by some extremely rare chance, the list ended up empty
    # This can happen if all random.random() calls for inclusion resulted in false and no DEP nodes were chosen.
    if not hierarchy_entitlements:
        hierarchy_entitlements.append(base_com_node)


    user_document = {
        # "_id" will be automatically generated as ObjectId by MongoDB
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "userType": random.choice(["Program Administrator", "Risk Analyst", "Compliance Officer", "Customer Support", "Operations Staff", "Finance User"]),
        "loadDate": datetime.datetime.now(), # PyMongo handles conversion to BSON Date
        "hierarchyEntitlements": hierarchy_entitlements,
        "isActive": random.choice([True, False]),
        "lastActivity": fake.date_time_between(start_date="-3m", end_date="now")
    }
    return user_document

def main():
    client = None
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = client[DB_NAME]
        users_collection = db[COLLECTION_NAME]

        print(f"Connected to MongoDB database: '{DB_NAME}'")

        # Drop the collection if it exists (to ensure fresh data per run)
        if COLLECTION_NAME in db.list_collection_names():
            users_collection.drop()
            print(f"Dropped existing collection: '{COLLECTION_NAME}'")
        else:
            print(f"Collection '{COLLECTION_NAME}' does not exist, creating new one.")

        # Generate and insert data
        num_documents_to_insert = 60 # You can change this number
        documents = []
        for _ in range(num_documents_to_insert):
            doc = generate_user_document()
            documents.append(doc)

        if documents:
            users_collection.insert_many(documents)
            print(f"Successfully inserted {len(documents)} documents into '{COLLECTION_NAME}'.")
        else:
            print("No documents to insert.")

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