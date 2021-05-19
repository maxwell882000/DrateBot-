from django import forms


class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    company = forms.CharField(required=False)
    department = forms.CharField(required=False)
    is_manager = forms.BooleanField(initial=False, required=False)
