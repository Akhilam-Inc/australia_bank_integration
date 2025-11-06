# Configuration Guide

## Bank Integration Setting

The Bank Integration Setting is a Single DocType that holds all configuration for the Airwallex integration.

### Access

Navigate to: **Bank Integration** workspace → **Bank Integration Setting**

### Configuration Fields

#### Integration Settings

| Field | Type | Description |
|-------|------|-------------|
| `enable_airwallex` | Checkbox | Enable/disable the Airwallex integration |
| `api_url` | Data | Airwallex API base URL |
| `enable_log` | Checkbox | Enable detailed API logging |

#### Token Management (Auto-managed)

| Field | Type | Description |
|-------|------|-------------|
| `token` | Small Text | Cached authentication token (auto-populated) |
| `token_expiry` | Datetime | Token expiration time (auto-populated) |

#### Scheduled Sync Settings

| Field | Type | Description |
|-------|------|-------------|
| `sync_schedule` | Select | Schedule frequency: Hourly, Daily, Weekly, Monthly |
| `last_sync_date` | Datetime | Last successful sync timestamp (auto-updated) |

#### Manual Sync Settings

| Field | Type | Description |
|-------|------|-------------|
| `sync_old_transactions` | Checkbox | Enable manual sync for historical transactions |
| `from_date` | Datetime | Start date for manual sync |
| `to_date` | Datetime | End date for manual sync |

#### Sync Status (Auto-managed)

| Field | Type | Description |
|-------|------|-------------|
| `sync_status` | Select | Current sync status: Not Started, In Progress, Completed, Completed with Errors, Failed |
| `processed_records` | Int | Number of transactions processed (auto-updated) |
| `total_records` | Int | Total transactions to process (auto-updated) |
| `sync_progress` | Percent | Sync progress percentage (auto-updated) |

#### Airwallex Clients (Child Table)

| Field | Type | Description |
|-------|------|-------------|
| `airwallex_client_id` | Data | Client ID from Airwallex (required) |
| `airwallex_api_key` | Password | API Key from Airwallex (required) |
| `bank_account` | Link | ERPNext Bank Account to map transactions to (required) |
| `token` | Small Text | Client-specific cached token (auto-managed) |
| `token_expiry` | Datetime | Client-specific token expiry (auto-managed) |

#### Transaction Type Filters (Child Table)

| Field | Type | Description |
|-------|------|-------------|
| `transaction_type` | Select | Airwallex transaction type to filter |
| `filter_action` | Select | Include or Exclude this transaction type |

**Available Transaction Types:**
- `PAYMENT` - Payment transactions
- `REFUND` - Refund transactions
- `DEPOSIT` - Deposit transactions
- `WITHDRAWAL` - Withdrawal transactions
- `FEE` - Fee transactions
- `ADJUSTMENT` - Account adjustment transactions
- `TRANSFER` - Transfer transactions
- `CONVERSION_SELL` - Currency conversion sell transactions
- `CONVERSION_BUY` - Currency conversion buy transactions
- `PAYOUT` - Payout transactions
- `DISPUTE_REVERSAL` - Dispute reversal transactions
- And 18 additional types (see [Transaction Mapping Reference](transaction_mapping.md) for complete list)

## Transaction Type Filtering

### How It Works

The transaction type filtering system allows you to control which Airwallex transaction types are imported into ERPNext.

#### Filtering Strategies

**1. Whitelist Approach (Include Filters)**
- Add "Include" filters for transaction types you want to sync
- Only the specified types will be imported
- All other types will be skipped

**2. Blacklist Approach (Exclude Filters)**
- Add "Exclude" filters for transaction types you don't want to sync
- All types except the excluded ones will be imported

**3. No Filters**
- If no filters are configured, all transaction types are imported
- This is the default behavior for backward compatibility

#### Filter Examples

**Example 1: Only sync payments and refunds**
```
Transaction Type: PAYMENT,     Action: Include
Transaction Type: REFUND,      Action: Include
```
Result: Only PAYMENT and REFUND transactions are imported.

**Example 2: Exclude fees and adjustments**
```
Transaction Type: FEE,         Action: Exclude
Transaction Type: ADJUSTMENT,  Action: Exclude
```
Result: All transaction types except FEE and ADJUSTMENT are imported.

