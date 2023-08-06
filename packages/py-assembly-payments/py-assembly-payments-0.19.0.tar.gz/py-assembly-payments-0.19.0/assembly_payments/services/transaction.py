
from assembly_payments.services.base import BaseService
from assembly_payments.types import Transaction, TransactionSupplementaryData


class TransactionService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "/transactions"

    def get(self, transaction_id):
        response = self._execute(
            TransactionService.GET, f"{self.endpoint}/{transaction_id}", url=self.beta_url
        )
        return Transaction(**response)

    def list(self):
        response = self._execute(TransactionService.GET, f"{self.endpoint}", url=self.beta_url)
        return list(map(lambda x: Transaction(**x), response.get("transactions", [])))

    def get_transaction_supplementary_data(self, transaction_id):
        response = self._execute(
            TransactionService.GET, f"{self.endpoint}/{transaction_id}/supplementary_data", url=self.beta_url
        )
        return TransactionSupplementaryData(**response)
