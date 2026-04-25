from django.db import models

# ----------------------------
# CUSTOMER MODEL
# ----------------------------
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# LOAN MODEL
# ----------------------------
class Loan(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # 🔥 ADD THIS
    loan_head = models.ForeignKey(
        "admin_panel.LoanHead",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    loan_type = models.CharField(max_length=50)
    amount = models.FloatField()
    tenure = models.IntegerField()

    bank = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    interest_rate = models.FloatField(default=10)

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.status}"


# ----------------------------
# DOCUMENT MODEL
# ----------------------------
class Document(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')  # ✅ required

    uploaded_at = models.DateTimeField(auto_now_add=True)


# ----------------------------
# EMI MODEL
# ----------------------------
class EMI(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    emi_number = models.IntegerField()
    amount = models.FloatField()
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"EMI {self.emi_number}"



