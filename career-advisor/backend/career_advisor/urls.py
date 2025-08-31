from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'traits', views.TraitViewSet, basename='trait')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'assessments', views.AssessmentViewSet, basename='assessment')
router.register(r'responses', views.ResponseViewSet, basename='response')
router.register(r'assessment-traits', views.AssessmentTraitViewSet, basename='assessment-trait')
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'interests', views.InterestViewSet, basename='interest')
router.register(r'domains', views.DomainViewSet, basename='domain')
router.register(r'careers', views.CareerViewSet, basename='career')
router.register(r'career-skill-maps', views.CareerSkillMapViewSet, basename='career-skill-map')
router.register(r'colleges', views.CollegeViewSet, basename='college')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'roadmaps', views.RoadmapViewSet, basename='roadmap')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')
router.register(r'user-skills', views.UserSkillViewSet, basename='user-skill')
router.register(r'user-interests', views.UserInterestViewSet, basename='user-interest')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]
