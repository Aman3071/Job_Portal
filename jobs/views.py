from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Job, Application
from .forms import JobForm


# Show all available jobs
class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "all_jobs"

    def get_queryset(self):
        queryset = Job.objects.all()

        title = self.request.GET.get("title")
        location = self.request.GET.get("location")
        salary = self.request.GET.get("salary")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if salary:
            queryset = queryset.filter(salary__gte=salary)

        return queryset


# Show details of a single job
class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["already_applied"] = Application.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()

            context["can_apply"] = self.request.user.role == "seeker"

        else:
            context["already_applied"] = False
            context["can_apply"] = False

        return context


# Create a new job
class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != "employer":
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


# Update an existing job
class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()

        if request.user.role != "employer" or job.posted_by != request.user:
            return redirect("job-detail", pk=job.pk)

        return super().dispatch(request, *args, **kwargs)


# Delete an existing job
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()

        if request.user.role != "employer" or job.posted_by != request.user:
            return redirect("job-detail", pk=job.pk)

        return super().dispatch(request, *args, **kwargs)


# Apply for a job
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.role != "seeker":
        return redirect("job-detail", pk=job.pk)

    already_applied = Application.objects.filter(
        job=job, applicant=request.user
    ).exists()

    if not already_applied:
        Application.objects.create(job=job, applicant=request.user)

    return redirect("job-detail", pk=job.pk)


class MyApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "jobs/my_application_list.html"
    context_object_name = "applications"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "seeker":
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related(
            "job"
        )


class MyJobsListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/my_jobs_list.html"
    context_object_name = "jobs"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "employer":
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


class JobApplicantsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "jobs/job_applicants_list.html"
    context_object_name = "applications"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "employer":
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs["pk"], posted_by=self.request.user)

        return Application.objects.filter(job=job).select_related("applicant", "job")


@login_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk, job__posted_by=request.user)

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["pending", "shortlisted", "rejected"]:
            application.status = status
            application.save()

    return redirect("job-applicants", pk=application.job.pk)
