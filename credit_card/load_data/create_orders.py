import pymongo
import random
import datetime
from faker import Faker

# Initialize Faker for realistic data
fake = Faker()

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://main_user:AdminAdmin1@cluster1.fgc5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
DB_NAME = "credit_card"
COLLECTION_NAME = "orders"

def generate_random_order(transaction_id_counter):
    """Generates a single credit card order document with random data."""

    # Subdocuments
    transactions = []
    num_transactions = random.randint(1, 5)
    for _ in range(num_transactions):
        transaction_id_counter += 1
        transactions.append({
            "transactionId": f"T{transaction_id_counter:03d}",
            "amount": round(random.uniform(5.00, 1000.00), 2),
            "currency": "USD",
            "timestamp": fake.date_time_between(start_date="-1y", end_date="now")
        })

    allocations = []
    num_allocations = random.randint(1, 3)
    for _ in range(num_allocations):
        allocations.append({
            "allocationId": fake.uuid4(),
            "amount": round(random.uniform(10.00, 500.00), 2),
            "category": fake.random_element(elements=('Groceries', 'Utilities', 'Entertainment', 'Travel', 'Online Shopping')),
            "status": fake.random_element(elements=('Applied', 'Pending', 'Rejected'))
        })

    comments = []
    num_comments = random.randint(0, 3)
    for _ in range(num_comments):
        comments.append({
            "commentId": fake.uuid4(),
            "text": fake.sentence(nb_words=10),
            "timestamp": fake.date_time_between(start_date="-6m", end_date="now"),
            "author": fake.name()
        })

    line_items = []
    num_line_items = random.randint(1, 5)
    for _ in range(num_line_items):
        line_items.append({
            "itemId": fake.uuid4(),
            "description": fake.catch_phrase(),
            "quantity": random.randint(1, 10),
            "unitPrice": round(random.uniform(1.00, 200.00), 2),
            "totalPrice": round(random.uniform(5.00, 1000.00), 2)
        })

    # 70 other fields (guessing at realistic credit card order fields)
    other_fields = {
        "orderId": fake.uuid4(),
        "customerId": fake.uuid4(),
        "cardNumberLastFour": str(random.randint(1000, 9999)),
        "merchantName": fake.company(),
        "merchantCategoryCode": str(random.randint(1000, 9999)),
        "transactionType": random.choice(["Purchase", "Refund", "Cash Advance", "Payment"]),
        "orderStatus": random.choice(["Completed", "Pending", "Cancelled", "Fraud_Detected"]),
        "orderDate": fake.date_time_between(start_date="-1y", end_date="now"),
        "billingAddressLine1": fake.street_address(),
        "billingAddressLine2": fake.secondary_address(),
        "billingCity": fake.city(),
        "billingState": fake.state_abbr(),
        "billingZipCode": fake.postcode(),
        "billingCountry": fake.country_code(),
        "shippingAddressLine1": fake.street_address(),
        "shippingAddressLine2": fake.secondary_address(),
        "shippingCity": fake.city(),
        "shippingState": fake.state_abbr(),
        "shippingZipCode": fake.postcode(),
        "shippingCountry": fake.country_code(),
        "totalAmount": round(random.uniform(10.00, 5000.00), 2),
        "taxAmount": round(random.uniform(0.00, 500.00), 2),
        "shippingCost": round(random.uniform(0.00, 50.00), 2),
        "discountAmount": round(random.uniform(0.00, 200.00), 2),
        "currencyCode": "USD",
        "paymentMethod": random.choice(["Credit Card", "Debit Card", "Digital Wallet"]),
        "cardHolderName": fake.name(),
        "cardBrand": random.choice(["Visa", "Mastercard", "Amex", "Discover"]),
        "cardExpiryMonth": str(random.randint(1, 12)).zfill(2),
        "cardExpiryYear": str(random.randint(datetime.datetime.now().year, datetime.datetime.now().year + 5)),
        "authCode": fake.bothify(text='######'),
        "arn": fake.bothify(text='####################'), # Acquirer Reference Number
        "retrievalReferenceNumber": fake.bothify(text='############'),
        "terminalId": fake.bothify(text='??????????'),
        "posEntryMode": random.choice(["01", "02", "05", "90"]),
        "posConditionCode": random.choice(["00", "01", "03"]),
        "networkReferenceId": fake.uuid4(),
        "settlementDate": datetime.datetime.combine(fake.date_this_year(), datetime.datetime.min.time()),        "invoiceNumber": fake.bothify(text='INV-########'),
        "customerEmail": fake.email(),
        "customerPhone": fake.phone_number(),
        "ipAddress": fake.ipv4(),
        "userAgent": fake.user_agent(),
        "deviceType": random.choice(["Mobile", "Desktop", "Tablet"]),
        "browser": random.choice(["Chrome", "Firefox", "Safari", "Edge"]),
        "operatingSystem": random.choice(["Windows", "MacOS", "iOS", "Android"]),
        "countryOfOrigin": fake.country_code(),
        "fraudScore": round(random.uniform(0.0, 100.0), 2),
        "riskLevel": random.choice(["Low", "Medium", "High", "Critical"]),
        "recommendation": random.choice(["Approve", "Deny", "Review"]),
        "reasonCode": random.choice(["", "CVV_Mismatch", "Address_Mismatch", "High_Value", "Multiple_Attempts"]),
        "processorResponseCode": random.choice(["00", "01", "05", "51", "91"]),
        "processorResponseMessage": fake.sentence(nb_words=5),
        "issuerBankName": fake.bank_country(),
        "acquirerBankName": fake.bank_country(),
        "interchangeFee": round(random.uniform(0.1, 2.0), 2),
        "processingFee": round(random.uniform(0.05, 1.5), 2),
        "chargebackStatus": random.choice(["None", "Initiated", "Represented", "Won", "Lost"]),
        "chargebackReasonCode": random.choice(["", "13.1", "4837", "4840", "4863"]),
        "disputeStatus": random.choice(["None", "Open", "Closed"]),
        "refundId": fake.uuid4() if random.random() < 0.2 else None, # Sometimes null
        "partialRefund": random.choice([True, False]),
        "originalOrderId": fake.uuid4() if random.random() < 0.1 else None, # For refunds/chargebacks
        "loyaltyPointsEarned": random.randint(0, 500),
        "promotionCodeUsed": fake.word() if random.random() < 0.3 else None,
        "isRecurring": random.choice([True, False]),
        "subscriptionId": fake.uuid4() if random.random() < 0.1 else None,
        "serviceType": random.choice(["Goods", "Services", "Digital"]),
        "deliveryMethod": random.choice(["Shipping", "Pickup", "Digital Download"]),
        "fulfillmentStatus": random.choice(["Fulfilled", "Partially Fulfilled", "Pending Fulfillment"]),
        "returnStatus": random.choice(["None", "Initiated", "Completed"]),
        "lastModifiedDate": fake.date_time_between(start_date="-3m", end_date="now"),
        "dataSource": "API",
        "systemVersion": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "auditLog": [{
            "action": "Created",
            "timestamp": fake.date_time_between(start_date="-1y", end_date="now"),
            "user": "System"
        }, {
            "action": "Updated",
            "timestamp": fake.date_time_between(start_date="-6m", end_date="now"),
            "user": fake.name()
        }]
    }

    # Combine all parts
    order_document = {
        "transactions": transactions,
        "allocations": allocations,
        "comments": comments,
        "lineItems": line_items,
        **other_fields  # Unpack the 70 other fields
    }
    return order_document, transaction_id_counter

def main():
    client = None  # Initialize client to None
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = client[DB_NAME]
        orders_collection = db[COLLECTION_NAME]

        print(f"Connected to MongoDB database: '{DB_NAME}'")

        # Drop the collection if it exists
        if COLLECTION_NAME in db.list_collection_names():
            orders_collection.drop()
            print(f"Dropped existing collection: '{COLLECTION_NAME}'")
        else:
            print(f"Collection '{COLLECTION_NAME}' does not exist, creating new one.")

        # Generate and insert data
        num_documents_to_insert = 100  # You can change this number
        documents = []
        transaction_id_counter = 0
        for _ in range(num_documents_to_insert):
            doc, transaction_id_counter = generate_random_order(transaction_id_counter)
            documents.append(doc)

        if documents:
            orders_collection.insert_many(documents)
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