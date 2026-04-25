from django.contrib import admin
from .models import LoanHead, LoanCategory, LoanPackage


@admin.register(LoanHead)
class LoanHeadAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(LoanCategory)
class LoanCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "loan_head", "created_at")
    list_filter = ("loan_head",)


@admin.register(LoanPackage)
class LoanPackageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "interest_rate",
        "tenure_years",
        "is_active",
    )

    list_filter = ("category", "is_active")

    search_fields = ("title",)
