from django.shortcuts import render,redirect
from httpcore import request
from admin_panel.models import LoanCategory, LoanPackage
from django.shortcuts import render, get_object_or_404
from admin_panel.models import LoanCategory, LoanPackage
import customer
from .models import ContactMessage
from customer.models import Document, Loan, Customer
from django.utils import timezone
from datetime import timedelta
from datetime import date, timedelta
from customer.models import EMI
from customer.models import Document



def index(request):

    packages = LoanPackage.objects.filter(is_active=True)

    for p in packages:
        p.feature_list = p.features.split(",")

    return render(
        request,
        "index.html",
        {
            "packages": packages
        }
    )

def required_documents(request):
     return render(request, "required_documents.html")

from admin_panel.models import LoanCategory

def loan_types(request):
    categories = LoanCategory.objects.prefetch_related("packages")
    return render(request, "loan_types.html", {
        "categories": categories
    })



def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def emi_calculator(request):
    return render(request, "emi_calculator.html")

def contact(request):
    return render(request, "contact.html")



def loan_app_form(request, pk):

    # 🔐 AUTH CHECK
    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect(f"/customer-panel/login/?next=/loan-app-form/{pk}/")

    package = get_object_or_404(
        LoanPackage.objects.select_related("category"),
        pk=pk,
        is_active=True
    )

    customer = Customer.objects.get(id=customer_id)

    # ---------------- POST ----------------
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        amount = float(request.POST.get("loan_amount"))
        tenure = int(request.POST.get("tenure"))
        bank = request.POST.get("bank")

        # 🔥 LOAN TYPE + INTEREST LOGIC
        loan_type = request.POST.get("loan_type")

        rate_map = {
            "personal": 5,
            "home": 7,
            "business": 10,
            "education": 6
        }

        interest_rate = rate_map.get(loan_type, 5)

        # ✅ CREATE LOAN
        loan = Loan.objects.create(
            customer=customer,
            full_name=full_name,
            email=email,
            loan_type=loan_type,
            amount=amount,
            tenure=tenure,
            bank=bank,
            mobile=mobile,
            interest_rate=interest_rate,
            status="Pending"
        )

        # 🔥 EMI CREATION
        total_months = tenure * 12
        monthly_emi = amount / total_months

        for i in range(1, total_months + 1):
            EMI.objects.create(
                loan=loan,
                emi_number=i,
                amount=monthly_emi,
                due_date=date.today() + timedelta(days=30 * i),
                is_paid=False
            )

        documents = [
            ("aadhaar_doc", "Aadhaar"),
            ("pan_doc", "PAN"),
            ("photo_doc", "photo_doc"),
            ("bank_doc", "Bank Statement"),
            ("salary_doc", "Salary Slip"),
            ("address_doc", "Address Proof"),
            ("income_doc", "Income Proof"),
            ("property_doc", "Property Document"),
            ("business_doc", "Business Proof"),
            ("sign_doc", "Signature"),
        ]

        for field_name, doc_type in documents:
            file = request.FILES.get(field_name)
            if file:
                Document.objects.create(
                    loan=loan,
                    document_type=doc_type,
                    file=file
                )

        return redirect("apply_loan")
    
    return render(request, "loan_app_form.html", {
        "package": package
    })



def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

    return render(request, "contact.html")






def loan_app_form(request, pk):

    package = get_object_or_404(
        LoanPackage.objects.select_related("category"),
        pk=pk,
        is_active=True
    )

    if request.method == "POST":

        customer_id = request.session.get("customer_id")

        if not customer_id:
            return redirect(f"/customer-panel/login/?next=/loan-app-form/{pk}/")

        customer = Customer.objects.get(id=customer_id)

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        amount = float(request.POST.get("loan_amount"))
        tenure = int(request.POST.get("tenure"))
        bank = request.POST.get("bank")

        # ✅ CREATE LOAN
        loan = Loan.objects.create(
            customer=customer,
            full_name=full_name,
            email=email,
            loan_type=package.title,
            amount=amount,
            tenure=tenure,
            bank=bank,
            mobile=mobile,
            interest_rate=package.interest_rate or 5,
            status="Pending"
        )

        # 🔥 EMI CREATION (MOST IMPORTANT)
        total_months = tenure * 12
        monthly_emi = amount / total_months

        for i in range(1, total_months + 1):
            EMI.objects.create(
                loan=loan,
                emi_number=i,
                amount=monthly_emi,
                due_date=date.today() + timedelta(days=30 * i),
                is_paid=False
            )

                # 🔥 SAVE DOCUMENTS
        documents = [
            ("aadhaar_doc", "Aadhaar"),
            ("pan_doc", "PAN"),
            ("photo_doc", "photo_doc"),
            ("bank_doc", "Bank Statement"),
            ("salary_doc", "Salary Slip"),
            ("address_doc", "Address Proof"),
            ("income_doc", "Income Proof"),
            ("property_doc", "Property Document"),
            ("business_doc", "Business Proof"),
            ("sign_doc", "Signature"),
        ]

        for field_name, doc_type in documents:
            file = request.FILES.get(field_name)

            if file:
                Document.objects.create(
                    loan=loan,
                    document_type=doc_type,
                    file=file
                )

        return redirect("apply_loan")

    return render(request, "loan_app_form.html", {
        "package": package
    })




def check_login_apply(request, pk):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect(f"/customer-panel/login/?next=/loan-app-form/{pk}/")

    return redirect(f"/loan-app-form/{pk}/")




