from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import CampayService
from .models import Payment
from clients.models import Booking
from catalog.models import Hairstyle
from rest_framework.permissions import AllowAny
from rest_framework import status
import secrets
import string


@api_view(["POST"])
@permission_classes([AllowAny])
def initiate_payment(request):
    #PAYMENT INFO
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    #BOOKING INFO
    bearer = request.data.get("name")
    hairstyle = request.data.get("hairstyle")
    # scheduled_date = request.data.get("date")
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


    #GENERATE TICKET NUMBER AND SAVE APPOINTMENT
    def get_ticket_number():
        alphabet = string.digits + string.ascii_uppercase
        random_part = ''.join(secrets.choice(alphabet) for _ in range(5))
        return f"YM-{random_part}"
    
    booking = Booking.objects.create(
        bearer=bearer,
        hairstyle=Hairstyle.objects.get(public_id=hairstyle),
        # scheduled_date=scheduled_date,
        ticket_number=get_ticket_number()
    )

    # Save and respond
    payment = Payment.objects.create(
        reference=reference,
        phone=phone,
        amount=amount,
        booking=booking,
        status=response.get("status", "PENDING")
    )

    return Response({
        "message": "Payment initiated",
        "reference": reference,
        "campay_response": response,
        "appointment": str(booking)

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
        response = service.get_status(reference)
        status = response.get("status")  # fixed typo

        payment = Payment.objects.get(reference=reference)  # fixed ORM query

        if status == "PENDING":
            payment.status = "PENDING"
            return Response({"status": payment.status})
        elif status == "SUCCESSFUL":
            payment.status = "SUCCESS"
            payment.save()
            return Response({"status": payment.status})
        elif status == "FAILED":
            payment.status = "FAILED"
            return Response({"status": payment.status})
            
    except Exception as e:
        return Response({"status": "error", "message": str(e)})