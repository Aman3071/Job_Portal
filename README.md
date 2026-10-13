# 🚀 AI-Powered Job Portal

A full-stack **Job Portal Web Application** built with Django that connects job seekers and employers. The platform includes job listings, job applications, employer job management, and an **AI-powered Resume Analyzer** to help candidates evaluate their resumes against job descriptions.

## ✨ Features

### 👤 User Authentication

- User registration and login
- Role-based access for job seekers and employers
- Secure access to role-specific features

### 💼 Job Management

- Browse available job listings
- View job details
- Employers can post and manage jobs
- View applicants for posted jobs

### 📄 Job Applications

- Apply for jobs
- Upload resumes with job applications
- Track application status
- Employers can review applications and manage applicant status

### 🤖 AI Resume Analyzer

- Upload a resume in PDF format
- Compare resume content against a job description
- Get AI-generated resume feedback and improvement suggestions
- Identify relevant skills and potential areas for improvement

### 🎨 User Interface

- Django Templates-based frontend
- HTML, CSS, and JavaScript
- Responsive styling and navigation

## 🛠️ Tech Stack

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Backend programming        |
| Django       | Web framework              |
| SQLite       | Database                   |
| HTML5        | Page structure             |
| CSS3         | Styling and layout         |
| JavaScript   | Frontend interactions      |
| Gemini API   | AI-powered resume analysis |
| Git & GitHub | Version control            |

## 📂 Project Structure

```text
Job_Portal/
├── accounts/
├── jobs/
│   ├── migrations/
│   ├── templates/
│   │   └── jobs/
│   ├── ai_services.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── jobportal/
│   ├── settings.py
│   ├── urls.py
│   └── static/
│       └── css/
├── templates/
│   └── base.html
├── manage.py
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone git@github.com:Aman3071/Job_Portal.git
cd Job_Portal
```

Alternatively, clone using HTTPS:

```bash
git clone https://github.com/Aman3071/Job_Portal.git
cd Job_Portal
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv env_jobportal
.\env_jobportal\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the packages required by the project. If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If not, install the project's dependencies based on the imports in your code, including Django, `google-genai`, `python-dotenv`, `pypdf`, and `nh3` where required.

### 4. Configure environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. **Never commit your `.env` file or expose your API key publicly.**

Ensure your Django settings or AI service reads the same environment variable name.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

`http://127.0.0.1:8000/`

## 🔐 Security Notes

- Keep API keys and credentials in environment variables.
- Do not commit `.env`, local databases, uploaded resumes, or generated files.
- Resume analysis requires a valid Gemini API configuration and available API quota.
- Use a production-ready database, secure settings, and appropriate file validation before deployment.

## 🚧 Future Improvements

- Advanced job search and filtering
- Email notifications for application updates
- Employer and candidate dashboards
- Resume scoring and skill matching
- Cloud deployment and production database integration

## 👨‍💻 Author

**Aman Tinmekar**

- GitHub: [Aman3071](https://github.com/Aman3071)

---
