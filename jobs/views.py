import logging

import markdown
import nh3

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Job, Application, ResumeAnalysis
from .forms import JobForm, ResumeAnalysisForm
from .ai_services import (
    ResumePDFError,
    analyze_resume,
    generate_professional_resume,
    create_resume_pdf,
)

from pathlib import Path
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

MAX_RESUME_SIZE = 5 * 1024 * 1024


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
            try:
                queryset = queryset.filter(salary__gte=salary)
            except (ValueError, TypeError):
                pass

        return queryset


class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["already_applied"] = Application.objects.filter(
                job=self.object,
                applicant=self.request.user,
            ).exists()

            context["can_apply"] = getattr(self.request.user, "role", None) == "seeker"
        else:
            context["already_applied"] = False
            context["can_apply"] = False

        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and getattr(request.user, "role", None) != "employer"
        ):
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        job = self.get_object()

        if (
            getattr(request.user, "role", None) != "employer"
            or job.posted_by != request.user
        ):
            return redirect("job-detail", pk=job.pk)

        return super().dispatch(request, *args, **kwargs)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("job-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        job = self.get_object()

        if (
            getattr(request.user, "role", None) != "employer"
            or job.posted_by != request.user
        ):
            return redirect("job-detail", pk=job.pk)

        return super().dispatch(request, *args, **kwargs)


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if getattr(request.user, "role", None) != "seeker":
        return redirect("job-detail", pk=job.pk)

    already_applied = Application.objects.filter(
        job=job,
        applicant=request.user,
    ).exists()

    if already_applied:
        return redirect("job-detail", pk=job.pk)

    error = None

    if request.method == "POST":
        uploaded_resume = request.FILES.get("resume")

        if not uploaded_resume:
            error = "Please upload your resume in PDF format."

        elif not uploaded_resume.name.lower().endswith(".pdf"):
            error = "Only PDF resumes are allowed."

        elif uploaded_resume.size > MAX_RESUME_SIZE:
            error = "Resume size must not exceed 5 MB."

        else:
            signature = uploaded_resume.read(5)
            uploaded_resume.seek(0)

            if signature != b"%PDF-":
                error = "The uploaded file is not a valid PDF."

        if error is None:
            Application.objects.create(
                job=job,
                applicant=request.user,
                resume=uploaded_resume,
            )

            return redirect("job-detail", pk=job.pk)

    return render(
        request,
        "jobs/apply_job.html",
        {
            "job": job,
            "error": error,
        },
    )


class MyApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "jobs/my_application_list.html"
    context_object_name = "applications"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and getattr(request.user, "role", None) != "seeker"
        ):
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
        if (
            request.user.is_authenticated
            and getattr(request.user, "role", None) != "employer"
        ):
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


class JobApplicantsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "jobs/job_applicants_list.html"
    context_object_name = "applications"

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and getattr(request.user, "role", None) != "employer"
        ):
            return redirect("job-list")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        job = get_object_or_404(
            Job,
            pk=self.kwargs["pk"],
            posted_by=self.request.user,
        )

        return Application.objects.filter(job=job).select_related("applicant", "job")


@login_required
def update_application_status(request, pk):
    if getattr(request.user, "role", None) != "employer":
        return redirect("job-list")

    application = get_object_or_404(
        Application,
        pk=pk,
        job__posted_by=request.user,
    )

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["pending", "shortlisted", "rejected"]:
            application.status = status
            application.save(update_fields=["status"])

    return redirect("job-applicants", pk=application.job.pk)


@login_required
def resume_analyzer(request):
    analysis = None
    error = None
    resume_record = None

    if request.method == "POST":
        form = ResumeAnalysisForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_resume = form.cleaned_data["resume"]
            job_description = form.cleaned_data["job_description"]

            try:
                # Step 1: Analyze the uploaded resume.
                uploaded_resume.seek(0)

                raw_analysis = analyze_resume(
                    pdf_file=uploaded_resume,
                    job_description=job_description,
                )

                # Step 2: Save the original resume and analysis.
                uploaded_resume.seek(0)

                resume_record = ResumeAnalysis(
                    applicant=request.user,
                    job_description=job_description,
                    analysis_result=raw_analysis,
                )

                resume_record.original_resume.save(
                    uploaded_resume.name,
                    uploaded_resume,
                    save=False,
                )
                resume_record.save()

                # Step 3: Generate the professional PDF.
                try:
                    uploaded_resume.seek(0)

                    generated_content = generate_professional_resume(
                        pdf_file=uploaded_resume,
                        job_description=job_description,
                    )

                    pdf_bytes = create_resume_pdf(generated_content)

                    resume_record.generated_resume.save(
                        "generated_resume.pdf",
                        ContentFile(pdf_bytes),
                        save=True,
                    )

                except Exception:
                    logger.exception(
                        "Resume PDF generation failed for analysis %s",
                        resume_record.pk,
                    )
                    error = (
                        "Your analysis was saved, but the generated PDF "
                        "could not be created. Please try again."
                    )

                # Step 4: Format the analysis safely.
                analysis_html = markdown.markdown(
                    raw_analysis,
                    extensions=["extra", "nl2br"],
                )

                analysis = nh3.clean(
                    analysis_html,
                    tags={
                        "p",
                        "br",
                        "strong",
                        "em",
                        "ul",
                        "ol",
                        "li",
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "blockquote",
                        "code",
                        "pre",
                        "hr",
                    },
                )

                # Clear the form only after the PDF is generated successfully.
                if resume_record.generated_resume:
                    form = ResumeAnalysisForm()

            except ResumePDFError as exc:
                error = str(exc)

            except Exception:
                logger.exception("Resume analyzer failed")
                error = (
                    "AI service is temporarily busy. " "Please try again in a minute."
                )

    else:
        form = ResumeAnalysisForm()

    # Show the current user's five most recent analyses.
    saved_analyses = list(
        ResumeAnalysis.objects.filter(applicant=request.user).order_by("-created_at")[
            :5
        ]
    )

    # Prepare readable filenames for the listing.
    for saved in saved_analyses:
        saved.display_filename = (
            Path(saved.original_resume.name).name
            if saved.original_resume
            else f"Resume Analysis #{saved.pk}"
        )

    return render(
        request,
        "jobs/resume_analyzer.html",
        {
            "form": form,
            "analysis": analysis,
            "error": error,
            "resume_record": resume_record,
            "saved_analyses": saved_analyses,
        },
    )
