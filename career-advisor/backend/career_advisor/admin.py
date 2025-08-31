from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Trait, Question, Assessment, Response, AssessmentTrait,
    Skill, Interest, Domain, Career, CareerSkillMap, College,
    Course, Roadmap, Recommendation, UserSkill, UserInterest
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'education_level', 'location', 'created_at']
    list_filter = ['education_level', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Career Advisor Info', {
            'fields': ('education_level', 'location', 'preferences')
        }),
    )

@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_type', 'trait', 'weight', 'is_active']
    list_filter = ['question_type', 'trait', 'is_active', 'created_at']
    search_fields = ['text', 'trait__name']
    ordering = ['question_type', 'trait__name']

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment_type', 'status', 'overall_score', 'started_at']
    list_filter = ['assessment_type', 'status', 'started_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-started_at']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'question', 'weighted_score', 'response_time', 'created_at']
    list_filter = ['created_at']
    search_fields = ['assessment__user__username', 'question__text']
    ordering = ['-created_at']

@admin.register(AssessmentTrait)
class AssessmentTraitAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'trait', 'score', 'percentile', 'created_at']
    list_filter = ['trait', 'created_at']
    search_fields = ['assessment__user__username', 'trait__name']
    ordering = ['-created_at']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'growth_potential', 'created_at']
    list_filter = ['industry', 'growth_potential', 'created_at']
    search_fields = ['name', 'description', 'industry']
    ordering = ['industry', 'name']

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['title', 'domain', 'job_outlook', 'is_active', 'created_at']
    list_filter = ['domain', 'job_outlook', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'domain__name']
    ordering = ['domain__name', 'title']
    filter_horizontal = ['required_skills', 'preferred_traits']

@admin.register(CareerSkillMap)
class CareerSkillMapAdmin(admin.ModelAdmin):
    list_display = ['career', 'skill', 'importance_level', 'created_at']
    list_filter = ['importance_level', 'created_at']
    search_fields = ['career__title', 'skill__name']
    ordering = ['career__title', 'skill__name']

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'country', 'type', 'ranking', 'created_at']
    list_filter = ['type', 'country', 'created_at']
    search_fields = ['name', 'location', 'country']
    ordering = ['country', 'name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'level', 'duration', 'is_online', 'created_at']
    list_filter = ['level', 'is_online', 'created_at']
    search_fields = ['name', 'college__name', 'description']
    ordering = ['college__name', 'name']
    filter_horizontal = ['skills_covered', 'career_paths']

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ['title', 'career', 'target_audience', 'duration_months', 'difficulty_level', 'created_at']
    list_filter = ['difficulty_level', 'created_at']
    search_fields = ['title', 'career__title', 'description']
    ordering = ['career__title', 'title']
    filter_horizontal = ['prerequisites']

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'career', 'match_score', 'confidence_level', 'created_at']
    list_filter = ['match_score', 'confidence_level', 'created_at']
    search_fields = ['user__username', 'career__title']
    ordering = ['-match_score', '-created_at']
    filter_horizontal = ['skill_gaps', 'suggested_courses', 'suggested_roadmaps']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'years_of_experience', 'is_verified', 'created_at']
    list_filter = ['proficiency_level', 'is_verified', 'created_at']
    search_fields = ['user__username', 'skill__name']
    ordering = ['user__username', 'skill__name']

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'interest', 'intensity', 'created_at']
    list_filter = ['intensity', 'created_at']
    search_fields = ['user__username', 'interest__name']
    ordering = ['user__username', 'interest__name']
