from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class User(AbstractUser):
    """Extended user model with career advisor specific fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    education_level = models.CharField(max_length=100, choices=[
        ('high_school', 'High School'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certification', 'Certification'),
        ('other', 'Other')
    ])
    location = models.CharField(max_length=200, blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Trait(models.Model):
    """Master table of personality and career traits"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('personality', 'Personality'),
        ('cognitive', 'Cognitive'),
        ('social', 'Social'),
        ('leadership', 'Leadership'),
        ('technical', 'Technical'),
        ('creative', 'Creative'),
        ('analytical', 'Analytical')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'traits'

    def __str__(self):
        return self.name

class Question(models.Model):
    """Question bank for assessments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[
        ('likert', 'Likert Scale'),
        ('single_choice', 'Single Choice'),
        ('multi_select', 'Multi Select'),
        ('text_input', 'Text Input')
    ])
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE, related_name='questions')
    weight = models.FloatField(default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    options = models.JSONField(default=list, blank=True)  # For multiple choice questions
    group = models.IntegerField(choices=[(i, f'Group {i}') for i in range(1, 7)], help_text='Question group (1-6)', default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return f"{self.question_type}: {self.text[:50]}..."

class Assessment(models.Model):
    """Assessment sessions for users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.CharField(max_length=50, choices=[
        ('personality', 'Personality'),
        ('interest', 'Interest'),
        ('aptitude', 'Aptitude'),
        ('comprehensive', 'Comprehensive')
    ])
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned')
    ], default='in_progress')
    overall_score = models.FloatField(null=True, blank=True)
    summary = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'assessments'

    def __str__(self):
        return f"{self.user.username} - {self.assessment_type} ({self.status})"

class Response(models.Model):
    """User responses to assessment questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    raw_response = models.TextField()
    weighted_score = models.FloatField()
    response_time = models.IntegerField(help_text="Response time in seconds", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'responses'
        unique_together = ['assessment', 'question']

class AssessmentTrait(models.Model):
    """Aggregated trait scores for each assessment"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='trait_scores')
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE, related_name='assessment_scores')
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    percentile = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assessment_traits'
        unique_together = ['assessment', 'trait']

class Skill(models.Model):
    """Skills that can be mapped to careers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('domain', 'Domain Knowledge'),
        ('tool', 'Tools & Technologies')
    ])
    proficiency_levels = models.JSONField(default=list)  # ['Beginner', 'Intermediate', 'Advanced']
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name

class Interest(models.Model):
    """User interests and hobbies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('creative', 'Creative'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('social', 'Social')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interests'

    def __str__(self):
        return self.name

class Domain(models.Model):
    """Career domains and industries"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    growth_potential = models.CharField(max_length=20, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ])
    salary_range = models.JSONField(default=dict)  # {'entry': 50000, 'mid': 80000, 'senior': 120000}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.name

class Career(models.Model):
    """Career paths and job titles"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='careers')
    required_skills = models.ManyToManyField(Skill, related_name='careers')
    preferred_traits = models.ManyToManyField(Trait, related_name='careers')
    education_requirements = models.JSONField(default=list)
    experience_levels = models.JSONField(default=list)
    salary_range = models.JSONField(default=dict)
    job_outlook = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'careers'

    def __str__(self):
        return self.title

class CareerSkillMap(models.Model):
    """Mapping between careers and skills with importance levels"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='skill_mappings')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='career_mappings')
    importance_level = models.CharField(max_length=20, choices=[
        ('critical', 'Critical'),
        ('important', 'Important'),
        ('preferred', 'Preferred'),
        ('optional', 'Optional')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'career_skill_maps'
        unique_together = ['career', 'skill']

class College(models.Model):
    """Educational institutions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('university', 'University'),
        ('college', 'College'),
        ('institute', 'Institute'),
        ('polytechnic', 'Polytechnic')
    ])
    ranking = models.IntegerField(null=True, blank=True)
    acceptance_rate = models.FloatField(null=True, blank=True)
    tuition_fees = models.JSONField(default=dict)
    programs = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'colleges'

    def __str__(self):
        return self.name

class Course(models.Model):
    """Educational courses and programs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    duration = models.CharField(max_length=50)
    level = models.CharField(max_length=50, choices=[
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD')
    ])
    skills_covered = models.ManyToManyField(Skill, related_name='courses')
    career_paths = models.ManyToManyField(Career, related_name='courses')
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return f"{self.name} - {self.college.name}"

class Roadmap(models.Model):
    """Career development roadmaps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='roadmaps')
    target_audience = models.CharField(max_length=100)
    duration_months = models.IntegerField()
    steps = models.JSONField(default=list)  # List of roadmap steps
    prerequisites = models.ManyToManyField(Skill, related_name='roadmap_prerequisites')
    outcomes = models.JSONField(default=list)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roadmaps'

    def __str__(self):
        return f"{self.title} - {self.career.title}"

class Recommendation(models.Model):
    """Career recommendations for users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='recommendations')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='recommendations')
    match_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    reasoning = models.TextField()
    confidence_level = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    skill_gaps = models.ManyToManyField(Skill, related_name='recommendation_gaps')
    suggested_courses = models.ManyToManyField(Course, related_name='recommendations')
    suggested_roadmaps = models.ManyToManyField(Roadmap, related_name='recommendations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommendations'
        unique_together = ['user', 'assessment', 'career']

    def __str__(self):
        return f"{self.user.username} - {self.career.title} ({self.match_score}%)"

class UserSkill(models.Model):
    """User's skills and proficiency levels"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='users')
    proficiency_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ])
    years_of_experience = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_skills'
        unique_together = ['user', 'skill']

class UserInterest(models.Model):
    """User's interests and preferences"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='users')
    intensity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_interests'
        unique_together = ['user', 'interest']
