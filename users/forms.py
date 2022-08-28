from django import forms

class SignupForm(forms.Form):
    firstName = forms.CharField(label='Your first name', max_length=100)
    email = forms.CharField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)