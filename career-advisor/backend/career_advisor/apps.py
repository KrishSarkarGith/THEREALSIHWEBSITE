from django.apps import AppConfig


class CareerAdvisorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'career_advisor'
    verbose_name = 'Career Advisor'

    def ready(self):
        import career_advisor.signals
