# Credit Card Data Processing System

This repository contains a comprehensive system for managing, analyzing, and processing credit card data. It provides tools for data generation, storage, retrieval, and analysis to support credit card operations.

## Directory Structure

The `credit_card` directory contains the following components:

### Load Data

Scripts for generating and populating credit card datasets:

- **create_accounts.py**: Generates synthetic credit card account data with account numbers, limits, and customer associations
- **create_orders.py**: Creates order records associated with accounts, including order dates, amounts, and status
- **create_transactions.py**: Generates transaction data for accounts with transaction types, amounts, timestamps, and merchant information
- **create_users.py**: Creates user data including personal information and account associations

### Query Data

Tools for querying and analyzing the credit card data:

- **generate_array.py**: Creates an array of unique hierarchical IDs with variable depth for testing query performance
- **hierarchy_query.json**: Contains generated hierarchical IDs (1,500 entries) representing different organizational paths
- **query_users.py**: Script for retrieving and filtering user data based on various criteria
- **sample_query.js**: JavaScript examples demonstrating how to query the data in different ways

## Hierarchical Data Structure

The system uses a hierarchical ID system to represent organizational relationships with the following segments:

| Segment | Description             | Example    |
|---------|-------------------------|------------|
| CLI     | Client identifier       | CLI_000023 |
| BAN     | Bank account number     | BAN_000088 |
| AGE     | Age group identifier    | AGE_000045 |
| COM     | Company identifier      | COM_000050 |
| DIV     | Division code           | DIV_000042 |
| DEP     | Department code         | DEP_000039 |

Examples of complete hierarchy IDs:
- `CLI_000023-BAN_000088-AGE_000045-COM_000050-DIV_000042`
- `CLI_000060-BAN_000082-AGE_000089-COM_000037-DIV_000050`
- `CLI_000031-BAN_000046-AGE_000006-COM_000020-DIV_000037-DEP_000073`

The hierarchical structure allows for flexible querying and aggregation at different organizational levels.

## Usage

### Generating Test Data

To generate sample credit card data:

```bash
cd credit_card/load_data
python create_orders.py
python create_accounts.py
python create_users.py
python create_transactions.py
```

### Generating Hierarchy IDs

To generate a new set of hierarchy IDs for testing:

```bash
cd credit_card/query_data
python generate_array.py
```

This will create a new `hierarchy_query.json` file containing 1,500 unique, randomly generated hierarchy IDs with variable depth.

### Running Queries

Use the query scripts to analyze and retrieve data based on hierarchical IDs:

```bash
cd credit_card/query_data
python query_users.py
```
The system supports partial hierarchies to query at any level of the organization structure.

## Data Analysis Capabilities

The system provides tools to:
- Aggregate transaction data by account, client, or organizational unit
- Analyze spending patterns across different departments or divisions
- Track order history and fulfillment status
- Generate reports on user activity and account usage
