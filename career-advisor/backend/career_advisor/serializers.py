from rest_framework import serializers
from .models import (
    User, Trait, Question, Assessment, Response, AssessmentTrait,
    Skill, Interest, Domain, Career, CareerSkillMap, College,
    Course, Roadmap, Recommendation, UserSkill, UserInterest
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'education_level', 'location', 'preferences', 'created_at']
        read_only_fields = ['id', 'created_at']

class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    trait_name = serializers.CharField(source='trait.name', read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    trait_name = serializers.CharField(source='question.trait.name', read_only=True)
    
    class Meta:
        model = Response
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)
    trait_scores = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = '__all__'
    
    def get_trait_scores(self, obj):
        return AssessmentTraitSerializer(obj.trait_scores.all(), many=True).data

class AssessmentTraitSerializer(serializers.ModelSerializer):
    trait_name = serializers.CharField(source='trait.name', read_only=True)
    
    class Meta:
        model = AssessmentTrait
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)
    preferred_traits = TraitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Career
        fields = '__all__'

class CareerSkillMapSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = CareerSkillMap
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    skills_covered = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class RoadmapSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    
    class Meta:
        model = Roadmap
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    career_description = serializers.CharField(source='career.description', read_only=True)
    domain_name = serializers.CharField(source='career.domain.name', read_only=True)
    skill_gaps = SkillSerializer(many=True, read_only=True)
    suggested_courses = CourseSerializer(many=True, read_only=True)
    suggested_roadmaps = RoadmapSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recommendation
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)
    
    class Meta:
        model = UserSkill
        fields = '__all__'

class UserInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.CharField(source='interest.name', read_only=True)
    interest_category = serializers.CharField(source='interest.category', read_only=True)
    
    class Meta:
        model = UserInterest
        fields = '__all__'

# Special serializers for assessment flow
class AssessmentStartSerializer(serializers.Serializer):
    assessment_type = serializers.ChoiceField(choices=[
        ('personality', 'Personality'),
        ('interest', 'Interest'),
        ('aptitude', 'Aptitude'),
        ('comprehensive', 'Comprehensive')
    ])

class QuestionResponseSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    response = serializers.CharField()
    response_time = serializers.IntegerField(required=False)

class AssessmentSubmissionSerializer(serializers.Serializer):
    assessment_id = serializers.UUIDField()
    responses = QuestionResponseSerializer(many=True)

class CareerRecommendationRequestSerializer(serializers.Serializer):
    assessment_id = serializers.UUIDField()
    include_courses = serializers.BooleanField(default=True)
    include_roadmaps = serializers.BooleanField(default=True)
    max_recommendations = serializers.IntegerField(default=5, min_value=1, max_value=20)
