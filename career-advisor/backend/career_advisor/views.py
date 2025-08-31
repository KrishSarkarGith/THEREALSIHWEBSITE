from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Count
import openai
from decouple import config
import json
import logging

from .models import (
    User, Trait, Question, Assessment, Response as ResponseModel, AssessmentTrait,
    Skill, Interest, Domain, Career, CareerSkillMap, College,
    Course, Roadmap, Recommendation, UserSkill, UserInterest
)
from .serializers import (
    UserSerializer, TraitSerializer, QuestionSerializer, AssessmentSerializer,
    ResponseSerializer, AssessmentTraitSerializer, SkillSerializer, InterestSerializer,
    DomainSerializer, CareerSerializer, CareerSkillMapSerializer, CollegeSerializer,
    CourseSerializer, RoadmapSerializer, RecommendationSerializer, UserSkillSerializer,
    UserInterestSerializer, AssessmentStartSerializer, AssessmentSubmissionSerializer,
    CareerRecommendationRequestSerializer
)

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = config('OPENAI_API_KEY', default='')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TraitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get traits by category"""
        category = request.query_params.get('category', '')
        if category:
            traits = self.queryset.filter(category=category)
        else:
            traits = self.queryset
        serializer = self.get_serializer(traits, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def for_assessment(self, request):
        """Get questions for a specific assessment type"""
        assessment_type = request.query_params.get('type', 'comprehensive')
        # For comprehensive assessment, return all questions ordered by group
        if assessment_type == 'comprehensive':
            questions = self.queryset.order_by('group')
        else:
            questions = self.queryset.filter(question_type=assessment_type)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for development

    def get_queryset(self):
        """Filter assessments by current user"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        else:
            # For development, return all assessments
            return self.queryset.all()

    @action(detail=False, methods=['post'])
    def start_assessment(self, request):
        """Start a new assessment"""
        serializer = AssessmentStartSerializer(data=request.data)
        if serializer.is_valid():
            # For development, create a temporary user if none exists
            if request.user.is_authenticated:
                user = request.user
            else:
                # Create a temporary anonymous user for development
                user, created = User.objects.get_or_create(
                    username='anonymous_user',
                    defaults={
                        'email': 'anonymous@example.com',
                        'first_name': 'Anonymous',
                        'last_name': 'User',
                        'education_level': 'bachelor'
                    }
                )
            
            assessment = Assessment.objects.create(
                user=user,
                assessment_type=serializer.validated_data['assessment_type']
            )
            return Response({
                'assessment_id': assessment.id,
                'message': f'{assessment.assessment_type.title()} assessment started'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit_responses(self, request, pk=None):
        """Submit assessment responses and calculate scores"""
        assessment = self.get_object()
        serializer = AssessmentSubmissionSerializer(data=request.data)
        
        if serializer.is_valid():
            if assessment.status != 'in_progress':
                return Response(
                    {'error': 'Assessment is not in progress'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                with transaction.atomic():
                    # Save responses
                    responses_data = serializer.validated_data['responses']
                    for response_data in responses_data:
                        ResponseModel.objects.create(
                            assessment=assessment,
                            question_id=response_data['question_id'],
                            raw_response=response_data['response'],
                            response_time=response_data.get('response_time'),
                            weighted_score=self._calculate_response_score(response_data)
                        )
                    
                    # Calculate trait scores
                    self._calculate_trait_scores(assessment)
                    
                    # Generate AI summary
                    ai_summary = self._generate_ai_summary(assessment)
                    
                    # Mark assessment as completed
                    assessment.status = 'completed'
                    assessment.completed_at = timezone.now()
                    assessment.summary = ai_summary
                    assessment.save()
                    
                    return Response({
                        'message': 'Assessment completed successfully',
                        'summary': ai_summary
                    }, status=status.HTTP_200_OK)
                    
            except Exception as e:
                logger.error(f"Error submitting assessment: {str(e)}")
                return Response(
                    {'error': 'Failed to submit assessment'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _calculate_response_score(self, response_data):
        """Calculate weighted score for a response"""
        # This is a simplified scoring system - can be enhanced with ML
        question = Question.objects.get(id=response_data['question_id'])
        base_score = 5.0  # Base score out of 10
        
        # Simple scoring logic - can be enhanced
        if question.question_type == 'personality':
            # Personality questions get weighted by trait importance
            return base_score * question.weight
        elif question.question_type == 'interest':
            # Interest questions get higher weight for positive responses
            return base_score * question.weight * 1.2
        else:
            return base_score * question.weight

    def _calculate_trait_scores(self, assessment):
        """Calculate aggregated trait scores from responses"""
        responses = assessment.responses.all()
        
        # Group responses by trait and calculate weighted averages
        trait_scores = {}
        for response in responses:
            trait = response.question.trait
            if trait.id not in trait_scores:
                trait_scores[trait.id] = {'total_score': 0, 'total_weight': 0}
            
            trait_scores[trait.id]['total_score'] += response.weighted_score * response.question.weight
            trait_scores[trait.id]['total_weight'] += response.question.weight
        
        # Create or update AssessmentTrait records
        for trait_id, scores in trait_scores.items():
            avg_score = scores['total_score'] / scores['total_weight']
            # Normalize to 0-100 scale
            normalized_score = min(100, max(0, (avg_score / 10) * 100))
            
            AssessmentTrait.objects.update_or_create(
                assessment=assessment,
                trait_id=trait_id,
                defaults={'score': normalized_score}
            )

    def _generate_ai_summary(self, assessment):
        """Generate AI-powered assessment summary"""
        if not openai.api_key:
            return "Assessment completed. AI summary not available."
        
        try:
            # Get trait scores for context
            trait_scores = assessment.trait_scores.all()
            trait_summary = "\n".join([
                f"- {trait.trait.name}: {trait.score:.1f}/100"
                for trait in trait_scores
            ])
            
            prompt = f"""
            Based on the following assessment results, provide a brief, encouraging summary:
            
            Assessment Type: {assessment.assessment_type}
            Trait Scores:
            {trait_summary}
            
            Please provide a 2-3 sentence summary highlighting strengths and areas for growth.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return "Assessment completed successfully."

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.filter(is_active=True)
    serializer_class = CareerSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_domain(self, request):
        """Get careers by domain"""
        domain_id = request.query_params.get('domain_id')
        if domain_id:
            careers = self.queryset.filter(domain_id=domain_id)
        else:
            careers = self.queryset
        serializer = self.get_serializer(careers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search careers by title or description"""
        query = request.query_params.get('q', '')
        if query:
            careers = self.queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            careers = self.queryset
        serializer = self.get_serializer(careers, many=True)
        return Response(serializer.data)

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for development

    def get_queryset(self):
        """Filter recommendations by current user"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        else:
            # For development, return all recommendations
            return self.queryset.all()

    @action(detail=False, methods=['post'])
    def generate_career_recommendations(self, request):
        """Generate career recommendations based on assessment"""
        serializer = CareerRecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            assessment_id = serializer.validated_data['assessment_id']
            # For development, allow access to any assessment
            if request.user.is_authenticated:
                assessment = get_object_or_404(Assessment, id=assessment_id, user=request.user)
            else:
                assessment = get_object_or_404(Assessment, id=assessment_id)
            
            if assessment.status != 'completed':
                return Response(
                    {'error': 'Assessment must be completed first'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                recommendations = self._generate_recommendations(
                    assessment, 
                    serializer.validated_data
                )
                return Response(recommendations, status=status.HTTP_200_OK)
                
            except Exception as e:
                logger.error(f"Error generating recommendations: {str(e)}")
                return Response(
                    {'error': 'Failed to generate recommendations'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_recommendations(self, assessment, options):
        """Generate career recommendations using trait scores and ML"""
        trait_scores = assessment.trait_scores.all()
        
        # Get all careers
        careers = Career.objects.filter(is_active=True)
        career_scores = []
        
        for career in careers:
            match_score = self._calculate_career_match(career, trait_scores)
            if match_score > 0:  # Only include relevant matches
                career_scores.append({
                    'career': career,
                    'match_score': match_score
                })
        
        # Sort by match score and get top recommendations
        career_scores.sort(key=lambda x: x['match_score'], reverse=True)
        top_careers = career_scores[:options['max_recommendations']]
        
        recommendations = []
        for career_score in top_careers:
            career = career_score['career']
            match_score = career_score['match_score']
            
            # Generate AI explanation
            explanation = self._generate_career_explanation(career, trait_scores, match_score)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(career, assessment.user)
            
            # Get relevant courses and roadmaps
            suggested_courses = []
            suggested_roadmaps = []
            
            if options['include_courses']:
                suggested_courses = Course.objects.filter(
                    career_paths=career
                )[:3]
            
            if options['include_roadmaps']:
                suggested_roadmaps = Roadmap.objects.filter(
                    career=career
                )[:2]
            
            # Create recommendation
            recommendation = Recommendation.objects.create(
                user=assessment.user,
                assessment=assessment,
                career=career,
                match_score=match_score,
                reasoning=explanation,
                confidence_level=min(1.0, match_score / 100)
            )
            
            recommendation.skill_gaps.set(skill_gaps)
            recommendation.suggested_courses.set(suggested_courses)
            recommendation.suggested_roadmaps.set(suggested_roadmaps)
            
            recommendations.append(RecommendationSerializer(recommendation).data)
        
        return recommendations

    def _calculate_career_match(self, career, trait_scores):
        """Calculate match score between career and user traits"""
        total_score = 0
        total_weight = 0
        
        for trait_score in trait_scores:
            # Check if this trait is preferred for the career
            if career.preferred_traits.filter(id=trait_score.trait.id).exists():
                # Higher weight for preferred traits
                weight = 2.0
            else:
                weight = 1.0
            
            # Calculate score based on trait alignment
            trait_value = trait_score.score / 100.0  # Normalize to 0-1
            
            # Simple scoring: higher trait values get higher scores
            score = trait_value * weight
            total_score += score
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        # Convert to 0-100 scale
        return (total_score / total_weight) * 100

    def _generate_career_explanation(self, career, trait_scores, match_score):
        """Generate AI explanation for career recommendation"""
        if not openai.api_key:
            return f"Based on your assessment results, {career.title} shows a {match_score:.1f}% match."
        
        try:
            # Get top traits for context
            top_traits = sorted(trait_scores, key=lambda x: x.score, reverse=True)[:3]
            trait_context = "\n".join([
                f"- {trait.trait.name}: {trait.score:.1f}/100"
                for trait in top_traits
            ])
            
            prompt = f"""
            Explain why {career.title} is a good career match based on these trait scores:
            
            {trait_context}
            
            Career: {career.title}
            Domain: {career.domain.name}
            Match Score: {match_score:.1f}%
            
            Provide a brief, encouraging explanation in 2-3 sentences.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Based on your assessment results, {career.title} shows a {match_score:.1f}% match."

    def _identify_skill_gaps(self, career, user):
        """Identify skills the user lacks for the career"""
        required_skills = career.required_skills.all()
        user_skills = set(user.skills.values_list('skill_id', flat=True))
        
        skill_gaps = []
        for skill in required_skills:
            if skill.id not in user_skills:
                skill_gaps.append(skill)
        
        return skill_gaps

class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [AllowAny]

class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search colleges by name or location"""
        query = request.query_params.get('q', '')
        if query:
            colleges = self.queryset.filter(
                Q(name__icontains=query) | Q(location__icontains=query)
            )
        else:
            colleges = self.queryset
        serializer = self.get_serializer(colleges, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_career(self, request):
        """Get courses relevant to a specific career"""
        career_id = request.query_params.get('career_id')
        if career_id:
            courses = self.queryset.filter(career_paths__id=career_id)
        else:
            courses = self.queryset
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class RoadmapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Roadmap.objects.all()
    serializer_class = RoadmapSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_career(self, request):
        """Get roadmaps for a specific career"""
        career_id = request.query_params.get('career_id')
        if career_id:
            roadmaps = self.queryset.filter(career_id=career_id)
        else:
            roadmaps = self.queryset
        serializer = self.get_serializer(roadmaps, many=True)
        return Response(serializer.data)

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter skills by current user"""
        return self.queryset.filter(user=self.request.user)

class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter interests by current user"""
        return self.queryset.filter(user=self.request.user)

# Additional ViewSets for missing models
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter responses by current user's assessments"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(assessment__user=self.request.user)
        else:
            # For development, return all responses
            return self.queryset.all()

class AssessmentTraitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssessmentTrait.objects.all()
    serializer_class = AssessmentTraitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter trait scores by current user's assessments"""
        return self.queryset.filter(assessment__user=self.request.user)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]

class CareerSkillMapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CareerSkillMap.objects.all()
    serializer_class = CareerSkillMapSerializer
    permission_classes = [AllowAny]
