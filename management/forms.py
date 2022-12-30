from django import forms 

class SignIn(forms.Form):
    Email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)