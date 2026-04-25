from django.shortcuts import render, redirect
from .models import Customer, Loan, Document, EMI
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from datetime import date
from .utils import send_sms
from django.shortcuts import get_object_or_404
from .models import Document
from collections import defaultdict
from django.contrib import messages
from .utils import send_sms, send_emi_email
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Customer, Loan, EMI


# ---------------- REGISTER ----------------
def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        address = request.POST.get("address")
        age = request.POST.get("age")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password,
            address=address,   # ✅ added
            age=age            # ✅ added
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "customer/register.html")

# ---------------- LOGIN ----------------
def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            customer = Customer.objects.get(email=email, password=password)

            request.session["customer_id"] = customer.id
            request.session["customer_email"] = customer.email

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        except:
            return render(request, "customer/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "customer/login.html")


# ---------------- LOGOUT ----------------
def logout(request):

    if "customer_id" in request.session:
        del request.session["customer_id"]

    auth_logout(request)
    return redirect("login")

# Dashboard
def dashboard(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)

    loans = Loan.objects.filter(customer=customer).distinct()

    total_loans = loans.count()
    approved_loans = loans.filter(status="Approved").count()
    pending_loans = loans.filter(status="Pending").count()

    return render(request, "customer/dashboard.html", {
        "total_loans": total_loans,
        "approved_loans": approved_loans,
        "pending_loans": pending_loans,
    })


# Loan
def apply_loan(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    loans = Loan.objects.filter(customer_id=customer_id).order_by('-id')

    return render(request, "customer/apply_loan.html", {
        "loans": loans
    })


def loan_status(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    loans = Loan.objects.filter(customer_id=customer_id).order_by('-id')

    return render(request, "customer/loan_status.html", {
        "loans": loans
    })


# # Document
# def upload_document(request, loan_id):

#     customer_id = request.session.get("customer_id")

#     if not customer_id:
#         return redirect("login")

#     loan = Loan.objects.get(id=loan_id)

#     if request.method == "POST":

#         document_type = request.POST.get("document_type")
#         file = request.FILES.get("file")

#         Document.objects.create(
#             loan=loan,
#             document_type=document_type,
#             file=file
#         )

#         return redirect("documents")

#     return render(request, "customer/upload_document.html", {
#         "loan": loan
#     })


# EMI


# EMI TRACKING
def emi_tracking(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    loans = Loan.objects.filter(customer_id=customer_id)

    loan_data = []

    for loan in loans:

        emis = EMI.objects.filter(loan=loan).order_by("emi_number")

        # 🔥 NEXT EMI (first unpaid)
        next_emi = emis.filter(is_paid=False).first()

        loan_data.append({
            "loan": loan,
            "next_emi": next_emi
        })

    total_emis = EMI.objects.filter(loan__in=loans).count()
    paid_emis = EMI.objects.filter(loan__in=loans, is_paid=True).count()
    pending_emis = EMI.objects.filter(loan__in=loans, is_paid=False).count()

    return render(request, "customer/emi_tracking.html", {
        "loan_data": loan_data,
        "total_emis": total_emis,
        "paid_emis": paid_emis,
        "pending_emis": pending_emis
    })


# PAY EMI
def pay_emi(request, emi_id):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    emi = EMI.objects.get(id=emi_id)
    emi.is_paid = True
    emi.save()

    return redirect("emi_tracking")


def profile(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)

    loans = Loan.objects.filter(customer=customer)

    # 🔥 EMI FETCH
    emis = EMI.objects.filter(loan__in=loans)

    photo = Document.objects.filter(
        loan__in=loans,
        document_type="photo_doc"
    ).order_by('-id').first()

    return render(request, "customer/profile.html", {
        "customer": customer,
        "photo": photo,
        "emis": emis   
    })




def documents(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    documents = Document.objects.select_related(
        'loan', 'loan__customer'
    ).filter(
        loan__customer_id=customer_id   # ✅ IMPORTANT FILTER
    ).order_by('loan__id')

    grouped_documents = defaultdict(list)

    for doc in documents:
        key = doc.loan.id   # ✅ GROUP BY LOAN
        grouped_documents[key].append(doc)

    return render(request, "customer/documents.html", {
        "grouped_documents": dict(grouped_documents)
    })




def payment_page(request, emi_id):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    emi = EMI.objects.get(id=emi_id)

    return render(request, "customer/payment.html", {
        "emi": emi
    })


def process_payment(request, emi_id):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    emi = EMI.objects.get(id=emi_id)

    # ❌ Already paid check
    if emi.is_paid:
        from django.contrib import messages
        messages.warning(request, "EMI already paid")
        return redirect("emi_tracking")

    # 🔥 GET UPI ID
    upi_id = request.POST.get("upi_id")

    if not upi_id:
        from django.contrib import messages
        messages.error(request, "Please enter UPI ID")
        return redirect("payment_page", emi_id=emi.id)

    # 🔥 SIMULATE PAYMENT SUCCESS
    emi.is_paid = True
    emi.save()

    customer = emi.loan.customer

    # 📧 SEND EMAIL
    send_emi_email(customer.email, customer.name, emi)

    # 📱 SEND SMS
    message = f"EMI ₹{emi.amount} Paid via UPI ({upi_id})"

    send_sms(customer.phone, message)

    from django.contrib import messages
    messages.success(request, "✅ Payment Successful! Email Sent")

    return redirect("emi_tracking")





def check_emi_notifications():

    today = date.today()

    print("Today's Date:", today)   

    emis = EMI.objects.filter(
        due_date=today,
        is_paid=False
    )

    print("Total EMI Found:", emis.count())   

    if not emis:
        print("❌ No EMI due today")

    for emi in emis:

        customer = emi.loan.customer

        message = f"EMI ₹{emi.amount} due today"

        print("Sending SMS to:", customer.phone)  

        response = send_sms(customer.phone, message)

        print("API Response:", response)  






def delete_document(request, doc_id):

    if request.method == "POST":

        customer_id = request.session.get("customer_id")

        if not customer_id:
            return redirect("login")

        document = get_object_or_404(Document, id=doc_id)

        if document.loan.customer.id != customer_id:
            return redirect("documents")

        document.delete()

    return redirect("documents")



def emi_history(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)

    # 🔥 FETCH ONLY PAID EMIs
    emis = EMI.objects.filter(
        loan__customer=customer,
        is_paid=True
    ).select_related("loan").order_by("-id")

    return render(request, "customer/emi_history.html", {
        "emis": emis
    })






def download_emi_receipt(request, emi_id):

    emi = EMI.objects.get(id=emi_id)
    loan = emi.loan
    customer = loan.customer

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="EMI_{emi_id}_receipt.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    # 🔥 HEADER (LOGO + COMPANY NAME)
    logo_path = os.path.join(settings.BASE_DIR, "static/image/l7.png")

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=100, height=50)
        elements.append(logo)

    elements.append(Paragraph("<b>SMART FINANCE</b>", styles['Title']))
    elements.append(Paragraph("Loan & EMI Management System", styles['Normal']))
    elements.append(Spacer(1, 20))

    # 🔥 INVOICE INFO
    invoice_data = [
        ["Receipt No:", f"EMI-{emi.id}"],
        ["Date:", datetime.now().strftime("%d-%m-%Y")],
        ["Status:", "Paid"]
    ]

    invoice_table = Table(invoice_data, colWidths=[120, 200])
    invoice_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(invoice_table)
    elements.append(Spacer(1, 20))

    # 🔥 EMI DETAILS TABLE
    emi_data = [
        ["EMI No", "Amount", "Due Date", "Status"],
        [
            str(emi.emi_number),
            f"₹ {emi.amount:.2f}",
            str(emi.due_date),
            "Paid"
        ]
    ]

    emi_table = Table(emi_data, colWidths=[100, 100, 120, 100])
    emi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(Paragraph("<b>EMI DETAILS</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(emi_table)
    elements.append(Spacer(1, 20))

    # 🔥 CUSTOMER DETAILS
    customer_data = [
        ["Full Name", customer.name],
        ["Phone Number", customer.phone],
        ["Loan Type", loan.loan_type],
        ["Loan Amount", f"₹ {loan.amount:.2f}"],
        ["Interest Rate", f"{loan.interest_rate}%"],
        ["Bank Name", loan.bank],
        ["Account No.", f"XXXX{str(loan.id)[-4:]}"],
    ]

    customer_table = Table(customer_data, colWidths=[150, 250])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(Paragraph("<b>CUSTOMER & LOAN DETAILS</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(customer_table)
    elements.append(Spacer(1, 30))

    # 🔥 FOOTER
    elements.append(Paragraph("Thank you for your payment.", styles['Normal']))
    elements.append(Paragraph("<b>Smart Finance Team</b>", styles['Normal']))

    doc.build(elements)

    return response