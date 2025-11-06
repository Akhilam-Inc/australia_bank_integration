# Data Mapping

## Overview

This document describes how Airwallex transaction data is mapped to ERPNext Bank Transaction format, including transaction filtering logic.

## Core Functions

### Transaction Mapping Function

The core mapping function is located in `bank_integration/airwallex/utils.py`:

```python
def map_airwallex_to_erpnext(txn, bank_account)
```

### Transaction Filtering Function

The filtering logic is located in `bank_integration/bank_integration/doctype/bank_integration_setting/bank_integration_setting.py`:

```python
def should_sync_transaction(self, transaction_type)
```

## Transaction Filtering Logic

### Pre-Processing Filter

Before mapping Airwallex data to ERPNext format, each transaction goes through a filtering process:

```python
# In sync_client_transactions()
transaction_type = txn.get('transaction_type', '').upper()

# Check transaction type filtering
if not settings.should_sync_transaction(transaction_type):
    frappe.logger().info(f"Transaction {transaction_id} type '{transaction_type}' filtered out, skipping")
    processed += 1
    skipped += 1
    continue
```

### Filtering Strategies

#### 1. No Filters (Default)
```python
# If no filters configured
if not self.transaction_type_filters:
    return True  # Sync all transactions
```

#### 2. Whitelist Approach (Include Filters)
```python
# If any "Include" filters exist
has_include_filters = any(f.filter_action == "Include" for f in self.transaction_type_filters)

if has_include_filters:
    # Only sync explicitly included types
    for filter_rule in self.transaction_type_filters:
        if filter_rule.transaction_type == transaction_type and filter_rule.filter_action == "Include":
            return True
    return False  # Not in include list
```

#### 3. Blacklist Approach (Exclude Filters)
```python
# If only "Exclude" filters exist
for filter_rule in self.transaction_type_filters:
    if filter_rule.transaction_type == transaction_type and filter_rule.filter_action == "Exclude":
        return False  # Explicitly excluded

return True  # Not in exclude list, so sync
```

### Supported Transaction Types

The system supports all Airwallex transaction types:

```
DISPUTE_REVERSAL, DISPUTE_LOST, REFUND, REFUND_REVERSAL, REFUND_FAILURE,
PAYMENT_RESERVE_HOLD, PAYMENT_RESERVE_RELEASE, PAYOUT, PAYOUT_FAILURE,
PAYOUT_REVERSAL, CONVERSION_SELL, CONVERSION_BUY, CONVERSION_REVERSAL,
DEPOSIT, ADJUSTMENT, FEE, DD_CREDIT, DD_DEBIT, DC_CREDIT, DC_DEBIT,
TRANSFER, PAYMENT, ISSUING_AUTHORISATION_HOLD, ISSUING_AUTHORISATION_RELEASE,
ISSUING_CAPTURE, ISSUING_REFUND, PURCHASE, PREPAYMENT, PREPAYMENT_RELEASE
```

## Field Mapping

### Direct Mappings

| ERPNext Field | Airwallex Field | Transformation |
|---------------|-----------------|----------------|
| `date` | `created_at` | Extract date part (YYYY-MM-DD) |
| `currency` | `currency` | Direct mapping |
| `description` | `description` or `source_type` | Use description, fallback to source_type |
| `reference_number` | `batch_id` | Direct mapping |
| `transaction_id` | `id` | Direct mapping (used for duplicate detection) |
| `transaction_type` | `transaction_type` | Direct mapping |
| `airwallex_source_type` | `source_type` | Custom field |
| `airwallex_source_id` | `source_id` | Custom field |

### Conditional Mappings

#### Status Mapping

```python
def map_airwallex_status_to_erpnext(airwallex_status):
    status_mapping = {
        "PENDING": "Unreconciled",
        "SETTLED": "Settled",
        "CANCELLED": "Cancelled"
    }
    return status_mapping.get(airwallex_status.upper(), "Unreconciled")
```

| Airwallex Status | ERPNext Status |
|------------------|----------------|
| PENDING | Unreconciled |
| SETTLED | Settled |
| CANCELLED | Cancelled |
| *Other* | Unreconciled (default) |

#### Amount Mapping

```python
amount = txn.get("net", 0)
is_deposit = amount > 0

# In ERPNext format:
"deposit": amount if is_deposit else 0,
"withdrawal": abs(amount) if not is_deposit else 0
```

- **Positive amount**: Mapped to `deposit`
- **Negative amount**: Mapped to `withdrawal` (absolute value)

#### Bank Account Mapping

```python
# Get transaction currency
txn_currency = txn.get("currency", "")

# Check if bank account currency matches
mapped_bank_account = None
if bank_account and txn_currency:
    # Fetch the bank account's currency
    account = frappe.db.get_value("Bank Account", bank_account, "account")
    bank_account_currency = frappe.db.get_value("Account", account, "account_currency")

    # Only map if currencies match
    if bank_account_currency == txn_currency:
        mapped_bank_account = bank_account
    else:
        frappe.logger().info("Currency mismatch")
```

