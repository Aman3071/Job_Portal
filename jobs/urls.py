from django.urls import path

from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    apply_job,
    MyApplicationListView,
    MyJobsListView,
    JobApplicantsListView,
    update_application_status,
)

urlpatterns = [
    # Job list
    path("", JobListView.as_view(), name="job-list"),
    # Job detail
    path("job/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    # Create new job
    path("job/create/", JobCreateView.as_view(), name="job-create"),
    # Update existing job
    path("job/<int:pk>/update/", JobUpdateView.as_view(), name="job-update"),
    # Delete existing job
    path("job/<int:pk>/delete/", JobDeleteView.as_view(), name="job-delete"),
    # Apply for a job
    path("job/<int:pk>/apply/", apply_job, name="apply-job"),
    path("my-applications/", MyApplicationListView.as_view(), name="my-applications"),
    path("my-jobs/", MyJobsListView.as_view(), name="my-jobs"),
    path(
        "job/<int:pk>/applicants/",
        JobApplicantsListView.as_view(),
        name="job-applicants",
    ),
    path(
        "application/<int:pk>/status/",
        update_application_status,
        name="update-application-status",
    ),
]
