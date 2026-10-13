from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from jobs.forms import ResumeAnalysisForm


class ResumeAnalyzerTests(TestCase):

    def setUp(self):
        self.url = reverse("resume-analyzer")
        self.user = get_user_model().objects.create_user(
            username="testseeker",
            password="TestPass123!",
            role="seeker",
        )

    def test_analyzer_requires_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_open_analyzer(self):
        self.client.login(
            username="testseeker",
            password="TestPass123!",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI Resume Analyzer")


class ResumeAnalysisFormTests(SimpleTestCase):

    def test_valid_pdf_is_accepted(self):
        pdf = SimpleUploadedFile(
            "resume.pdf",
            b"%PDF-1.4\nSample resume content",
            content_type="application/pdf",
        )

        form = ResumeAnalysisForm(files={"resume": pdf})

        self.assertTrue(form.is_valid(), form.errors)

    def test_non_pdf_file_is_rejected(self):
        file = SimpleUploadedFile(
            "resume.txt",
            b"Sample resume content",
            content_type="text/plain",
        )

        form = ResumeAnalysisForm(files={"resume": file})

        self.assertFalse(form.is_valid())
        self.assertIn("resume", form.errors)

    def test_invalid_pdf_signature_is_rejected(self):
        file = SimpleUploadedFile(
            "resume.pdf",
            b"Not a PDF file",
            content_type="application/pdf",
        )

        form = ResumeAnalysisForm(files={"resume": file})

        self.assertFalse(form.is_valid())
        self.assertIn("resume", form.errors)

    def test_pdf_over_5mb_is_rejected(self):
        content = b"%PDF-" + (b"A" * (5 * 1024 * 1024))

        file = SimpleUploadedFile(
            "large_resume.pdf",
            content,
            content_type="application/pdf",
        )

        form = ResumeAnalysisForm(files={"resume": file})

        self.assertFalse(form.is_valid())
        self.assertIn("resume", form.errors)


class ResumeAnalyzerViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="viewtester",
            password="TestPass123!",
            role="seeker",
        )

        self.client.login(
            username="viewtester",
            password="TestPass123!",
        )

        self.url = reverse("resume-analyzer")

    def test_invalid_upload_does_not_call_ai_service(self):
        invalid_file = SimpleUploadedFile(
            "resume.txt",
            b"This is not a PDF",
            content_type="text/plain",
        )

        with patch("jobs.views.analyze_resume") as mock_analyze:
            response = self.client.post(
                self.url,
                {
                    "resume": invalid_file,
                    "job_description": "",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("resume", response.context["form"].errors)
        mock_analyze.assert_not_called()

    @patch(
        "jobs.views.analyze_resume",
        side_effect=Exception("Gemini unavailable"),
    )
    def test_ai_service_error_shows_friendly_message(self, mock_analyze):
        valid_pdf = SimpleUploadedFile(
            "resume.pdf",
            b"%PDF-1.4\nSample resume content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.url,
            {
                "resume": valid_pdf,
                "job_description": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "AI service is temporarily busy.",
        )
        mock_analyze.assert_called_once()
