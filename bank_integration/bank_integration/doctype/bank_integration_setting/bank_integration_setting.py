# Copyright (c) 2025, Akhilam Inc and contributors
# For license information, please see license.txt

from bank_integration.airwallex.api.airwallex_authenticator import AirwallexAuthenticator
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from frappe.utils import add_days, add_months, get_datetime, now_datetime
from frappe.utils.scheduler import is_scheduler_inactive

AUTH_ROUTE = '/api/v1/authentication/login'


class BankIntegrationSetting(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from bank_integration.bank_integration.doctype.airwallex_bank_account_mapping.airwallex_bank_account_mapping import AirwallexBankAccountMapping
        from frappe.types import DF

        api_key: DF.Password | None
        api_url: DF.Data | None
        bank_account_mappings: DF.Table[AirwallexBankAccountMapping]
        client_id: DF.Data | None
        enable_airwallex: DF.Check
        enable_log: DF.Check
        file_url: DF.Data | None
        from_date: DF.Date | None
        last_sync_date: DF.Datetime | None
        processed_records: DF.Int
        sync_old_transactions: DF.Check
        sync_progress: DF.Percent
        sync_schedule: DF.Literal["Hourly", "Daily", "Weekly", "Monthly"]
        sync_status: DF.Literal["Not Started", "In Progress", "Completed", "Failed"]
        to_date: DF.Date | None
        total_records: DF.Int
    # end: auto-generated types

    def is_enabled(self):
        return bool(self.enable_airwallex)

    def validate(self): # Temporarily disable Airwallex integration
        if self.is_enabled():
            self.test_authentication()

    def on_update(self):
        """Trigger sync job when sync_old_transactions is enabled"""
        if self.sync_old_transactions and self.sync_status == "Not Started":
            self.start_transaction_sync()

    def test_authentication(self):
        """Test authentication with Airwallex API"""
        try:
            api = AirwallexAuthenticator()
            response = api.authenticate()

            if response and response.get('token'):
                frappe.msgprint("Airwallex authentication successful!", indicator="green")
            else:
                frappe.throw("Authentication failed. Please check your credentials.")
        except Exception as e:
            import traceback
            frappe.msgprint(f"Bank Integration failed. Please check your credentials. {e}", indicator="red")
            frappe.log_error(traceback.format_exc(), "Airwallex Authentication Error")
            return False

    @frappe.whitelist()
    def start_transaction_sync(self):
        """Start background job for syncing transactions"""
        if not self.from_date or not self.to_date:
            frappe.throw("From and To dates are required for syncing old transactions")

        # Validate date range
        if self.from_date > self.to_date:
            frappe.throw("From date cannot be greater than To date")

        # Update status to indicate sync has started
        self.db_set('sync_status', 'In Progress')
        self.db_set('last_sync_date', frappe.utils.now())
        self.db_set('processed_records', 0)
        self.db_set('total_records', 0)
        self.db_set('sync_progress', 0)

        # Enqueue the sync job
        enqueue(
            'bank_integration.airwallex.transaction.sync_transactions',
            queue='long',
            timeout=3600,  # 1 hour timeout
            from_date=str(self.from_date),
            to_date=str(self.to_date),
            setting_name=self.name
        )

        frappe.msgprint(
            "Transaction sync job has been started. You can monitor the progress from this page.",
            indicator="blue"
        )

    @frappe.whitelist()
    def restart_transaction_sync(self):
        """Restart transaction sync by resetting status and starting new job"""
        if not self.from_date or not self.to_date:  # Changed from self.from to self.from_date
            frappe.throw("From and To dates are required for syncing old transactions")

        # Reset sync status and counters
        self.db_set('sync_status', 'Not Started')
        self.db_set('processed_records', 0)
        self.db_set('total_records', 0)
        self.db_set('sync_progress', 0)

        # Start the sync
        return self.start_transaction_sync()

    @frappe.whitelist()
    def stop_transaction_sync(self):
        """Stop the current transaction sync"""
        try:
            # Update status to stopped
            self.db_set('sync_status', 'Stopped')

            frappe.msgprint(
                "Transaction sync has been marked as stopped. The background job may take a moment to complete.",
                indicator="orange"
            )

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Failed to stop sync job")
            frappe.throw(f"Failed to stop sync job: {str(e)}")

    def update_sync_progress(self, processed, total, status="In Progress"):
        """Update sync progress"""
        progress = (processed / total * 100) if total > 0 else 0

        self.db_set('processed_records', processed)
        self.db_set('total_records', total)
        self.db_set('sync_progress', progress)
        self.db_set('sync_status', status)
        self.db_set('last_sync_date', frappe.utils.now())

        frappe.publish_realtime(
            'transaction_sync_progress',
            {
                'processed': processed,
                'total': total,
                'progress': progress,
                'status': status
            },
            user=frappe.session.user
        )
