import frappe
from bank_integration.airwallex.api.financial_transactions import FinancialTransactions
from bank_integration.airwallex.utils import map_airwallex_to_erpnext
from  bank_integration.bank_integration.doctype.bank_integration_log import bank_integration_log as bi_log
from datetime import datetime
import traceback


def sync_transactions(from_date, to_date, setting_name):
    """
    Sync transactions from Airwallex to ERPNext Bank Transactions
    """
    setting = None
    bi_log.create_log(f"Starting transaction sync from {from_date} to {to_date}")
    try:
        # Get the setting document first
        setting = frappe.get_doc("Bank Integration Setting", setting_name)

        # Initialize the API
        ft_api = FinancialTransactions()

        # Initialize counters
        page_num = 0
        page_size = 100
        total_processed = 0
        total_created = 0
        total_errors = 0

        # Convert dates to ISO format for API
        from_created_at = from_date  # Just the date: "2025-10-06"
        to_created_at = to_date      # Just the date: "2025-10-08"

        frappe.logger().info(f"Starting transaction sync from {from_date} to {to_date}")

        # Update initial status
        setting.update_sync_progress(0, 0, "In Progress")

        while True:
            # Get transactions from Airwallex
            response = ft_api.get_list(
                from_created_at=from_created_at,
                to_created_at=to_created_at,
                page_num=page_num,
                page_size=page_size
            )

            if not response or not response.get('items'):
                break

            transactions = response.get('items', [])
            has_more = response.get('has_more', False)

            # Process each transaction
            for txn in transactions:
                try:
                    # Check if transaction already exists using the correct field
                    if transaction_exists(txn.get('id')):
                        frappe.logger().info(f"Transaction {txn.get('id')} already exists, skipping")
                        total_processed += 1
                        continue

                    # Map and create ERPNext Bank Transaction
                    erpnext_txn = map_airwallex_to_erpnext(txn)

                    # Create the Bank Transaction document
                    bank_txn_doc = frappe.get_doc(erpnext_txn)
                    bank_txn_doc.insert()

                    total_created += 1
                    total_processed += 1

                    frappe.logger().info(f"Created Bank Transaction: {bank_txn_doc.name}")

                except Exception as e:
                    total_errors += 1
                    total_processed += 1
                    frappe.logger().error(f"Error processing transaction {txn.get('id')}: {str(e)}")
                    frappe.log_error(traceback.format_exc(), f"Transaction Sync Error - {txn.get('id')}")

            # Update progress (use processed as total since we don't have total count)
            setting.update_sync_progress(total_processed, total_processed, "In Progress")

            # Check if there are more pages
            if not has_more:
                break

            page_num += 1

        # Final status update (fix the syntax error)
        final_status = "Completed" if total_errors == 0 else "Completed with Errors"
        setting.update_sync_progress(total_processed, total_processed, final_status)

        # Log summary
        frappe.logger().info(
            f"Transaction sync completed. "
            f"Processed: {total_processed}, Created: {total_created}, Errors: {total_errors}"
        )

        # Send notification
        frappe.publish_realtime(
            'transaction_sync_complete',
            {
                'processed': total_processed,
                'created': total_created,
                'errors': total_errors,
                'status': final_status,
                'message': f"Sync completed successfully. Created {total_created} transactions."
            },
            user=frappe.session.user
        )

    except Exception as e:
        # Update status to Failed
        if setting:
            setting.update_sync_progress(0, 0, "Failed")

        error_msg = f"Transaction sync failed: {str(e)}"
        frappe.log_error(traceback.format_exc(), "Transaction Sync Failed")
        frappe.logger().error(error_msg)

        # Send error notification
        frappe.publish_realtime(
            'transaction_sync_complete',
            {
                'processed': 0,
                'created': 0,
                'errors': 1,
                'status': 'error',
                'message': error_msg
            },
            user=frappe.session.user
        )


def get_bank_account_lookup():
    """
    Build a lookup dictionary mapping funding_source_id to ERPNext Bank Account names

    Returns:
        dict: Mapping of funding_source_id to bank account names
    """
    # This is a placeholder - you'll need to implement based on how you store
    # the mapping between Airwallex funding sources and ERPNext bank accounts

    # Option 1: If you have a custom doctype for mapping
    # bank_accounts = frappe.get_all(
    #     "Airwallex Bank Account Mapping",
    #     fields=["funding_source_id", "bank_account"]
    # )
    # return {account.funding_source_id: account.bank_account for account in bank_accounts}

    # Option 2: Simple mapping (you can configure this)
    return {
        "99d23411-234-22dd-23po-13sd7c267b9e": "Airwallex CNY Account",
        # Add more mappings as needed
    }


def transaction_exists(transaction_id):
    """
    Check if a Bank Transaction with the given Airwallex source ID already exists
    """
    # Check using the custom field we added for Airwallex source ID
    return frappe.db.exists("Bank Transaction", {"airwallex_source_id": transaction_id})


def sync_scheduled_transactions(setting_name, schedule_type):
    """
    Sync transactions based on schedule type
    """
    from datetime import datetime, timedelta

    try:
        # For single doctype, use get_single instead of get_doc
        setting = frappe.get_single("Bank Integration Setting")

        # Check if sync is already in progress
        if setting.sync_status == "In Progress":
            frappe.logger().info(f"Sync already in progress, skipping {schedule_type} sync")
            return

        if not setting.is_enabled():
            frappe.logger().info(f"Airwallex integration disabled")
            return

        # Set status to prevent concurrent runs
        setting.db_set('sync_status', 'In Progress')
        setting.db_set('last_sync_date', frappe.utils.now())

        # Calculate date range based on schedule type
        end_date = datetime.now().date()

        if schedule_type == "Hourly":
            # Sync last 2 hours
            start_date = (datetime.now() - timedelta(hours=2)).date()
        elif schedule_type == "Daily":
            # Sync yesterday
            start_date = end_date - timedelta(days=1)
        elif schedule_type == "Weekly":
            # Sync last 7 days
            start_date = end_date - timedelta(days=7)
        elif schedule_type == "Monthly":
            # Sync last 30 days
            start_date = end_date - timedelta(days=30)
        else:
            frappe.logger().error(f"Unknown schedule type: {schedule_type}")
            setting.db_set('sync_status', 'Failed')
            return

        bi_log.create_log(f"Starting scheduled {schedule_type} sync from {start_date} to {end_date}")
        frappe.logger().info(f"Starting scheduled {schedule_type} sync from {start_date} to {end_date}")

        # Use the existing sync function with calculated dates
        # Pass the doctype name since it's a single doctype
        sync_transactions(str(start_date), str(end_date), "Bank Integration Setting")

    except Exception as e:
        # Make sure to reset status on error
        try:
            setting = frappe.get_single("Bank Integration Setting")
            setting.db_set('sync_status', 'Failed')
        except:
            pass

        error_msg = f"Scheduled {schedule_type} sync failed: {str(e)}"
        bi_log.create_log(error_msg, status="Error")
        frappe.log_error(frappe.get_traceback(), f"Scheduled Sync Error - {schedule_type}")
        frappe.logger().error(error_msg)
