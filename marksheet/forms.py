# marksheet/forms.py
from django import forms
from .models import Class
from captcha.fields import CaptchaField

class MarksheetForm(forms.Form):
    roll_number = forms.CharField(max_length=15, label="Enter Roll Number")
    student_class = forms.ModelChoiceField(queryset=Class.objects.all(), label="Select Class")
    captcha = CaptchaField()  # Add CAPTCHA field
