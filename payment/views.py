from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import CampayService
from .models import Payment
from rest_framework.permissions import AllowAny
from rest_framework import status

@api_view(["POST"])
@permission_classes([AllowAny])
def initiate_payment(request):
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response({"error": "phone and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    service = CampayService()
    response = service.initiate_payment(
        amount=amount,
        phone=phone,
        description="Barbing appointment"
    )

    # If SDK returns error dict:
    if response.get("status") == "error":
        return Response(
            {"error": "CamPay error", "details": response},
            status=status.HTTP_400_BAD_REQUEST
        )

    # If no reference (unexpected):
    reference = response.get("reference")
    if not reference:
        return Response(
            {"error": "Missing reference in CamPay response", "details": response},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Save and respond
    payment = Payment.objects.create(
        reference=reference,
        phone=phone,
        amount=amount,
        status=response.get("status", "PENDING")
    )

    return Response({
        "message": "Payment initiated",
        "reference": reference,
        "campay_response": response
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
@permission_classes([AllowAny])
def check_payment_status(request, reference):
    service = CampayService()
    try:
        response = service.getStatus(reference)
        status = response.get("status")  # fixed typo

        payment = Payment.objects.get(reference=reference)  # fixed ORM query

        if status == "PENDING":
            payment.status = "PENDING"
        elif status == "SUCCESSFUL":
            payment.status = "SUCCESS"
        elif status == "FAILED":
            payment.status = "FAILED"

        payment.save()
        return Response({"status": payment.status})
        
        
    except Exception as e:
        return Response({"status": "error", "message": str(e)})