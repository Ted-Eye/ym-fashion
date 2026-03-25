from campay.sdk import Client as campayClient
from django.conf import settings


class CampayService:
    def __init__(self):
        self.client = campayClient(
            username=settings.CAMPAY_USERNAME, password=settings.CAMPAY_PASSWORD, mode=settings.CAMPAY_MODE
        )
    def initiatePayment(self, amount, phone, description):
        try:
            return self.client.collect({
            "amount": str(amount), "currency": "XAF", "from": phone, "description": description
        })
        except Exception as e:
            return {"status": "error", "message": str(e)}
    def getStatus(self, reference):
        try:
            return self.client.get_transaction_status(reference)
        except Exception as e:
            return {"status": "error", "message": str(e)}