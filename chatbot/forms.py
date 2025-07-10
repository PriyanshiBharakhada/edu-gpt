# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise forms.ValidationError("Passwords do not match")



from django import forms

class UploadPDFForm(forms.Form):
    pdf = forms.FileField(label="PDF File", allow_empty_file=False)

from django import forms


class UploadPDFForm(forms.Form):
    pdf = forms.FileField()
