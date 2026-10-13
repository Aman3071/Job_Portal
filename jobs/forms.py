from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company_name", "description", "location", "salary"]


class ResumeAnalysisForm(forms.Form):
    resume = forms.FileField(
        label="Upload Resume (PDF)", help_text="Upload a text-based PDF, maximum 5 MB."
    )

    job_description = forms.CharField(
        label="Job Description (Optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Paste the job description to check your resume match...",
            }
        ),
    )

    def clean_resume(self):
        resume = self.cleaned_data["resume"]

        # Maximum file size: 5 MB
        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Resume size must be 5 MB or less.")

        # Check PDF extension
        if not resume.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Only PDF files are allowed.")

        # Check PDF signature
        if resume.read(5) != b"%PDF-":
            raise forms.ValidationError("The uploaded file is not a valid PDF.")

        resume.seek(0)
        return resume
