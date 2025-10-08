# Airwallex Financial Transaction to ERPNext Bank Transaction Mapping Strategy

| ERPNext Field                  | Airwallex Field             | Description                                                                 |
|-------------------------------|-----------------------------|-----------------------------------------------------------------------------|
| `date`                        | `created_at`                | Transaction creation timestamp (convert to YYYY-MM-DD)                      |
| `status`                      | `status`                    | Transaction status (`PENDING`, `SETTLED`, `CANCELLED`), equivalent to `Pending`, `Settled`, `Unreconciled`, `Reconciled`, `Cancelled` in ERPNext                            |
| `bank_account`                | `funding_source_id`         | Map to ERPNext Bank Account via lookup                                     |
| `currency`                    | `currency`                  | ISO 4217 currency code (e.g. CNY, USD)                                      |
| `description`                 | `description` or `source_type` | Use `description` if available, fallback to `source_type`               |
| `reference_number`            | `batch_id`                  | Optional batch reference ID                                                 |
| `transaction_id`              | `id`                        | Unique Airwallex transaction ID                                             |
| `transaction_type`            | `transaction_type`          | e.g. `PAYMENT`, `CONVERSION`, etc. (see transaction types below)            |
| `deposit`                     | `net` (if positive)          | Net amount received (used for incoming funds)                               |
| `withdrawal`                  | `net` (if negative)          | Net amount paid out (used for outgoing funds)                               |
| `bank_party_name`             | -                           | Standard ERPNext field (not mapped from Airwallex)                         |
| `bank_party_account_number`   | -                           | Standard ERPNext field (not mapped from Airwallex)                         |
| **Custom Field: `airwallex_source_type`** | `source_type`               | Transaction source type (see options below)                                 |
| **Custom Field: `airwallex_source_id`**   | `source_id`                 | Optional: source identifier from Airwallex                                 |

## Custom Fields Required

The following custom fields need to be added to the ERPNext Bank Transaction doctype:

1. **`airwallex_source_type`** (Data field)
   - Label: "Airwallex Source Type"
   - Field Type: Data
   - Options: None (stores raw Airwallex source_type values)

2. **`airwallex_source_id`** (Data field)
   - Label: "Airwallex Source ID"
   - Field Type: Data
   - Description: "Source identifier from Airwallex transaction"

## Airwallex Source Type Options

The `source_type` field can contain the following values:

- `CONVERSION` - Currency conversion transactions
- `DEPOSIT` - Incoming deposit transactions  
- `ADJUSTMENT` - Account balance adjustments
- `FEE` - Platform or service fees
- `PAYMENT_ATTEMPT` - Payment processing attempts
- `REFUND` - Refund transactions
- `DISPUTE` - Chargeback or dispute transactions
- `CHARGE` - Direct charges or debits
- `TRANSFER` - Transfer transactions between accounts
- `YIELD` - Interest or yield payments
- `BATCH_PAYOUT` - Batch payout transactions
- `CARD_PURCHASE` - Card-based purchase transactions
- `CARD_REFUND` - Card-based refund transactions
- `PURCHASE` - General purchase transactions
- `REFUND_REVERSAL` - Reversed refund transactions

## Airwallex Transaction Type Options

The `transaction_type` field can contain the following values:

- `DISPUTE_REVERSAL` - Reversal of dispute transactions
- `DISPUTE_LOST` - Lost dispute transactions
- `REFUND` - Refund transactions
- `REFUND_REVERSAL` - Reversed refund transactions
- `REFUND_FAILURE` - Failed refund transactions
- `PAYMENT_RESERVE_HOLD` - Payment reserve hold transactions
- `PAYMENT_RESERVE_RELEASE` - Payment reserve release transactions
- `PAYOUT` - Payout transactions
- `PAYOUT_FAILURE` - Failed payout transactions
- `PAYOUT_REVERSAL` - Reversed payout transactions
- `CONVERSION_SELL` - Currency conversion sell transactions
- `CONVERSION_BUY` - Currency conversion buy transactions
- `CONVERSION_REVERSAL` - Reversed conversion transactions
- `DEPOSIT` - Deposit transactions
- `ADJUSTMENT` - Account adjustment transactions
- `FEE` - Fee transactions
- `DD_CREDIT` - Direct debit credit transactions
- `DD_DEBIT` - Direct debit debit transactions
- `DC_CREDIT` - Direct credit transactions
- `DC_DEBIT` - Direct debit transactions
- `TRANSFER` - Transfer transactions
- `PAYMENT` - Payment transactions
- `ISSUING_AUTHORISATION_HOLD` - Card issuing authorization hold
- `ISSUING_AUTHORISATION_RELEASE` - Card issuing authorization release
- `ISSUING_CAPTURE` - Card issuing capture transactions
- `ISSUING_REFUND` - Card issuing refund transactions
- `PURCHASE` - Purchase transactions
- `PREPAYMENT` - Prepayment transactions
- `PREPAYMENT_RELEASE` - Prepayment release transactions
