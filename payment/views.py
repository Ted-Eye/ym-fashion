from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import CampayService
from .models import Payment


@api_view(["POST"])
def initiate_payment(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")
    service = CampayService()
    response = service.initiatePayment(
        amount=amount, phone=phone, description='Barbing appointment'
    )
    reference = response.get("reference")

    payment = Payment.objects.create(
        reference=reference, phone=phone, amount=amount, status="PENDING"
    )
    return Response({
        "message": "Payment initiated", "reference": reference
    })

@api_view(["GET"])
def check_payment_status(request, reference):
    service = CampayService()
    response = service.getStatus(reference)
    status = response.get("satus")
    paymet = Payment.objects.get(reference==reference)
    if status == "SUCCESSFUL":
        paymet.status == "SUCCESS"
    elif status == "FAILED":
        paymet.status == "FAILED"

    paymet.save()

    return Response({
        "status": paymet.status
    })
