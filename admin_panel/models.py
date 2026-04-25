from django.db import models


class LoanHead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LoanCategory(models.Model):
    loan_head = models.ForeignKey(
    LoanHead,
    on_delete=models.CASCADE,
    related_name="categories",
    null=True,
    blank=True
)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LoanPackage(models.Model):

    category = models.ForeignKey(
        LoanCategory,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    title = models.CharField(max_length=200)

    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    min_amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField()

    tenure_years = models.PositiveIntegerField()

    features = models.TextField(help_text="Comma separated values")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name