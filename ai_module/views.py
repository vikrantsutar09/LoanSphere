from rest_framework.decorators import api_view
from rest_framework.response import Response
import math


@api_view(['POST'])
def chatbot_api(request):

    user_message = request.data.get("message", "").lower()

    if user_message in ["hi", "hello", "hii"]:
        bot_reply = "Hello 👋 Welcome to Smart Finance Loan. How can I assist you?"

    elif "loan" in user_message:
        bot_reply = "We offer Personal, Home and Business Loans."

    elif "interest" in user_message:
        bot_reply = "Interest rates start from 8.5% per annum."

    elif "emi" in user_message:
        try:
            parts = user_message.split()
            principal = float(parts[1])
            rate = float(parts[2]) / 100 / 12
            time = float(parts[3]) * 12

            emi = (principal * rate * pow(1 + rate, time)) / (pow(1 + rate, time) - 1)
            bot_reply = f"Your EMI is ₹{round(emi,2)} per month."

        except:
            bot_reply = "To calculate EMI type: emi loan_amount interest_rate years"

    else:
        bot_reply = "Sorry, I didn't understand. Ask about loan, interest, or EMI."

    return Response({
        "user_message": user_message,
        "bot_response": bot_reply,
        "status": "success"
    })
