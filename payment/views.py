from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import CampayService
from .models import Payment
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes([AllowAny])
def initiate_payment(request):
    try:
        phone = request.data.get("phone")
        amount = request.data.get("amount")
        service = CampayService()
        response = service.initiatePayment(
            amount=amount, phone=phone, description='Barbing appointment'
        )
    # TEMP DEBUG
        return Response({
        "debug_response": str(response)
    })
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)


    
    # reference = response.get("reference") if isinstance(response, dict) else None

    # if not response:
    #     return Response({
    #         "error": "payment initiation failed",
    #         "details": str(response)
    #     }, status=400)

    # payment = Payment.objects.create(
    #     reference=reference, phone=phone, amount=amount, status="PENDING"
    # )
    # return Response({
    #     "message": "Payment initiated", "reference": reference
    # })

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
