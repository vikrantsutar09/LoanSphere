from django import forms
from .models import Customer, Loan, Document

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_type', 'amount', 'tenure']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']
