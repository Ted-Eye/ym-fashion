from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import CampayService
from .models import Payment
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes([AllowAny])
def initiate_payment(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response({"error": "phone and amount are required"}, status=400)

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return Response({"error": "Invalid amount"}, status=400)

    service = CampayService()

    try:
        response = service.initiatePayment(
            amount=amount,
            phone=phone,
            description='Barbing appointment'
        )
    except Exception as e:
        return Response(
            {"error": "Payment service error", "details": str(e)},
            status=500
        )

    if not response or "reference" not in response:
        return Response(
            {"error": "Payment initiation failed", "details": response},
            status=400
        )

    reference = response.get("reference")
    status = response.get("status", "PENDING")

    payment = Payment.objects.create(
        reference=reference,
        phone=phone,
        amount=amount,
        status=status
    )

    return Response({
        "message": "Payment initiated",
        "reference": reference
    })

    # except Exception as e:
    #     return Response({
    #         "error": str(e)
    #     }, status=500)


    
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
