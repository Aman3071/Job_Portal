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

## 💻 How to Run the Project on Another Laptop

Follow these steps to set up and run the project on a new Windows computer.

### Prerequisites

- Python installed
- Visual Studio Code (recommended)
- Internet connection
- Gemini API key for the AI Resume Analyzer

### Step 1: Download the Project

1. Open the [Job Portal GitHub Repository](https://github.com/Aman3071/Job_Portal).
2. Click **Code → Download ZIP**.
3. Extract the downloaded ZIP file.
4. Open the extracted project folder in VS Code.

### Step 2: Open the Terminal

In VS Code, select **Terminal → New Terminal**.

Make sure the terminal is in the project root directory containing `manage.py`.

### Step 3: Create a Virtual Environment

```powershell
python -m venv env_jobportal
```

Activate it:

```powershell
.\env_jobportal\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

If `requirements.txt` exists, run:

```powershell
python -m pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own valid API key. Never upload your API key to GitHub.

### Step 6: Check the Django Project

```powershell
python manage.py check
```

### Step 7: Set Up the Database

```powershell
python manage.py migrate
```

Optionally, create an administrator account:

```powershell
python manage.py createsuperuser
```

### Step 8: Run the Application

```powershell
python manage.py runserver
```

Open the application:

- **Job Portal:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/

Press `Ctrl + C` in the terminal to stop the development server.

### Important Notes

- The local SQLite database and uploaded resumes are not included in the GitHub ZIP.
- Running migrations creates a fresh database; existing users, jobs, and applications will not automatically transfer.
- The AI Resume Analyzer requires a valid Gemini API key.
- If a Python package is missing, install it in the active virtual environment.
- This setup is intended for local development, not production deployment.
