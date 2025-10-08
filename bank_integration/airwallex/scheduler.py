import frappe
from bank_integration.airwallex.transaction import sync_scheduled_transactions

def run_hourly_sync():
    """Run hourly sync for enabled setting"""
    try:
        # Get the single doctype instance
        setting = frappe.get_single("Bank Integration Setting")

        if (setting.enable_airwallex and
            setting.sync_schedule == "Hourly" and
            setting.sync_status != "In Progress"):

            sync_scheduled_transactions("Bank Integration Setting", "Hourly")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Hourly Sync Error")

def run_daily_sync():
    """Run daily sync for enabled setting"""
    try:
        setting = frappe.get_single("Bank Integration Setting")

        if (setting.enable_airwallex and
            setting.sync_schedule == "Daily" and
            setting.sync_status != "In Progress"):

            sync_scheduled_transactions("Bank Integration Setting", "Daily")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Daily Sync Error")

def run_weekly_sync():
    """Run weekly sync for enabled setting"""
    try:
        setting = frappe.get_single("Bank Integration Setting")

        if (setting.enable_airwallex and
            setting.sync_schedule == "Weekly" and
            setting.sync_status != "In Progress"):

            sync_scheduled_transactions("Bank Integration Setting", "Weekly")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Weekly Sync Error")

def run_monthly_sync():
    """Run monthly sync for enabled setting"""
    try:
        setting = frappe.get_single("Bank Integration Setting")

        if (setting.enable_airwallex and
            setting.sync_schedule == "Monthly" and
            setting.sync_status != "In Progress"):

            sync_scheduled_transactions("Bank Integration Setting", "Monthly")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Monthly Sync Error")
