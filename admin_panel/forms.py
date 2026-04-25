from django import forms
from .models import LoanHead, LoanCategory, LoanPackage



class LoanHeadForm(forms.ModelForm):
    class Meta:
        model = LoanHead
        fields = ['name', 'email', 'phone', 'password']


class LoanCategoryForm(forms.ModelForm):

    class Meta:
        model = LoanCategory
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter category name"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control description-box",
                "rows": 5,
                "placeholder": "Write category description here..."
            }),
        }


class LoanPackageForm(forms.ModelForm):
    class Meta:
        model = LoanPackage
        fields = "__all__"
