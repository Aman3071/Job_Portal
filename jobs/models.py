from django.db import models
from django.conf import settings


class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_posted = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    resume = models.FileField(
        upload_to="resumes/applications/",
        blank=True,
        default="",
    )
    date_applied = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    class Meta:
        unique_together = ["job", "applicant"]

    def __str__(self):
        return f"{self.applicant} applied to {self.job}"


class ResumeAnalysis(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume_analyses",
    )
    original_resume = models.FileField(
        upload_to="resumes/original/",
    )
    job_description = models.TextField(blank=True)
    analysis_result = models.TextField(blank=True)
    generated_resume = models.FileField(
        upload_to="resumes/generated/",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Resume analysis - {self.applicant}"
