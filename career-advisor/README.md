
# 🎓 SIH Career & Education Advisor (MVP)

An AI-powered **Career and Education Advisor** built for **Smart India Hackathon (SIH)**.  
It helps students explore careers based on their **personality traits, skills, interests, and education level**, with tailored **career paths, study plans, and AI-powered insights**.

---

## ⚡ Features

- 🧠 **Comprehensive Assessment System** (Personality, Interest, Aptitude)
- 🤖 **AI-Powered Insights** (OpenAI GPT-4o integration)
- 🎯 **Smart Career Matching** (ML-based trait analysis + similarity scoring)
- 📚 **Educational Guidance** (Colleges, Courses, Roadmaps)
- 🌐 **Full-Stack App** (Django REST API + React frontend)
- 📊 **Interactive Dashboard** with detailed career recommendations
- 🈳 **Multilingual-Ready** (English, Hindi, Kashmiri)
- 📂 **Extensible Architecture** (supports 1500+ careers)

---

## 🏗 Project Structure

```
career-advisor/
├── backend/                    # Django REST API backend
│   ├── career_advisor/        # Main Django app
│   │   ├── models.py         # Database models (Users, Assessments, Careers, etc.)
│   │   ├── views.py          # API endpoints and business logic
│   │   ├── serializers.py    # Data serialization
│   │   ├── admin.py          # Django admin interface
│   │   └── management/       # Custom commands
│   ├── career_advisor_backend/ # Django project settings
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend documentation
│
├── frontend/                  # React + Vite frontend
│   ├── src/
│   │   ├── components/       # Quiz + Dashboard UI
│   │   ├── services/         # API service layer
│   │   └── App.jsx          # Main application
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
│
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ with conda environment `sih_backend_py310`
- Node.js 16+ and npm
- OpenAI API key (for AI-powered insights)

### 1. Backend Setup (Django)

```bash
cd backend

# Activate conda environment
conda activate sih_backend_py310

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_sample_data

# Start Django server
python manage.py runserver
```

**Backend will be available at:** `http://localhost:8000/`

### 2. Frontend Setup (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:5173/`

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=sqlite:///db.sqlite3
```

### API Endpoints

The Django backend provides comprehensive REST API endpoints:

- **Authentication**: `/api/users/`
- **Assessments**: `/api/assessments/`
- **Questions**: `/api/questions/`
- **Career Recommendations**: `/api/recommendations/`
- **Data Models**: `/api/traits/`, `/api/skills/`, `/api/careers/`, etc.

---

## 🧠 Assessment Flow

1. **User Profile**: Collect basic information and preferences
2. **Assessment Start**: Initialize assessment session
3. **Question Flow**: Present trait-based questions with progress tracking
4. **Response Processing**: Calculate weighted trait scores
5. **AI Analysis**: Generate personalized insights using OpenAI
6. **Career Matching**: ML algorithm matches traits to careers
7. **Recommendations**: Generate comprehensive career guidance

---

## 🎯 Key Components

### Backend Models
- **Users**: Extended user model with career-specific fields
- **Assessments**: Assessment sessions and responses
- **Traits**: Personality and career traits
- **Careers**: Career paths with skill requirements
- **Colleges & Courses**: Educational opportunities
- **Roadmaps**: Step-by-step career development plans

### Frontend Components
- **Quiz**: Interactive assessment interface
- **Dashboard**: Comprehensive results and recommendations
- **API Service**: Backend communication layer

---

## 🤖 AI Integration

- **OpenAI GPT-4o**: Personalized assessment summaries and career explanations
- **ML Scoring**: Career compatibility ranking and user segmentation
- **Hybrid Approach**: Combines AI insights with structured data for explainable recommendations

---

## 📊 Sample Data

The system comes pre-populated with:
- 10+ personality traits
- 10+ assessment questions
- 8+ skills (technical & soft)
- 5+ career domains
- 3+ sample careers
- Top universities and courses
- Career development roadmaps

---

## 🔮 Future Enhancements

- **WhatsApp Bot Integration**: Expose API endpoints for messaging platforms
- **Advanced ML Models**: Enhanced career matching algorithms
- **Multilingual Support**: Hindi, Kashmiri, and other languages
- **Mobile App**: React Native or Flutter implementation
- **Analytics Dashboard**: User behavior and recommendation insights

---

## 🛠 Development

### Adding New Features

1. **Backend**: Define models, create serializers, add views, update URLs
2. **Frontend**: Create components, update API service, integrate with UI
3. **Testing**: Run Django tests and frontend validation

### Custom Commands

```bash
# Create new Django management command
python manage.py startcommand command_name

# Populate sample data
python manage.py populate_sample_data
```

---

## 🚀 Production Deployment

1. Set `DEBUG=False` in production
2. Use environment variables for sensitive data
3. Configure production database (PostgreSQL recommended)
4. Set up static file serving
5. Configure CORS for production domains
6. Use HTTPS in production

---

## 📝 API Documentation

### Assessment Flow

```bash
# Start assessment
POST /api/assessments/start_assessment/
{
  "assessment_type": "comprehensive"
}

# Submit responses
POST /api/assessments/{id}/submit_responses/
{
  "assessment_id": "uuid",
  "responses": [
    {
      "question_id": "uuid",
      "response": "Agree",
      "response_time": 5
    }
  ]
}

# Generate recommendations
POST /api/recommendations/generate_career_recommendations/
{
  "assessment_id": "uuid",
  "include_courses": true,
  "include_roadmaps": true,
  "max_recommendations": 5
}
```

---

## 🤝 Contributing

1. Follow Django and React coding standards
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

---

## 📄 License

This project is part of the SIH Career Advisor application.

---

## 🆘 Support

For technical support or questions:
1. Check the backend and frontend README files
2. Review API documentation
3. Check Django admin interface for data validation
4. Verify OpenAI API key configuration

---

**Built with ❤️ for SIH 2025**
