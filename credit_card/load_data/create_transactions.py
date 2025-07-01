import pymongo
import random
import datetime
from faker import Faker
from bson.decimal128 import Decimal128 # Import Decimal128 if you decide to use it for other fields

# Initialize Faker for realistic data
fake = Faker()

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://main_user:AdminAdmin1@cluster1.fgc5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
DB_NAME = "credit_card"  # Your database name
COLLECTION_NAME = "transactions" # New collection name

def generate_random_transaction(transaction_id_counter):
    """
    Generates a single credit card transaction document with random data.
    Takes a transaction_id_counter to ensure sequential IDs.
    """

    # Subdocuments
    allocations = []
    num_allocations = random.randint(1, 4)
    for _ in range(num_allocations):
        allocations.append({
            "allocationId": fake.uuid4(),
            "amount": round(random.uniform(5.00, 500.00), 2),
            "currency": "USD",
            "category": fake.random_element(elements=('Merchant Fee', 'Interchange Fee', 'Processing Fee', 'Surcharge', 'Cashback Reward', 'Dispute Settlement')),
            "status": fake.random_element(elements=('Applied', 'Pending', 'Reversed')),
            "allocationDate": fake.date_time_between(start_date="-6m", end_date="now")
        })

    comments = []
    num_comments = random.randint(0, 3)
    for _ in range(num_comments):
        comments.append({
            "commentId": fake.uuid4(),
            "text": fake.paragraph(nb_sentences=2, variable_nb_sentences=True),
            "timestamp": fake.date_time_between(start_date="-3m", end_date="now"),
            "author": fake.name()
        })

    line_items = []
    num_line_items = random.randint(1, 6)

    # --- Predefined lists for product names and categories (WORKAROUND FOR FAKER.COMMERCE ISSUE) ---
    common_product_names = [
        "Bluetooth Headphones", "Stainless Steel Water Bottle", "USB-C Charger",
        "Ergonomic Mouse", "Wireless Keyboard", "Smartwatch", "Portable Speaker",
        "Coffee Maker", "Toaster Oven", "Blender", "Cookware Set", "Dinner Plates",
        "Graphic T-Shirt", "Jeans", "Running Shoes", "Winter Coat", "Laptop Backpack",
        "Notebook", "Pens Set", "Desk Lamp", "External Hard Drive", "Webcam",
        "Gaming Headset", "Microfiber Towels", "Yoga Mat", "Dumbbell Set",
        "Protein Powder", "Vitamins", "Face Moisturizer", "Shampoo", "Toothbrush Pack",
        "Fiction Novel", "Gardening Tools", "Pet Food", "Board Game", "Art Supplies",
        "Car Cleaning Kit", "First Aid Kit", "Travel Mug", "Reusable Shopping Bag",
        "Electric Kettle", "Weighted Blanket", "Drone", "VR Headset", "Smart Thermostat"
    ]

    common_product_categories = [
        "Electronics", "Home Goods", "Apparel", "Footwear", "Accessories",
        "Kitchen & Dining", "Health & Beauty", "Sports & Outdoors", "Office Supplies",
        "Computer Peripherals", "Books", "Software", "Food & Beverages", "Pet Supplies",
        "Toys & Games", "Automotive", "Travel Gear", "Home Improvement", "Wearable Tech"
    ]
    # --- END OF WORKAROUND ---

    for _ in range(num_line_items):
        line_items.append({
            "lineItemId": fake.uuid4(),
            "productDescription": random.choice(common_product_names), # Using random.choice
            "quantity": random.randint(1, 5),
            "unitPrice": round(random.uniform(1.00, 300.00), 2),
            "totalPrice": round(random.uniform(5.00, 1500.00), 2),
            "productCategory": random.choice(common_product_categories), # Using random.choice
            "sku": fake.bothify(text='SKU-####-????')
        })

    approvals = []
    num_approvals = random.randint(1, 3)
    for _ in range(num_approvals):
        approvals.append({
            "approvalId": fake.uuid4(),
            "approver": fake.name(),
            "approvalDate": fake.date_time_between(start_date="-1y", end_date="now"),
            "status": random.choice(["Approved", "Rejected", "Pending Review"]),
            "notes": fake.sentence(nb_words=8) if random.random() < 0.7 else None
        })

    # 80 other fields for credit card transactions
    other_fields = {
        "transactionId": f"T{transaction_id_counter:03d}",
        "customerId": fake.uuid4(),
        "accountId": fake.uuid4(),
        "cardNumberMasked": f"XXXX-XXXX-XXXX-{random.randint(1000, 9999)}",
        "transactionDate": fake.date_time_between(start_date="-1y", end_date="now"),
        "postingDate": fake.date_time_between(start_date="-1y", end_date="now"),
        "transactionAmount": round(random.uniform(0.50, 2500.00), 2),
        "transactionCurrency": "USD",
        "localCurrencyAmount": round(random.uniform(0.50, 2500.00), 2),
        "localCurrencyCode": "USD" if random.random() < 0.9 else fake.currency_code(),
        "exchangeRate": round(random.uniform(0.8, 1.2), 4) if random.random() < 0.1 else 1.0,
        "merchantName": fake.company(),
        "merchantCategoryCode": str(random.randint(5000, 9999)), # MCC code
        "merchantCity": fake.city(),
        "merchantState": fake.state_abbr(),
        "merchantZip": fake.postcode(),
        "merchantCountry": fake.country_code(),
        "merchantId": fake.bothify(text='MID######'),
        "terminalId": fake.bothify(text='TID??????'),
        "transactionType": random.choice(["Purchase", "Refund", "Cash Advance", "Payment", "ATM Withdrawal"]),
        "transactionStatus": random.choice(["Approved", "Declined", "Pending", "Settled", "Reversed"]),
        "authCode": fake.bothify(text='######'),
        "responseCode": random.choice(["00", "01", "05", "51", "91", "CN"]), # Common transaction response codes
        "processorResponse": fake.sentence(nb_words=5),
        "authTimestamp": fake.date_time_between(start_date="-1y", end_date="now"),
        "settlementTimestamp": fake.date_time_between(start_date="-1y", end_date="now"),
        "batchId": fake.uuid4(),
        "invoiceNumber": fake.bothify(text='INV-########'),
        "referenceNumber": fake.bothify(text='REF-############'),
        "arn": fake.bothify(text='####################'), # Acquirer Reference Number
        "rrn": fake.bothify(text='############'), # Retrieval Reference Number
        "cardBrand": random.choice(["Visa", "Mastercard", "Amex", "Discover", "JCB"]),
        "cardType": random.choice(["Credit", "Debit", "Prepaid"]),
        "entryMode": random.choice(["Chip", "Swipe", "Contactless", "Keyed", "eCommerce"]),
        "cardPresent": random.choice([True, False]),
        "cvvProvided": random.choice([True, False]),
        "avsResponse": random.choice(["Y", "A", "N", "Z", "W", "P", "S", "U", "R"]), # Address Verification System
        "fraudScore": round(random.uniform(0.0, 100.0), 2),
        "riskLevel": random.choice(["Low", "Medium", "High", "Critical"]),
        "fraudIndicators": random.sample(["IP_Mismatch", "High_Frequency", "Unusual_Location", "New_Device", "Multiple_Declines", "Velocity_Breach"], k=random.randint(0, 3)),
        "disputeStatus": random.choice(["None", "Initiated", "Under Review", "Resolved_Merchant", "Resolved_Cardholder"]),
        "disputeReasonCode": fake.bothify(text='R###') if random.random() < 0.1 else None, # e.g., R01, R03
        "chargebackStatus": random.choice(["None", "Filed", "Represented", "Won", "Lost"]),
        "chargebackAmount": round(random.uniform(0.00, 2500.00), 2) if random.random() < 0.05 else 0.00,
        "isRefund": random.choice([True, False]),
        "originalTransactionId": fake.uuid4() if random.random() < 0.1 else None, # For refunds/chargebacks
        "customerIpAddress": fake.ipv4(),
        "customerDeviceType": random.choice(["Mobile", "Desktop", "Tablet"]),
        "customerBrowser": random.choice(["Chrome", "Firefox", "Safari", "Edge", "Opera"]),
        "customerOperatingSystem": random.choice(["Windows", "MacOS", "iOS", "Android", "Linux"]),
        # --- CONVERT DECIMAL TO FLOAT FOR LATITUDE AND LONGITUDE ---
        "geoLatitude": float(fake.latitude()),
        "geoLongitude": float(fake.longitude()),
        # --- END CONVERSION ---
        "geoCountry": fake.country_code(),
        "loyaltyPointsEarned": random.randint(0, 1000),
        "promotionApplied": fake.word() if random.random() < 0.2 else None,
        "isRecurringTransaction": random.choice([True, False]),
        "subscriptionId": fake.uuid4() if random.random() < 0.1 else None,
        "installmentsPlan": random.choice([True, False]),
        "numberOfInstallments": random.randint(1, 12) if random.random() < 0.05 else 1,
        "authorizationMode": random.choice(["Online", "Offline"]),
        "issuerBankName": fake.bank_country(),
        "acquirerBankName": fake.bank_country(),
        "networkName": random.choice(["VisaNet", "Mastercard Cirrus", "Amex Express"]),
        "interchangeFeeAmount": round(random.uniform(0.05, 1.50), 2),
        "schemeFeeAmount": round(random.uniform(0.01, 0.50), 2),
        "processorFeeAmount": round(random.uniform(0.05, 1.00), 2),
        "totalFeesAmount": round(random.uniform(0.10, 3.00), 2),
        "isTokenized": random.choice([True, False]),
        "tokenType": random.choice(["Card Token", "Wallet Token"]) if random.random() < 0.3 else None,
        "cardholderVerificationMethod": random.choice(["PIN", "Signature", "No CVM", "Online Auth"]),
        "fundingSource": random.choice(["Credit", "Debit", "Prepaid"]),
        "settlementCurrency": "USD",
        "netSettlementAmount": round(random.uniform(0.40, 2490.00), 2),
        "acquirerTransactionId": fake.uuid4(),
        "issuerTransactionId": fake.uuid4(),
        "isoMessage": fake.sentence(nb_words=10), # Simulated ISO 8583 message part
        "is3DSecure": random.choice([True, False]),
        "dsStatus": random.choice(["Y", "N", "A"]) if random.random() < 0.3 else None, # 3D Secure Directory Server Status
        "cavvResultCode": random.choice(["0", "1", "2", "9"]) if random.random() < 0.3 else None, # Cardholder Authentication Verification Value
        "xid": fake.bothify(text='??????????????????????') if random.random() < 0.3 else None, # Transaction Identifier from 3DS
        "originalApprovalCode": fake.bothify(text='######') if random.random() < 0.1 else None, # For re-auths or adjustments
        "adjustmentAmount": round(random.uniform(-100.00, 100.00), 2) if random.random() < 0.05 else 0.00,
        "adjustmentReason": fake.word() if random.random() < 0.05 else None,
        "lastUpdatedDate": datetime.datetime.now(),
        "dataSourceSystem": random.choice(["POS", "eCommerce Platform", "Mobile App", "Call Center"]),
        "externalRefId": fake.bothify(text='EXT########') if random.random() < 0.2 else None
    }

    # Combine all parts
    transaction_document = {
        "allocations": allocations,
        "comments": comments,
        "lineItems": line_items,
        "approvals": approvals,
        **other_fields  # Unpack the 80 other fields
    }
    return transaction_document

