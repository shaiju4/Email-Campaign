from django import forms
from django.core.exceptions import ValidationError

class RecipientForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV or Excel file",
    )

    def clean_file(self):
        """
        Validate that the uploaded file is either a CSV or Excel file.
        """
        uploaded_file = self.cleaned_data["file"]
        allowed_extensions = (".csv", ".xls", ".xlsx")

        if not uploaded_file.name.lower().endswith(allowed_extensions):
            raise ValidationError("Only CSV or Excel files are allowed.")

        return uploaded_file
