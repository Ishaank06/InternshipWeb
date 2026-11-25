from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import UserProfile
from skills.models import SkillCategory, Skill, StudentSkill
from internships.models import Opportunity, OpportunitySkillRequirement, Application
from datetime import date, timedelta

class PortalCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create student user
        self.student_user = User.objects.create_user('test_student', 'student@test.com', 'pass123')
        self.student_profile = UserProfile.objects.create(
            user=self.student_user,
            role='STUDENT',
            roll_number='2022CS001',
            department='Computer Science & Engineering',
            cgpa=8.5
        )

        # Create recruiter user
        self.recruiter_user = User.objects.create_user('test_recruiter', 'rec@test.com', 'pass123')
        self.recruiter_profile = UserProfile.objects.create(
            user=self.recruiter_user,
            role='RECRUITER',
            company_name='Acme Corp'
        )

        # Create skills
        cat = SkillCategory.objects.create(name='Web Development')
        self.skill_python = Skill.objects.create(name='Python', category=cat, industry_demand_index=90)
        self.skill_django = Skill.objects.create(name='Django', category=cat, industry_demand_index=85)
        self.skill_docker = Skill.objects.create(name='Docker', category=cat, industry_demand_index=95)

        # Assign skills to student (Python: 4, Django: 3)
        StudentSkill.objects.create(student=self.student_profile, skill=self.skill_python, proficiency=4)
        StudentSkill.objects.create(student=self.student_profile, skill=self.skill_django, proficiency=3)

        # Create Opportunity requiring Python (req: 4) and Docker (req: 4)
        self.opp = Opportunity.objects.create(
            company=self.recruiter_profile,
            title='Backend Intern',
            opportunity_type='INTERNSHIP',
            work_mode='REMOTE',
            location='Remote',
            stipend_salary='₹30,000 / month',
            deadline=date.today() + timedelta(days=20),
            status='APPROVED'
        )
        OpportunitySkillRequirement.objects.create(opportunity=self.opp, skill=self.skill_python, min_proficiency=4)
        OpportunitySkillRequirement.objects.create(opportunity=self.opp, skill=self.skill_docker, min_proficiency=4)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Academia')
        self.assertContains(response, 'Industry')

    def test_skill_match_calculation(self):
        # Opportunity requires Python (4) and Docker (4) -> total points = 8
        # Student has Python (4) and Docker (0) -> student points = 4
        # Match percentage should be 4 / 8 = 50%
        match_score, matching, missing = self.opp.calculate_student_match(self.student_profile)
        self.assertEqual(match_score, 50)
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]['skill_name'], 'Python')
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]['skill_name'], 'Docker')

    def test_application_flow(self):
        self.client.login(username='test_student', password='pass123')
        response = self.client.post(f'/internships/{self.opp.id}/apply/', {
            'cover_letter': 'Very excited to apply for this backend role.',
            'portfolio_url': 'https://github.com/test'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Application.objects.filter(opportunity=self.opp, student=self.student_profile).exists())
        app = Application.objects.get(opportunity=self.opp, student=self.student_profile)
        self.assertEqual(app.match_score, 50)
