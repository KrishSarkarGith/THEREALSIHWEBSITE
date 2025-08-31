from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from career_advisor.models import (
    Trait, Question, Skill, Interest, Domain, Career, College, Course, Roadmap
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data for career advisor app'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create traits
        traits = self.create_traits()
        
        # Create questions
        self.create_questions(traits)
        
        # Create skills
        skills = self.create_skills()
        
        # Create interests
        interests = self.create_interests()
        
        # Create domains
        domains = self.create_domains()
        
        # Create careers
        careers = self.create_careers(domains, skills, traits)
        
        # Create colleges
        colleges = self.create_colleges()
        
        # Create courses
        self.create_courses(colleges, skills, careers)
        
        # Create roadmaps
        self.create_roadmaps(careers, skills)
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_traits(self):
        traits_data = [
            {'name': 'Teamwork', 'description': 'Ability to work effectively in teams', 'category': 'personality'},
            {'name': 'Decision Making', 'description': 'Comfort with making decisions under pressure', 'category': 'personality'},
            {'name': 'Logical Thinking', 'description': 'Enjoyment of solving logical puzzles', 'category': 'cognitive'},
            {'name': 'Working Style', 'description': 'Preferred approach to work tasks', 'category': 'personality'},
            {'name': 'Self Awareness', 'description': 'Understanding of personal strengths', 'category': 'personality'},
            {'name': 'Innovation', 'description': 'Interest in exploring new trends', 'category': 'interests'},
            {'name': 'Work Preference', 'description': 'Preference for working with people, data, or things', 'category': 'interests'},
            {'name': 'Hobbies', 'description': 'Active pursuit of recreational activities', 'category': 'interests'},
            {'name': 'Career Aspiration', 'description': 'Dream career without financial constraints', 'category': 'interests'},
            {'name': 'Problem Solving', 'description': 'Ability to solve complex problems', 'category': 'skills'},
            {'name': 'Communication', 'description': 'Effectiveness in verbal and written communication', 'category': 'skills'},
            {'name': 'Technical Skills', 'description': 'Proficiency in technical areas', 'category': 'skills'},
            {'name': 'Creative Skills', 'description': 'Proficiency in creative areas', 'category': 'skills'},
            {'name': 'Management Skills', 'description': 'Proficiency in management areas', 'category': 'skills'},
            {'name': 'Research Skills', 'description': 'Proficiency in research areas', 'category': 'skills'},
            {'name': 'Work Environment', 'description': 'Preferred type of work environment', 'category': 'preferences'},
            {'name': 'Risk Tolerance', 'description': 'Preference for stability vs high risk-high reward', 'category': 'preferences'},
            {'name': 'Collaboration Style', 'description': 'Preference for individual vs collaborative work', 'category': 'preferences'},
            {'name': 'Relocation Willingness', 'description': 'Comfort with relocating for career opportunities', 'category': 'preferences'},
            {'name': 'Motivation Factors', 'description': 'Primary factors that motivate work', 'category': 'preferences'},
            {'name': 'Learning Mode', 'description': 'Preferred method of learning', 'category': 'learning'},
            {'name': 'Self-Paced Learning', 'description': 'Enjoyment of self-paced learning', 'category': 'learning'},
            {'name': 'Learning Approach', 'description': 'Preference for theoretical vs hands-on learning', 'category': 'learning'},
            {'name': 'Subject Interest', 'description': 'Fascination with specific subjects or topics', 'category': 'learning'},
            {'name': 'Learning Resources', 'description': 'Preferred resources for learning', 'category': 'learning'},
            {'name': 'Education Level', 'description': 'Current level of education', 'category': 'constraints'},
            {'name': 'Budget Constraint', 'description': 'Budget available for higher studies', 'category': 'constraints'},
            {'name': 'Work-Life Balance', 'description': 'Importance of work-life balance', 'category': 'constraints'},
            {'name': 'Career Vision', 'description': 'Five-year career vision', 'category': 'constraints'},
            {'name': 'Career Path Openness', 'description': 'Openness to unconventional career paths', 'category': 'constraints'},
        ]
        
        traits = []
        for trait_data in traits_data:
            trait, created = Trait.objects.get_or_create(
                name=trait_data['name'],
                defaults=trait_data
            )
            traits.append(trait)
            if created:
                self.stdout.write(f'Created trait: {trait.name}')
        
        return traits

    def create_questions(self, traits):
        questions_data = [
            # Group 1: Personality Traits
            {'text': 'I enjoy working in a team.', 'type': 'likert', 'trait': 'Teamwork', 'group': 1},
            {'text': 'I am comfortable making decisions under pressure.', 'type': 'likert', 'trait': 'Decision Making', 'group': 1},
            {'text': 'I enjoy solving logical puzzles.', 'type': 'likert', 'trait': 'Logical Thinking', 'group': 1},
            {'text': 'Which best describes your working style?', 'type': 'single_choice', 'trait': 'Working Style', 'group': 1, 'options': ['Analytical', 'Creative', 'Practical', 'Strategic']},
            {'text': 'Describe one strength you are proud of.', 'type': 'text_input', 'trait': 'Self Awareness', 'group': 1},
            
            # Group 2: Interests & Passions
            {'text': 'Which fields excite you the most?', 'type': 'multi_select', 'trait': 'Innovation', 'group': 2, 'options': ['Technology', 'Arts', 'Business', 'Healthcare', 'Law', 'Education']},
            {'text': 'I enjoy exploring new and emerging trends.', 'type': 'likert', 'trait': 'Innovation', 'group': 2},
            {'text': 'Do you prefer working with people, data, or things?', 'type': 'single_choice', 'trait': 'Work Preference', 'group': 2, 'options': ['People', 'Data', 'Things']},
            {'text': 'Hobbies you actively pursue:', 'type': 'multi_select', 'trait': 'Hobbies', 'group': 2, 'options': ['Reading', 'Gaming', 'Sports', 'Music', 'Volunteering', 'Other']},
            {'text': 'If money wasn\'t a concern, what career would you try?', 'type': 'text_input', 'trait': 'Career Aspiration', 'group': 2},
            
            # Group 3: Skills Assessment
            {'text': 'Rate your problem-solving skills.', 'type': 'likert', 'trait': 'Problem Solving', 'group': 3},
            {'text': 'Rate your communication skills.', 'type': 'likert', 'trait': 'Communication', 'group': 3},
            {'text': 'Which area do you feel most skilled in?', 'type': 'single_choice', 'trait': 'Technical Skills', 'group': 3, 'options': ['Technical', 'Creative', 'Management', 'Research']},
            {'text': 'Which of these do you have experience with?', 'type': 'multi_select', 'trait': 'Technical Skills', 'group': 3, 'options': ['Programming', 'Public Speaking', 'Writing', 'Design', 'Data Analysis', 'Leadership']},
            {'text': 'What\'s one skill you wish to master?', 'type': 'text_input', 'trait': 'Technical Skills', 'group': 3},
            
            # Group 4: Work Preferences
            {'text': 'Which work environment do you prefer?', 'type': 'single_choice', 'trait': 'Work Environment', 'group': 4, 'options': ['Startup', 'Corporate', 'Academia', 'Freelance']},
            {'text': 'I value job stability over high risk-high reward opportunities.', 'type': 'likert', 'trait': 'Risk Tolerance', 'group': 4},
            {'text': 'Would you prefer to work individually or collaboratively?', 'type': 'single_choice', 'trait': 'Collaboration Style', 'group': 4, 'options': ['Individually', 'Collaboratively', 'Both']},
            {'text': 'I am comfortable relocating for career opportunities.', 'type': 'likert', 'trait': 'Relocation Willingness', 'group': 4},
            {'text': 'What motivates you the most?', 'type': 'multi_select', 'trait': 'Motivation Factors', 'group': 4, 'options': ['Salary', 'Impact', 'Growth', 'Recognition', 'Learning']},
            
            # Group 5: Learning Style & Education
            {'text': 'Which learning mode do you prefer?', 'type': 'single_choice', 'trait': 'Learning Mode', 'group': 5, 'options': ['Online', 'Offline', 'Hybrid']},
            {'text': 'I enjoy self-paced learning.', 'type': 'likert', 'trait': 'Self-Paced Learning', 'group': 5},
            {'text': 'Do you prefer theoretical or hands-on learning?', 'type': 'single_choice', 'trait': 'Learning Approach', 'group': 5, 'options': ['Theoretical', 'Hands-on', 'Both']},
            {'text': 'Name one subject/topic you find fascinating.', 'type': 'text_input', 'trait': 'Subject Interest', 'group': 5},
            {'text': 'Which resources do you usually use?', 'type': 'multi_select', 'trait': 'Learning Resources', 'group': 5, 'options': ['Books', 'YouTube', 'Online Courses', 'Internships', 'Mentorship']},
            
            # Group 6: Constraints & Career Goals
            {'text': 'What is your current education level?', 'type': 'single_choice', 'trait': 'Education Level', 'group': 6, 'options': ['High School', 'Undergraduate', 'Postgraduate']},
            {'text': 'What is your budget for higher studies?', 'type': 'single_choice', 'trait': 'Budget Constraint', 'group': 6, 'options': ['Low', 'Medium', 'High', 'Not sure']},
            {'text': 'Work-life balance is important to me.', 'type': 'likert', 'trait': 'Work-Life Balance', 'group': 6},
            {'text': 'Where do you see yourself in 5 years?', 'type': 'text_input', 'trait': 'Career Vision', 'group': 6},
            {'text': 'Are you open to unconventional career paths?', 'type': 'single_choice', 'trait': 'Career Path Openness', 'group': 6, 'options': ['Yes', 'No', 'Maybe']},
        ]
        
        for question_data in questions_data:
            trait = next(t for t in traits if t.name == question_data['trait'])
            question, created = Question.objects.get_or_create(
                text=question_data['text'],
                defaults={
                    'question_type': question_data['type'],
                    'trait': trait,
                    'weight': 1.0,
                    'group': question_data['group'],
                    'options': question_data.get('options', [])
                }
            )
            if created:
                self.stdout.write(f'Created question: {question.text[:50]}...')

    def create_skills(self):
        skills_data = [
            {'name': 'Python Programming', 'description': 'Programming in Python language', 'category': 'technical'},
            {'name': 'Data Analysis', 'description': 'Analyzing and interpreting data', 'category': 'technical'},
            {'name': 'Project Management', 'description': 'Managing projects and teams', 'category': 'soft'},
            {'name': 'Communication', 'description': 'Effective verbal and written communication', 'category': 'soft'},
            {'name': 'Problem Solving', 'description': 'Identifying and solving complex problems', 'category': 'cognitive'},
            {'name': 'Machine Learning', 'description': 'Understanding and applying ML algorithms', 'category': 'technical'},
            {'name': 'Web Development', 'description': 'Building web applications', 'category': 'technical'},
            {'name': 'Leadership', 'description': 'Leading teams and organizations', 'category': 'soft'},
            {'name': 'Creative Design', 'description': 'Creating visual and creative content', 'category': 'creative'},
            {'name': 'Research Methods', 'description': 'Conducting research and analysis', 'category': 'research'},
            {'name': 'Public Speaking', 'description': 'Effective presentation and speaking skills', 'category': 'soft'},
            {'name': 'Writing', 'description': 'Professional writing and documentation', 'category': 'soft'},
            {'name': 'Design Thinking', 'description': 'Creative problem-solving approach', 'category': 'creative'},
            {'name': 'Data Visualization', 'description': 'Creating charts and visual representations', 'category': 'technical'},
            {'name': 'Team Management', 'description': 'Managing and coordinating team efforts', 'category': 'management'},
        ]
        
        skills = []
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            skills.append(skill)
            if created:
                self.stdout.write(f'Created skill: {skill.name}')
        
        return skills

    def create_interests(self):
        interests_data = [
            {'name': 'Technology', 'description': 'Interest in technology and innovation', 'category': 'technology'},
            {'name': 'Arts', 'description': 'Interest in creative arts and design', 'category': 'arts'},
            {'name': 'Business', 'description': 'Interest in business and entrepreneurship', 'category': 'business'},
            {'name': 'Healthcare', 'description': 'Interest in medical and healthcare services', 'category': 'healthcare'},
            {'name': 'Law', 'description': 'Interest in legal and justice systems', 'category': 'law'},
            {'name': 'Education', 'description': 'Interest in teaching and learning', 'category': 'education'},
            {'name': 'Science', 'description': 'Interest in scientific research and discovery', 'category': 'science'},
            {'name': 'Sports', 'description': 'Interest in sports and physical activities', 'category': 'sports'},
            {'name': 'Music', 'description': 'Interest in musical arts and performance', 'category': 'arts'},
            {'name': 'Reading', 'description': 'Interest in literature and knowledge', 'category': 'intellectual'},
            {'name': 'Gaming', 'description': 'Interest in video games and interactive media', 'category': 'entertainment'},
            {'name': 'Volunteering', 'description': 'Interest in community service and helping others', 'category': 'social'},
        ]
        
        interests = []
        for interest_data in interests_data:
            interest, created = Interest.objects.get_or_create(
                name=interest_data['name'],
                defaults=interest_data
            )
            interests.append(interest)
            if created:
                self.stdout.write(f'Created interest: {interest.name}')
        
        return interests

    def create_domains(self):
        domains_data = [
            {'name': 'Technology', 'description': 'Information technology and software development', 'industry': 'Technology', 'growth_potential': 'high'},
            {'name': 'Healthcare', 'description': 'Medical and healthcare services', 'industry': 'Healthcare', 'growth_potential': 'high'},
            {'name': 'Finance', 'description': 'Banking, investment, and financial services', 'industry': 'Finance', 'growth_potential': 'medium'},
            {'name': 'Education', 'description': 'Educational institutions and training', 'industry': 'Education', 'growth_potential': 'medium'},
            {'name': 'Manufacturing', 'description': 'Industrial manufacturing and production', 'industry': 'Manufacturing', 'growth_potential': 'medium'},
            {'name': 'Arts & Media', 'description': 'Creative arts, entertainment, and media', 'industry': 'Arts', 'growth_potential': 'medium'},
            {'name': 'Law & Policy', 'description': 'Legal services and public policy', 'industry': 'Law', 'growth_potential': 'medium'},
            {'name': 'Research & Development', 'description': 'Scientific research and development', 'industry': 'Science', 'growth_potential': 'high'},
        ]
        
        domains = []
        for domain_data in domains_data:
            domain, created = Domain.objects.get_or_create(
                name=domain_data['name'],
                defaults=domain_data
            )
            domains.append(domain)
            if created:
                self.stdout.write(f'Created domain: {domain.name}')
        
        return domains

    def create_careers(self, domains, skills, traits):
        careers_data = [
            {
                'title': 'Data Scientist',
                'description': 'Analyze complex data to help organizations make better decisions',
                'domain': 'Technology',
                'required_skills': ['Python Programming', 'Data Analysis', 'Machine Learning'],
                'preferred_traits': ['Logical Thinking', 'Problem Solving'],
                'job_outlook': 'excellent'
            },
            {
                'title': 'Software Engineer',
                'description': 'Design, develop, and maintain software applications',
                'domain': 'Technology',
                'required_skills': ['Python Programming', 'Web Development', 'Problem Solving'],
                'preferred_traits': ['Logical Thinking', 'Problem Solving'],
                'job_outlook': 'excellent'
            },
            {
                'title': 'Project Manager',
                'description': 'Plan and oversee projects to ensure they are completed on time and within budget',
                'domain': 'Technology',
                'required_skills': ['Project Management', 'Communication', 'Leadership'],
                'preferred_traits': ['Leadership', 'Decision Making'],
                'job_outlook': 'good'
            },
            {
                'title': 'UX Designer',
                'description': 'Create user-friendly and visually appealing digital experiences',
                'domain': 'Arts & Media',
                'required_skills': ['Creative Design', 'Design Thinking', 'Communication'],
                'preferred_traits': ['Creative Skills', 'Teamwork'],
                'job_outlook': 'good'
            },
            {
                'title': 'Research Analyst',
                'description': 'Conduct research and analysis to support decision-making',
                'domain': 'Research & Development',
                'required_skills': ['Research Methods', 'Data Analysis', 'Writing'],
                'preferred_traits': ['Logical Thinking', 'Problem Solving'],
                'job_outlook': 'good'
            },
            {
                'title': 'Healthcare Administrator',
                'description': 'Manage healthcare facilities and coordinate patient care services',
                'domain': 'Healthcare',
                'required_skills': ['Project Management', 'Communication', 'Leadership'],
                'preferred_traits': ['Teamwork', 'Decision Making'],
                'job_outlook': 'excellent'
            },
            {
                'title': 'Financial Analyst',
                'description': 'Analyze financial data and provide investment guidance',
                'domain': 'Finance',
                'required_skills': ['Data Analysis', 'Problem Solving', 'Communication'],
                'preferred_traits': ['Logical Thinking', 'Decision Making'],
                'job_outlook': 'good'
            },
            {
                'title': 'Educational Consultant',
                'description': 'Advise educational institutions on curriculum and teaching methods',
                'domain': 'Education',
                'required_skills': ['Communication', 'Research Methods', 'Leadership'],
                'preferred_traits': ['Teamwork', 'Innovation'],
                'job_outlook': 'medium'
            },
        ]
        
        careers = []
        for career_data in careers_data:
            domain = next(d for d in domains if d.name == career_data['domain'])
            career, created = Career.objects.get_or_create(
                title=career_data['title'],
                defaults={
                    'description': career_data['description'],
                    'domain': domain,
                    'job_outlook': career_data['job_outlook'],
                    'education_requirements': ['Bachelor\'s Degree'],
                    'experience_levels': ['Entry Level', 'Mid Level', 'Senior Level'],
                    'salary_range': {'entry': 60000, 'mid': 90000, 'senior': 130000}
                }
            )
            
            # Add required skills
            for skill_name in career_data['required_skills']:
                skill = next(s for s in skills if s.name == skill_name)
                career.required_skills.add(skill)
            
            # Add preferred traits
            for trait_name in career_data['preferred_traits']:
                try:
                    trait = next(t for t in traits if t.name == trait_name)
                    career.preferred_traits.add(trait)
                except StopIteration:
                    self.stdout.write(f'Warning: Trait "{trait_name}" not found for career "{career.title}"')
            
            careers.append(career)
            if created:
                self.stdout.write(f'Created career: {career.title}')
        
        return careers

    def create_colleges(self):
        colleges_data = [
            {'name': 'MIT', 'location': 'Cambridge, MA', 'country': 'USA', 'type': 'university', 'ranking': 1},
            {'name': 'Stanford University', 'location': 'Stanford, CA', 'country': 'USA', 'type': 'university', 'ranking': 2},
            {'name': 'Harvard University', 'location': 'Cambridge, MA', 'country': 'USA', 'type': 'university', 'ranking': 3},
            {'name': 'IIT Delhi', 'location': 'New Delhi', 'country': 'India', 'type': 'university', 'ranking': 4},
            {'name': 'IIT Bombay', 'location': 'Mumbai', 'country': 'India', 'type': 'university', 'ranking': 5},
            {'name': 'NIT Trichy', 'location': 'Tiruchirappalli', 'country': 'India', 'type': 'university', 'ranking': 6},
        ]
        
        colleges = []
        for college_data in colleges_data:
            college, created = College.objects.get_or_create(
                name=college_data['name'],
                defaults=college_data
            )
            colleges.append(college)
            if created:
                self.stdout.write(f'Created college: {college.name}')
        
        return colleges

    def create_courses(self, colleges, skills, careers):
        courses_data = [
            {
                'name': 'Introduction to Data Science',
                'description': 'Learn the fundamentals of data science and analytics',
                'college': 'MIT',
                'duration': '4 months',
                'level': 'certificate',
                'skills_covered': ['Data Analysis', 'Python Programming'],
                'career_paths': ['Data Scientist']
            },
            {
                'name': 'Computer Science Degree',
                'description': 'Bachelor\'s degree in computer science',
                'college': 'Stanford University',
                'duration': '4 years',
                'level': 'bachelor',
                'skills_covered': ['Python Programming', 'Web Development', 'Problem Solving'],
                'career_paths': ['Software Engineer']
            },
            {
                'name': 'Project Management Professional',
                'description': 'PMP certification for project managers',
                'college': 'IIT Delhi',
                'duration': '6 months',
                'level': 'certificate',
                'skills_covered': ['Project Management', 'Leadership'],
                'career_paths': ['Project Manager']
            },
            {
                'name': 'UX Design Bootcamp',
                'description': 'Intensive course in user experience design',
                'college': 'NIT Trichy',
                'duration': '3 months',
                'level': 'certificate',
                'skills_covered': ['Creative Design', 'Design Thinking'],
                'career_paths': ['UX Designer']
            },
            {
                'name': 'Data Analysis Fundamentals',
                'description': 'Learn data analysis and visualization',
                'college': 'IIT Bombay',
                'duration': '4 months',
                'level': 'certificate',
                'skills_covered': ['Data Analysis', 'Data Visualization'],
                'career_paths': ['Research Analyst', 'Financial Analyst']
            },
        ]
        
        for course_data in courses_data:
            college = next(c for c in colleges if c.name == course_data['college'])
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                college=college,
                defaults={
                    'description': course_data['description'],
                    'duration': course_data['duration'],
                    'level': course_data['level'],
                    'fees': 50000,
                    'is_online': False
                }
            )
            
            # Add skills covered
            for skill_name in course_data['skills_covered']:
                skill = next(s for s in skills if s.name == skill_name)
                course.skills_covered.add(skill)
            
            # Add career paths
            for career_title in course_data['career_paths']:
                career = next(c for c in careers if c.title == career_title)
                course.career_paths.add(career)
            
            if created:
                self.stdout.write(f'Created course: {course.name}')

    def create_roadmaps(self, careers, skills):
        roadmaps_data = [
            {
                'title': 'Data Scientist Career Path',
                'description': 'Complete roadmap to become a data scientist',
                'career': 'Data Scientist',
                'target_audience': 'Recent graduates and career changers',
                'duration_months': 24,
                'steps': [
                    'Learn Python programming basics',
                    'Study statistics and mathematics',
                    'Learn data analysis tools',
                    'Practice with real datasets',
                    'Build portfolio projects'
                ],
                'difficulty_level': 'intermediate'
            },
            {
                'title': 'Software Engineer Career Path',
                'description': 'Complete roadmap to become a software engineer',
                'career': 'Software Engineer',
                'target_audience': 'Recent graduates and career changers',
                'duration_months': 18,
                'steps': [
                    'Learn programming fundamentals',
                    'Study data structures and algorithms',
                    'Learn web development basics',
                    'Build personal projects',
                    'Contribute to open source'
                ],
                'difficulty_level': 'intermediate'
            },
            {
                'title': 'UX Designer Career Path',
                'description': 'Complete roadmap to become a UX designer',
                'career': 'UX Designer',
                'target_audience': 'Creative individuals and career changers',
                'duration_months': 12,
                'steps': [
                    'Learn design principles',
                    'Study user psychology',
                    'Master design tools',
                    'Create portfolio projects',
                    'Get feedback and iterate'
                ],
                'difficulty_level': 'beginner'
            },
        ]
        
        for roadmap_data in roadmaps_data:
            career = next(c for c in careers if c.title == roadmap_data['career'])
            roadmap, created = Roadmap.objects.get_or_create(
                title=roadmap_data['title'],
                career=career,
                defaults={
                    'description': roadmap_data['description'],
                    'target_audience': roadmap_data['target_audience'],
                    'duration_months': roadmap_data['duration_months'],
                    'steps': roadmap_data['steps'],
                    'difficulty_level': roadmap_data['difficulty_level']
                }
            )
            
            if created:
                self.stdout.write(f'Created roadmap: {roadmap.title}')