**Logic**:
1. Get transaction currency
2. Get bank account's linked GL account currency
3. Compare currencies
4. If match: assign bank account
5. If mismatch: leave bank account blank

**Rationale**: Prevents incorrectly assigning transactions to wrong-currency bank accounts.

## Complete Processing Flow

### 1. Transaction Retrieval
```python
# Get transactions from Airwallex API
transactions = api.get_list(from_created_at=from_date_iso, to_created_at=to_date_iso)
```

### 2. Pre-Processing Validation
```python
# Check if transaction already exists (duplicate prevention)
if transaction_exists(transaction_id):
    continue

# Check transaction type filtering
if not settings.should_sync_transaction(transaction_type):
    continue

# Check basic currency validation
if not transaction_currency:
    continue
```

### 3. Data Mapping
```python
# Map Airwallex transaction to ERPNext format
bank_txn = map_airwallex_to_erpnext(txn, client.bank_account)
```

### 4. Document Creation
```python
# Create and submit ERPNext Bank Transaction
bank_txn_doc = frappe.get_doc(bank_txn)
bank_txn_doc.insert()
bank_txn_doc.submit()
```

## Sample Transformation

### Input (Airwallex)

```json
{
  "amount": 200.21,
  "batch_id": "bat_20201202_SGD_2",
  "client_rate": 6.93,
  "created_at": "2021-03-22T16:08:02",
  "currency": "CNY",
  "description": "deposit to account",
  "id": "7f687fe6-dcf4-4462-92fa-80335301d9d2",
  "net": 100.21,
  "settled_at": "2021-03-22T16:08:02",
  "source_id": "9f687fe6-dcf4-4462-92fa-80335301d9d2",
  "source_type": "PAYMENT_ATTEMPT",
  "status": "PENDING",
  "transaction_type": "PAYMENT"
}
```

### Transaction Filter Check

```python
# Check if PAYMENT type should be synced
settings = frappe.get_single("Bank Integration Setting")
should_sync = settings.should_sync_transaction("PAYMENT")

# If filter exists and excludes PAYMENT, or no include filter for PAYMENT:
if not should_sync:
    # Transaction is skipped, not mapped
    return
```

### Output (ERPNext Bank Transaction)

```python
{
  "doctype": "Bank Transaction",
  "date": "2021-03-22",
  "status": "Unreconciled",
  "bank_account": "CNY Bank Account",  # Only if currency matches
  "currency": "CNY",
  "description": "deposit to account",
  "reference_number": "bat_20201202_SGD_2",
  "transaction_id": "7f687fe6-dcf4-4462-92fa-80335301d9d2",
  "transaction_type": "PAYMENT",
  "deposit": 100.21,
  "withdrawal": 0,
  "airwallex_source_type": "PAYMENT_ATTEMPT",
  "airwallex_source_id": "9f687fe6-dcf4-4462-92fa-80335301d9d2"
}
```

## Error Handling

### Filtering Errors
- **Unknown transaction type**: Filtered based on default strategy
- **Missing transaction type**: Skipped with warning log
- **Filter configuration errors**: Logged but don't stop sync

### Mapping Errors
- **Currency mismatch**: Bank account left blank, transaction still created
- **Missing required fields**: Transaction skipped with error log
- **Amount parsing errors**: Default to 0, log warning

### Duplicate Handling
- **Existing transaction_id**: Skip mapping, increment skip counter
- **Database constraint violations**: Catch and skip gracefully

## Performance Considerations

### Filtering Impact
- **Early filtering**: Reduces unnecessary mapping operations
- **Database queries**: Currency check requires 2 DB queries per transaction
- **Logging**: Filtered transactions are logged for audit trail

### Optimization Techniques
- **Batch processing**: Process transactions in chunks
- **Progress updates**: Update progress every 10 transactions
- **Connection pooling**: Reuse database connections
- **Token caching**: Avoid repeated authentication

## Monitoring and Debugging

### Log Messages
```python
# Successful mapping
frappe.logger().info(f"Created transaction {transaction_id} of type {transaction_type}")

# Filtered transaction
frappe.logger().info(f"Transaction {transaction_id} type '{transaction_type}' filtered out, skipping")

# Currency mismatch
frappe.logger().info(f"Currency mismatch: Transaction {transaction_id} currency {txn_currency} doesn't match Bank Account {bank_account} currency {bank_account_currency}")
```

### Counters
- `processed`: Total transactions examined
- `created`: Successfully mapped and created
- `skipped`: Filtered out or duplicates
- `errors`: Failed mapping attempts

### Best Practices
1. **Monitor skip ratios**: High skip rates may indicate filter misconfiguration
2. **Check currency mismatches**: May indicate wrong bank account assignment
3. **Review error logs**: Failed mappings indicate data issues
4. **Test filters thoroughly**: Use small date ranges to verify behavior