def main():
    client = None
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = client[DB_NAME]
        transactions_collection = db[COLLECTION_NAME]

        print(f"Connected to MongoDB database: '{DB_NAME}'")

        # Optional: Drop the collection if it exists (uncomment if you want to clear on each run)
        # If you drop, the IDs will always start from T001.
        # If you don't drop, they will continue from where the last run left off,
        # but won't be perfectly sequential across runs without more complex logic.
        if COLLECTION_NAME in db.list_collection_names():
            # If you want to drop the collection every time to ensure T001 starts fresh:
            # transactions_collection.drop()
            # print(f"Dropped existing collection: '{COLLECTION_NAME}'")
            pass # Keep it for adding new data, don't drop
        else:
            print(f"Collection '{COLLECTION_NAME}' does not exist, creating new one.")


        # Initialize the transaction ID counter
        # This will make IDs sequential *within this script run*, starting from 1.
        # If you want true global sequential IDs across multiple runs,
        # you would need to query the max ID from the DB first.
        transaction_id_counter = 0

        # Generate and insert data
        num_documents_to_insert = 100 # You can change this number
        documents = []
        for _ in range(num_documents_to_insert):
            transaction_id_counter += 1 # Increment for each new document
            doc = generate_random_transaction(transaction_id_counter)
            documents.append(doc)

        if documents:
            transactions_collection.insert_many(documents)
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