import frappe
from bank_integration.airwallex.api.base_api import AirwallexBase


class FinancialTransactions(AirwallexBase):
    """API class for Airwallex Financial Transactions endpoint"""

    def __init__(self):
        super().__init__()

    def get_list(self, batch_id=None, currency=None, from_created_at=None,
                 page_num=None, page_size=None, source_id=None, status=None,
                 to_created_at=None):
        """
        Get list of financial transactions

        Args:
            batch_id (str, optional): Batch ID of the financial transaction
            currency (str, optional): The currency (3-letter ISO-4217 code) of the financial transaction
            from_created_at (str, optional): The start time of created_at in ISO8601 format (inclusive)
            page_num (int, optional): Page number, starts from 0
            page_size (int, optional): Number of results per page, default is 100, max is 1000
            source_id (str, optional): The source ID of the transaction
            status (str, optional): Status of the financial transaction, one of: PENDING, SETTLED
            to_created_at (str, optional): The end time of created_at in ISO8601 format (inclusive)

        Returns:
            dict: API response containing list of financial transactions
        """
        params = {}

        # Add parameters only if they are provided
        if batch_id is not None:
            params['batch_id'] = batch_id
        if currency is not None:
            params['currency'] = currency
        if from_created_at is not None:
            params['from_created_at'] = from_created_at
        if page_num is not None:
            params['page_num'] = page_num
        if page_size is not None:
            params['page_size'] = page_size
        if source_id is not None:
            params['source_id'] = source_id
        if status is not None:
            params['status'] = status
        if to_created_at is not None:
            params['to_created_at'] = to_created_at

        return self.get(endpoint="financial_transactions", params=params)

    def get_by_id(self, transaction_id):
        """
        Get a specific financial transaction by ID

        Args:
            transaction_id (str): The ID of the financial transaction

        Returns:
            dict: API response containing the financial transaction details
        """
        return self.get(endpoint=f"financial_transactions/{transaction_id}")

def test_get_transactions():
    # bench execute bank_integration.airwallex.api.financial_transactions.test_get_transactions
	ft_api = FinancialTransactions()
	response = ft_api.get_list(page_num=0, page_size=10)
	print(response)
