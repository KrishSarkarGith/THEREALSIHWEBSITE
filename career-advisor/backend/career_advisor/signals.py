from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assessment, Response, AssessmentTrait

@receiver(post_save, sender=Response)
def update_assessment_progress(sender, instance, created, **kwargs):
    """Update assessment progress when responses are added"""
    if created:
        assessment = instance.assessment
        total_responses = assessment.responses.count()
        
        # You can add logic here to determine if assessment is complete
        # For example, check if all required questions are answered
        
        # Update assessment status if needed
        if assessment.status == 'in_progress' and total_responses >= 10:  # Example threshold
            # Assessment might be ready for completion
            pass

@receiver(post_save, sender=AssessmentTrait)
def calculate_percentiles(sender, instance, created, **kwargs):
    """Calculate percentile scores for trait scores"""
    if created:
        # Get all scores for this trait across all assessments
        all_scores = AssessmentTrait.objects.filter(
            trait=instance.trait
        ).values_list('score', flat=True)
        
        if len(all_scores) > 1:
            # Calculate percentile (simplified approach)
            sorted_scores = sorted(all_scores)
            instance_index = sorted_scores.index(instance.score)
            percentile = (instance_index / (len(sorted_scores) - 1)) * 100
            
            # Update without triggering the signal again
            AssessmentTrait.objects.filter(id=instance.id).update(percentile=percentile)
