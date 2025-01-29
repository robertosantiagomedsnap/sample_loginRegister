from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[("personal", "Personal"), ("company", "Company")],
        widget=forms.RadioSelect
    )

    # Fields for Personal Users
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    contact_number = forms.CharField(max_length=15, required=False)
    employee_specialty = forms.ChoiceField(
        choices=[
            ("general", "General"),
            ("aesthetic_medicine", "Aesthetic Medicine"),
            ("dermatologist", "Dermatologist"),
            ("plastic_surgery", "Plastic Surgery")
        ],
        required=False
    )
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female")], required=False)

    # Fields for Company Users
    company_name = forms.CharField(max_length=100, required=False)
    num_employees = forms.IntegerField(required=False)
    vat_number = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ["user_type", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        # Personal Users must have these fields
        if user_type == "personal":
            if not cleaned_data.get("first_name"):
                self.add_error("first_name", "First name is required for personal users.")
            if not cleaned_data.get("last_name"):
                self.add_error("last_name", "Last name is required for personal users.")

        # Company Users must have these fields
        if user_type == "company":
            if not cleaned_data.get("company_name"):
                self.add_error("company_name", "Company name is required.")
            if not cleaned_data.get("num_employees"):
                self.add_error("num_employees", "Number of employees is required.")
            if not cleaned_data.get("vat_number"):
                self.add_error("vat_number", "VAT Number is required.")
            if not cleaned_data.get("phone"):
                self.add_error("phone", "Phone is required.")
            if not cleaned_data.get("address"):
                self.add_error("address", "Address is required.")
            if not cleaned_data.get("country"):
                self.add_error("country", "Country is required.")

        return cleaned_data
