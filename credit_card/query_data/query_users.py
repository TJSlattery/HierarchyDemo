import json
from pymongo import MongoClient

# --- Configuration ---
MONGO_CONNECTION_STRING = "mongodb+srv://main_user:AdminAdmin1@cluster1.fgc5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
DATABASE_NAME = "credit_card"
COLLECTION_NAME = "accounts"
PREFIX_FILE = "hierarchy_query.json"

def load_prefixes(filename):
    """Loads a list of prefixes from a JSON file."""
    try:
        with open(filename, 'r') as f:
            prefixes = json.load(f)
            # 1. Output: Confirmation of loading prefixes
            print(f"✅ Successfully loaded {len(prefixes)} prefixes from {filename}.")
            return prefixes
    except FileNotFoundError:
        print(f"❌ ERROR: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"❌ ERROR: The file '{filename}' is not a valid JSON file.")
        return None

# --- Main Script ---
prefixes = load_prefixes(PREFIX_FILE)

if prefixes:
    try:
        with MongoClient(MONGO_CONNECTION_STRING) as client:
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]

            or_conditions = [{"hierarchy_id": {"$regex": f"^{prefix}"}} for prefix in prefixes]
            query = {"$or": or_conditions}

            # First, execute the query and get the documents
            # list() consumes the cursor and stores all docs in memory
            results = list(collection.find(query))
            document_count = len(results)

            # --- Conditional output based on the number of results ---
            if 0 < document_count < 10:
                # If 1-9 documents are found, print them all
                print(f"\nFound {document_count} document(s) (displaying full content):")
                print("-" * 40)
                for doc in results:
                    print(json.dumps(doc, indent=4, default=str))
                    print("-" * 40)
            else:
                # If 0 or 10+ documents are found, print the performance summary
                print(f"\nFound {document_count} document(s). Displaying performance summary:")
                
                # We need to run .explain() to get the stats
                explain_plan = collection.find(query).explain()
                stats = explain_plan.get('executionStats', {})
                
                keys_examined = stats.get('totalKeysExamined', 'N/A')
                exec_time = stats.get('executionTimeMillis', 'N/A')

                print(f"  - Keys examined: {keys_examined}")
                print(f"  - Execution time: {exec_time} ms")

    except Exception as e:
        print(f"An error occurred during database operation: {e}")