**Example 3: Mixed filters (Not recommended)**
```
Transaction Type: PAYMENT,     Action: Include
Transaction Type: FEE,         Action: Exclude
```
Result: Since there's an Include filter, only PAYMENT transactions are imported (whitelist takes precedence).

#### Best Practices

1. **Use one strategy**: Either use all Include filters or all Exclude filters, not both
2. **Test thoroughly**: After setting up filters, run a small manual sync to verify behavior
3. **Monitor logs**: Check Bank Integration Logs to see which transactions are filtered out
4. **Start permissive**: Begin with no filters, then add exclusions as needed

## Setup Steps

### 1. Initial Configuration

1. Navigate to **Bank Integration Setting**
2. Set the **API URL** (e.g., `https://api.airwallex.com/api/v1`)
3. Optionally enable **Enable Log** for detailed logging

### 2. Add Airwallex Clients

For each Airwallex account you want to sync:

1. Click **Add Row** in the Airwallex Clients table
2. Enter **Airwallex Client ID**
3. Enter **Airwallex API Key**
4. Select the corresponding **Bank Account** in ERPNext
5. Click **Save**

**Important**: The bank account currency should match the currencies of transactions from that Airwallex client.

### 3. Configure Transaction Type Filters (Optional)

To control which transaction types are imported:

1. In the **Transaction Type Filters** section, click **Add Row**
2. Select a **Transaction Type** from the dropdown
3. Choose **Action**: Include or Exclude
4. Repeat for additional transaction types
5. Click **Save**

**Note**: If no filters are configured, all transaction types will be imported.

### 4. Test Authentication

1. Click the **Test Authentication** button
2. The system will verify credentials for all configured clients
3. Green checkmarks indicate successful authentication
4. Red errors indicate failed authentication (fix credentials and try again)

### 5. Enable Integration

1. Check **Enable Airwallex**
2. Click **Save**

**Note**: The system automatically tests authentication when you enable the integration. If authentication fails, the integration will be automatically disabled.

### 6. Configure Scheduled Sync

1. Select **Sync Schedule** (Hourly/Daily/Weekly/Monthly)
2. Click **Save**

The scheduler will automatically start syncing based on your schedule.

### 7. Configure Manual Sync (Optional)

For syncing historical transactions:

1. Check **Sync Old Transactions**
2. Set **From Date** and **To Date**
3. Click **Save**
4. Click **Start Sync** button that appears

## Validation Rules

- At least one Airwallex client must be configured
- Client ID, API Key, and Bank Account are required for each client
- Authentication must succeed before enabling the integration
- From Date must be before To Date for manual sync
- Sync cannot start if another sync is in progress
- Transaction type filters must have both transaction type and action specified

## Best Practices

1. **Test Authentication First**: Always test authentication before enabling
2. **Match Currencies**: Ensure bank account currency matches transaction currencies
3. **Configure Filters Early**: Set up transaction type filters before your first sync
4. **Start Small**: Begin with a short date range for manual sync to test
5. **Monitor Progress**: Watch the sync progress percentage during operation
6. **Check Logs**: Review Bank Integration Logs for any errors
7. **Review Filtered Transactions**: Check logs to see which transactions are being filtered out
8. **Credential Security**: API keys are stored encrypted as password fields

## Troubleshooting Transaction Filters

### Common Issues

**No transactions syncing after adding filters**
- Check if you have Include filters that are too restrictive
- Verify transaction types exist in your Airwallex data
- Review sync logs for "filtered out" messages

**Wrong transactions syncing**
- Review your filter strategy (Include vs Exclude)
- Check for typos in transaction type names
- Ensure you're using the correct Airwallex transaction type values

**Mixed Include/Exclude behavior**
- When Include filters exist, Exclude filters are ignored
- Use consistent filtering strategy (all Include or all Exclude)

### Debugging Steps

1. **Check logs**: Look for "filtered out" messages in ERPNext logs
2. **Test without filters**: Temporarily remove all filters to see all available transaction types
3. **Use small date range**: Test with 1-2 days of data to see filtering behavior
4. **Review Airwallex data**: Check what transaction types your Airwallex account actually generates
