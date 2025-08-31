# Career Advisor Django Backend

A comprehensive Django REST API backend for the Career Advisor application that provides personality assessments, career recommendations, and educational guidance.

## Features

- **User Management**: Extended user model with career-specific fields
- **Assessment System**: Personality, interest, and aptitude assessments
- **Trait Analysis**: AI-powered personality trait scoring and analysis
- **Career Recommendations**: ML-based career matching using trait scores
- **Educational Guidance**: College and course recommendations
- **Career Roadmaps**: Step-by-step career development plans
- **AI Integration**: OpenAI GPT-4o for personalized insights

## Tech Stack

- **Django 5.2.5**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (can be changed to PostgreSQL/MySQL)
- **OpenAI API**: AI-powered insights and explanations
- **Django CORS Headers**: Cross-origin resource sharing

## Project Structure

```
career_advisor/
├── models.py          # Database models
├── serializers.py     # API serializers
├── views.py          # API views and logic
├── urls.py           # URL routing
├── admin.py          # Django admin configuration
├── signals.py        # Database signals
└── management/       # Custom management commands
    └── commands/
        └── populate_sample_data.py
```

## Setup Instructions

### 1. Environment Setup

```bash
# Activate your conda environment
conda activate sih_backend_py310

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

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

### 3. Database Setup

```bash
# Make and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_sample_data
```

### 4. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/users/` - User registration
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/update_profile/` - Update user profile

### Assessments
- `POST /api/assessments/start_assessment/` - Start new assessment
- `POST /api/assessments/{id}/submit_responses/` - Submit assessment responses
- `GET /api/assessments/` - List user assessments

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/for_assessment/` - Get questions for assessment type

### Career Recommendations
- `POST /api/recommendations/generate_career_recommendations/` - Generate recommendations
- `GET /api/recommendations/` - List user recommendations

### Data Models
- `GET /api/traits/` - List personality traits
- `GET /api/skills/` - List skills
- `GET /api/careers/` - List careers
- `GET /api/domains/` - List career domains
- `GET /api/colleges/` - List educational institutions
- `GET /api/courses/` - List courses
- `GET /api/roadmaps/` - List career roadmaps

## Assessment Flow

1. **Start Assessment**: User initiates assessment of specific type
2. **Answer Questions**: User responds to trait-based questions
3. **Calculate Scores**: System calculates weighted trait scores
4. **Generate Summary**: AI creates personalized assessment summary
5. **Career Matching**: ML algorithm matches traits to careers
6. **Recommendations**: Generate personalized career recommendations

## AI Integration

The system uses OpenAI's GPT-4o for:
- **Assessment Summaries**: Personalized feedback on assessment results
- **Career Explanations**: AI-generated reasoning for career matches
- **Personalized Insights**: Context-aware recommendations

## Sample Data

The `populate_sample_data` command creates:
- 10 personality traits
- 10 assessment questions
- 8 skills across technical and soft categories
- 5 interest categories
- 5 career domains
- 3 sample careers (Data Scientist, Software Engineer, Project Manager)
- 3 top universities
- Sample courses and roadmaps

## Development

### Adding New Models

1. Define model in `models.py`
2. Create serializer in `serializers.py`
3. Add viewset in `views.py`
4. Register in `urls.py`
5. Add to admin in `admin.py`
6. Create and run migrations

### Custom Management Commands

```bash
# Create new command
python manage.py startcommand command_name

# Run existing commands
python manage.py populate_sample_data
```

## Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test career_advisor
```

## Production Deployment

1. Set `DEBUG=False` in production
2. Use environment variables for sensitive data
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving
5. Configure CORS for production domains
6. Use HTTPS in production

## Contributing

1. Follow Django coding standards
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

## License

This project is part of the SIH Career Advisor application.
