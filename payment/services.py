from campay.sdk import Client as campayClient
from django.conf import settings


class CampayService:
    def __init__(self):
        self.client = campayClient(
            username=settings.CAMPAY_USERNAME,
            password=settings.CAMPAY_PASSWORD,
            mode=settings.CAMPAY_MODE
        )

    def initiate_payment(self, amount, phone, description):
        """
        Calls CamPay SDK and returns a dict.
        The SDK returns a dict on success.
        On exception, we wrap the exception into a dict.
        """
        try:
            result = self.client.collect({
                "amount": str(amount),
                "currency": "XAF",
                "from": phone,
                "description": description,
                "external_reference": ""  # optional if needed
            })

            # Ensure result is a dict
            if isinstance(result, dict):
                return result
            return {"status": "error", "message": "Unexpected non-dict response"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_status(self, reference):
        try:
            return self.client.get_transaction_status(reference)
        except Exception as e:
            return {"status": "error", "message": str(e)}