from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile
from skills.models import SkillCategory, Skill, StudentSkill
from internships.models import Opportunity, OpportunitySkillRequirement, Application
from collaboration.models import CollaborationProject, CurriculumFeedback, IndustryMoU
from datetime import date, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds database with realistic demo data for Academia-Industry Collaboration Portal'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        Application.objects.all().delete()
        OpportunitySkillRequirement.objects.all().delete()
        Opportunity.objects.all().delete()
        StudentSkill.objects.all().delete()
        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()
        CollaborationProject.objects.all().delete()
        CurriculumFeedback.objects.all().delete()
        IndustryMoU.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating Users & Profiles..."))

        # 1. Superuser / Admin
        admin_user = User.objects.create_superuser('admin', 'admin@university.edu', 'admin123')
        admin_user.first_name = 'Portal'
        admin_user.last_name = 'Administrator'
        admin_user.save()
        UserProfile.objects.create(
            user=admin_user,
            role='ADMIN',
            phone='+91 98765 00001',
            bio='Central Administrator for Academia-Industry Integration & Accreditation.'
        )

        # 2. Faculty / TPO Head
        tpo_user = User.objects.create_user('prof_sharma', 'tpo@university.edu', 'tpo123')
        tpo_user.first_name = 'Dr. Rajiv'
        tpo_user.last_name = 'Sharma'
        tpo_user.save()
        tpo_profile = UserProfile.objects.create(
            user=tpo_user,
            role='FACULTY_TPO',
            phone='+91 98765 43210',
            employee_id='FAC-CS-108',
            faculty_department='Training, Placement & Corporate Relations',
            bio='Head of Training and Placement Cell. Dedicated to bridging industry demand with university talent.'
        )

        # 3. Recruiters / Industry
        # Recruiter 1: Google India
        rec1_user = User.objects.create_user('google_recruiter', 'sundar.r@google.mock', 'pass123')
        rec1_user.first_name = 'Sundar'
        rec1_user.last_name = 'Ramaswamy'
        rec1_user.save()
        rec1_profile = UserProfile.objects.create(
            user=rec1_user,
            role='RECRUITER',
            phone='+91 80 6721 8000',
            company_name='Google Cloud & Engineering India',
            company_website='https://careers.google.com',
            company_sector='Cloud Infrastructure & Software Systems',
            designation='Lead Campus Talent Partner',
            company_address='RMZ Infinity, Old Madras Road, Bengaluru',
            company_logo='https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
            bio='Hiring brilliant student innovators for summer internships and entry-level engineering roles.'
        )

        # Recruiter 2: Microsoft India
        rec2_user = User.objects.create_user('microsoft_recruiter', 'ananya.sen@microsoft.mock', 'pass123')
        rec2_user.first_name = 'Ananya'
        rec2_user.last_name = 'Sen'
        rec2_user.save()
        rec2_profile = UserProfile.objects.create(
            user=rec2_user,
            role='RECRUITER',
            phone='+91 40 6695 0000',
            company_name='Microsoft IDC',
            company_website='https://careers.microsoft.com',
            company_sector='Enterprise Software & Cloud Platforms',
            designation='University Relations Specialist',
            company_address='Microsoft India Development Center, Hyderabad',
            company_logo='https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg',
            bio='Connecting university minds with cutting-edge Azure, AI, and developer tools.'
        )

        # Recruiter 3: Zomato / Blinkit
        rec3_user = User.objects.create_user('zomato_recruiter', 'kavita.nair@zomato.mock', 'pass123')
        rec3_user.first_name = 'Kavita'
        rec3_user.last_name = 'Nair'
        rec3_user.save()
        rec3_profile = UserProfile.objects.create(
            user=rec3_user,
            role='RECRUITER',
            phone='+91 124 412 7700',
            company_name='Zomato & Eternal Tech',
            company_website='https://www.zomato.com',
            company_sector='Hyperlocal Logistics & Consumer Tech',
            designation='Senior Tech Talent Partner',
            company_address='Golf Course Road, Sector 42, Gurugram',
            company_logo='https://upload.wikimedia.org/wikipedia/commons/7/75/Zomato_logo.png',
            bio='Seeking product engineers and machine learning practitioners who love high-scale systems.'
        )

        # 4. Students
        # Student 1: Rohan Verma (Strong in Python, Django, React, Git)
        s1_user = User.objects.create_user('student_rohan', 'rohan.v@student.edu', 'student123')
        s1_user.first_name = 'Rohan'
        s1_user.last_name = 'Verma'
        s1_user.save()
        s1_profile = UserProfile.objects.create(
            user=s1_user,
            role='STUDENT',
            phone='+91 99887 11223',
            roll_number='2022BCSE042',
            department='Computer Science & Engineering',
            graduation_year=2026,
            cgpa=8.85,
            resume_link='https://example.com/resumes/rohan_verma.pdf',
            github_link='https://github.com/rohan-tech',
            linkedin_link='https://linkedin.com/in/rohan-verma',
            bio='Full-Stack Enthusiast passionate about Django, microservices, and React application development.'
        )

        # Student 2: Priya Sharma (Strong in Cloud, Docker, DevOps, Linux)
        s2_user = User.objects.create_user('student_priya', 'priya.s@student.edu', 'student123')
        s2_user.first_name = 'Priya'
        s2_user.last_name = 'Sharma'
        s2_user.save()
        s2_profile = UserProfile.objects.create(
            user=s2_user,
            role='STUDENT',
            phone='+91 98112 33445',
            roll_number='2022BCSE015',
            department='Information Technology',
            graduation_year=2026,
            cgpa=9.20,
            resume_link='https://example.com/resumes/priya_sharma.pdf',
            github_link='https://github.com/priya-devops',
            linkedin_link='https://linkedin.com/in/priya-sharma-cloud',
            bio='Cloud & Infrastructure aspirant. Certified AWS Cloud Practitioner with expertise in Docker, Kubernetes and CI/CD.'
        )

        # Student 3: Amit Patel (AI/ML aspirant)
        s3_user = User.objects.create_user('student_amit', 'amit.p@student.edu', 'student123')
        s3_user.first_name = 'Amit'
        s3_user.last_name = 'Patel'
        s3_user.save()
        s3_profile = UserProfile.objects.create(
            user=s3_user,
            role='STUDENT',
            phone='+91 97766 55443',
            roll_number='2022BECE089',
            department='Electronics & Communication Engineering',
            graduation_year=2026,
            cgpa=7.95,
            resume_link='https://example.com/resumes/amit_patel.pdf',
            github_link='https://github.com/amit-ml',
            linkedin_link='https://linkedin.com/in/amit-patel-data',
            bio='Exploring Deep Learning, computer vision, and embedded edge systems.'
        )

        self.stdout.write(self.style.SUCCESS("Creating Skill Taxonomy..."))

        # Categories
        cat_prog = SkillCategory.objects.create(name='Programming & Core CS', icon='bi-code-square', description='Fundamental languages and problem solving')
        cat_web = SkillCategory.objects.create(name='Web & Mobile Engineering', icon='bi-window-desktop', description='Modern web frameworks, frontend and backend development')
        cat_cloud = SkillCategory.objects.create(name='Cloud, DevOps & Systems', icon='bi-cloud-check', description='Containerization, virtualization and orchestration')
        cat_ai = SkillCategory.objects.create(name='AI, ML & Data Science', icon='bi-cpu', description='Machine learning algorithms, neural nets, and statistical analysis')
        cat_soft = SkillCategory.objects.create(name='Soft Skills & Collaboration', icon='bi-people', description='Professional communication, teamwork and agile practices')

        # Skills
        sk_python = Skill.objects.create(name='Python', category=cat_prog, is_trending=True, industry_demand_index=96)
        sk_java = Skill.objects.create(name='Java', category=cat_prog, is_trending=False, industry_demand_index=88)
        sk_dsa = Skill.objects.create(name='Data Structures & Algorithms', category=cat_prog, is_trending=True, industry_demand_index=95)
        sk_git = Skill.objects.create(name='Git & Version Control', category=cat_prog, is_trending=True, industry_demand_index=90)

        sk_django = Skill.objects.create(name='Django Web Framework', category=cat_web, is_trending=True, industry_demand_index=86)
        sk_react = Skill.objects.create(name='React.js', category=cat_web, is_trending=True, industry_demand_index=94)
        sk_node = Skill.objects.create(name='Node.js', category=cat_web, is_trending=False, industry_demand_index=84)
        sk_sql = Skill.objects.create(name='SQL & Relational Databases', category=cat_web, is_trending=True, industry_demand_index=92)
        sk_rest = Skill.objects.create(name='REST API Architecture', category=cat_web, is_trending=True, industry_demand_index=91)

        sk_docker = Skill.objects.create(name='Docker Containerization', category=cat_cloud, is_trending=True, industry_demand_index=94)
        sk_k8s = Skill.objects.create(name='Kubernetes', category=cat_cloud, is_trending=True, industry_demand_index=90)
        sk_aws = Skill.objects.create(name='AWS Cloud Architecture', category=cat_cloud, is_trending=True, industry_demand_index=93)
        sk_linux = Skill.objects.create(name='Linux Systems & Shell', category=cat_cloud, is_trending=False, industry_demand_index=89)

        sk_ml = Skill.objects.create(name='Machine Learning (Scikit-Learn)', category=cat_ai, is_trending=True, industry_demand_index=92)
        sk_pytorch = Skill.objects.create(name='PyTorch Deep Learning', category=cat_ai, is_trending=True, industry_demand_index=93)
        sk_nlp = Skill.objects.create(name='Natural Language Processing / LLMs', category=cat_ai, is_trending=True, industry_demand_index=97)

        sk_agile = Skill.objects.create(name='Agile & Scrum Methodologies', category=cat_soft, is_trending=False, industry_demand_index=80)
        sk_comm = Skill.objects.create(name='Technical Communication', category=cat_soft, is_trending=False, industry_demand_index=85)

        self.stdout.write(self.style.SUCCESS("Mapping Student Skills..."))

        # Student 1 (Rohan) skills
        StudentSkill.objects.create(student=s1_profile, skill=sk_python, proficiency=5, is_verified=True, verified_by=tpo_profile, certificate_name='Python for Everybody (Specialization)')
        StudentSkill.objects.create(student=s1_profile, skill=sk_django, proficiency=4, is_verified=True, verified_by=tpo_profile, certificate_name='Django Full-Stack Certified Developer')
        StudentSkill.objects.create(student=s1_profile, skill=sk_react, proficiency=4, is_verified=False)
        StudentSkill.objects.create(student=s1_profile, skill=sk_rest, proficiency=4, is_verified=True, verified_by=tpo_profile)
        StudentSkill.objects.create(student=s1_profile, skill=sk_dsa, proficiency=4, is_verified=False)
        StudentSkill.objects.create(student=s1_profile, skill=sk_git, proficiency=4, is_verified=True, verified_by=tpo_profile)
        StudentSkill.objects.create(student=s1_profile, skill=sk_sql, proficiency=3, is_verified=False)
        StudentSkill.objects.create(student=s1_profile, skill=sk_docker, proficiency=2, is_verified=False)

        # Student 2 (Priya) skills
        StudentSkill.objects.create(student=s2_profile, skill=sk_docker, proficiency=5, is_verified=True, verified_by=tpo_profile, certificate_name='Certified Docker Associate')
        StudentSkill.objects.create(student=s2_profile, skill=sk_k8s, proficiency=4, is_verified=True, verified_by=tpo_profile, certificate_name='Kubernetes Hands-on Labs')
        StudentSkill.objects.create(student=s2_profile, skill=sk_aws, proficiency=4, is_verified=True, verified_by=tpo_profile, certificate_name='AWS Certified Solutions Architect Associate')
        StudentSkill.objects.create(student=s2_profile, skill=sk_linux, proficiency=5, is_verified=True, verified_by=tpo_profile)
        StudentSkill.objects.create(student=s2_profile, skill=sk_python, proficiency=3, is_verified=False)
        StudentSkill.objects.create(student=s2_profile, skill=sk_git, proficiency=5, is_verified=True, verified_by=tpo_profile)
        StudentSkill.objects.create(student=s2_profile, skill=sk_dsa, proficiency=3, is_verified=False)

        # Student 3 (Amit) skills
        StudentSkill.objects.create(student=s3_profile, skill=sk_python, proficiency=4, is_verified=False)
        StudentSkill.objects.create(student=s3_profile, skill=sk_ml, proficiency=4, is_verified=True, verified_by=tpo_profile, certificate_name='DeepLearning.AI Machine Learning Specialization')
        StudentSkill.objects.create(student=s3_profile, skill=sk_pytorch, proficiency=3, is_verified=False)
        StudentSkill.objects.create(student=s3_profile, skill=sk_sql, proficiency=3, is_verified=False)
        StudentSkill.objects.create(student=s3_profile, skill=sk_git, proficiency=3, is_verified=False)

        self.stdout.write(self.style.SUCCESS("Creating Opportunities (Internships & Placements)..."))

        # Opportunity 1: Google Software Engineering Intern
        opp1 = Opportunity.objects.create(
            company=rec1_profile,
            title='Software Engineering Intern (Summer 2026)',
            opportunity_type='INTERNSHIP',
            work_mode='HYBRID',
            location='Bengaluru, Karnataka',
            stipend_salary='₹1,10,000 / month',
            duration='3 Months (May - July 2026)',
            openings=8,
            min_cgpa=8.0,
            department_eligibility='B.Tech / M.Tech in CSE, IT, ECE (Penultimate Year)',
            description='Join Google engineering teams building next-generation distributed systems, web services, and developer tooling. As an intern, you will collaborate with seasoned software engineers to design, build, and deploy real-world features.',
            responsibilities='- Design and implement modular backend components and web APIs.\n- Write clean, maintainable, well-tested code following best engineering practices.\n- Participate in design reviews, standups, and architecture discussions.',
            perks='Pre-Placement Offer (PPO) opportunity, 1-on-1 mentorship by Senior Google Engineers, Free meals & transport',
            deadline=date.today() + timedelta(days=25),
            status='APPROVED'
        )
        OpportunitySkillRequirement.objects.create(opportunity=opp1, skill=sk_python, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp1, skill=sk_django, min_proficiency=3, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp1, skill=sk_dsa, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp1, skill=sk_git, min_proficiency=3, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp1, skill=sk_react, min_proficiency=3, is_mandatory=False)

        # Opportunity 2: Microsoft Cloud & DevOps Engineer Intern
        opp2 = Opportunity.objects.create(
            company=rec2_profile,
            title='Cloud Infrastructure & DevOps Intern',
            opportunity_type='INTERNSHIP',
            work_mode='HYBRID',
            location='Hyderabad / Remote',
            stipend_salary='₹80,000 / month',
            duration='6 Months',
            openings=5,
            min_cgpa=7.5,
            department_eligibility='All B.Tech / MCA branches',
            description='Work alongside Azure core teams to automate cloud deployment pipelines, container orchestration, and continuous security scanning across global data centers.',
            responsibilities='- Build automated CI/CD pipelines using Docker and Kubernetes.\n- Implement infrastructure-as-code and observability monitoring.\n- Ensure high availability and system reliability.',
            perks='PPO track for full-time FTE role, Microsoft Certification vouchers, Home office setup allowance',
            deadline=date.today() + timedelta(days=18),
            status='APPROVED'
        )
        OpportunitySkillRequirement.objects.create(opportunity=opp2, skill=sk_docker, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp2, skill=sk_k8s, min_proficiency=3, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp2, skill=sk_linux, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp2, skill=sk_aws, min_proficiency=3, is_mandatory=False)
        OpportunitySkillRequirement.objects.create(opportunity=opp2, skill=sk_git, min_proficiency=3, is_mandatory=True)

        # Opportunity 3: Zomato AI & Data Science Intern
        opp3 = Opportunity.objects.create(
            company=rec3_profile,
            title='AI & Machine Learning Engineering Intern',
            opportunity_type='INTERNSHIP',
            work_mode='ON_SITE',
            location='Gurugram, Haryana',
            stipend_salary='₹50,000 / month',
            duration='6 Months',
            openings=4,
            min_cgpa=7.0,
            department_eligibility='B.Tech / M.Tech in CS, IT, ECE, Mathematics & Computing',
            description='Help optimize recommendation engines, ETA prediction models, and dynamic catalog intelligence handling millions of orders daily across India.',
            responsibilities='- Train and fine-tune machine learning and deep learning models.\n- Build data pipelines for real-time feature extraction.\n- Deploy REST APIs serving predictions at sub-50ms latency.',
            perks='Free Gourmet Lunch, Subsidized dining credits, fast-track full-time offer',
            deadline=date.today() + timedelta(days=14),
            status='APPROVED'
        )
        OpportunitySkillRequirement.objects.create(opportunity=opp3, skill=sk_python, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp3, skill=sk_ml, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp3, skill=sk_pytorch, min_proficiency=3, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp3, skill=sk_sql, min_proficiency=3, is_mandatory=True)

        # Opportunity 4: Full-Time Campus Placement (Microsoft)
        opp4 = Opportunity.objects.create(
            company=rec2_profile,
            title='Software Engineer - Campus Placement (Class of 2026)',
            opportunity_type='PLACEMENT',
            work_mode='HYBRID',
            location='Bengaluru / Hyderabad',
            stipend_salary='₹24.5 - ₹28 LPA (CTC)',
            duration='Permanent Full-Time',
            openings=12,
            min_cgpa=8.0,
            department_eligibility='B.Tech / Dual Degree CSE & IT',
            description='Microsoft University Hiring drive for graduating seniors. Join engineering teams building Windows, Azure, Office 365, and AI Copilot integrations.',
            responsibilities='- Build scalable enterprise solutions with high availability.\n- Collaborate across international teams and customer engineering groups.',
            perks='Stock Grants (RSUs), Comprehensive Health Cover, Annual Wellness Bonus',
            deadline=date.today() + timedelta(days=35),
            status='APPROVED'
        )
        OpportunitySkillRequirement.objects.create(opportunity=opp4, skill=sk_dsa, min_proficiency=4, is_mandatory=True)
        OpportunitySkillRequirement.objects.create(opportunity=opp4, skill=sk_python, min_proficiency=3, is_mandatory=False)
        OpportunitySkillRequirement.objects.create(opportunity=opp4, skill=sk_git, min_proficiency=4, is_mandatory=True)

        self.stdout.write(self.style.SUCCESS("Creating Applications with match calculations..."))

        # Application 1: Rohan applied to Google Intern
        match1, _, _ = opp1.calculate_student_match(s1_profile)
        Application.objects.create(
            opportunity=opp1,
            student=s1_profile,
            match_score=match1,
            cover_letter="I have built 3 production-grade full-stack web applications using Django and React. I have consistently practiced algorithmic problem solving on LeetCode (300+ problems). I am eager to contribute to Google Cloud's core web services.",
            portfolio_url="https://rohan-portfolio.dev",
            status='INTERVIEW_SCHEDULED',
            interview_date=timezone.now() + timedelta(days=3, hours=4),
            interview_link='https://meet.google.com/xyz-abcd-uvw',
            recruiter_notes="Strong algorithmic foundation and excellent Django project showcase. Scheduled for Technical Round 1."
        )

        # Application 2: Priya applied to Microsoft DevOps Intern
        match2, _, _ = opp2.calculate_student_match(s2_profile)
        Application.objects.create(
            opportunity=opp2,
            student=s2_profile,
            match_score=match2,
            cover_letter="I am an AWS Certified Solutions Architect Associate with practical experience in Kubernetes cluster administration, automated CI/CD using GitHub Actions, and Linux kernel fundamentals.",
            portfolio_url="https://priyasharma.io",
            status='OFFERED',
            recruiter_notes="Exceptional candidate! 100% skill alignment on Docker, K8s, and Cloud Architecture. Extended Offer for Summer 2026."
        )

        # Application 3: Amit applied to Zomato AI Intern
        match3, _, _ = opp3.calculate_student_match(s3_profile)
        Application.objects.create(
            opportunity=opp3,
            student=s3_profile,
            match_score=match3,
            cover_letter="Worked on computer vision and neural model fine-tuning. Passionate about applying PyTorch to high-throughput recommendation systems.",
            portfolio_url="https://github.com/amit-ml",
            status='SHORTLISTED',
            recruiter_notes="High academic score in Deep Learning. Moving to coding assessment."
        )

        # Application 4: Rohan applied to Microsoft Full-Time Placement
        match4, _, _ = opp4.calculate_student_match(s1_profile)
        Application.objects.create(
            opportunity=opp4,
            student=s1_profile,
            match_score=match4,
            cover_letter="Final-year student with proven problem solving and full-stack software development experience.",
            status='APPLIED'
        )

        self.stdout.write(self.style.SUCCESS("Creating Collaboration Projects & Curriculum Feedback..."))

        # Collaboration Project 1
        CollaborationProject.objects.create(
            title='Autonomous Delivery Fleet Routing Optimization',
            industry_partner=rec3_profile,
            faculty_mentor=tpo_profile,
            project_type='INDUSTRY_RND',
            description='Joint research challenge between Zomato Data Labs and University Department of Computer Science to optimize multi-vehicle delivery routes under real-time urban traffic constraints.',
            expected_outcomes='- Working PyTorch / Reinforcement Learning prototype.\n- Joint research paper submission to IEEE / ACM conference.\n- Internship offers for top student contributors.',
            stipend_grant='₹1,50,000 Research Grant & Cloud Computing Credits',
            team_size_limit=4,
            status='IN_PROGRESS',
            deadline=date.today() + timedelta(days=90)
        )

        # Collaboration Project 2
        CollaborationProject.objects.create(
            title='Cloud-Native Microservices Security Sandbox',
            industry_partner=rec2_profile,
            faculty_mentor=tpo_profile,
            project_type='CAPSTONE',
            description='Final year capstone project sponsored by Microsoft Azure Security team. Students will build eBPF-based container runtime intrusion detection modules.',
            expected_outcomes='Open-source GitHub repository and deployment on Azure Kubernetes Service (AKS).',
            stipend_grant='₹60,000 Project Stipend',
            team_size_limit=3,
            status='PROPOSED',
            deadline=date.today() + timedelta(days=120)
        )

        # Curriculum Feedback 1
        CurriculumFeedback.objects.create(
            industry_partner=rec1_profile,
            course_name='CS304: Database Management Systems',
            department='Computer Science & Engineering',
            observed_industry_gap='Students are well-versed in theoretical relational algebra and normalized SQL tables, but lack hands-on experience with modern distributed key-value stores, caching layers (Redis), and vector databases for AI embeddings.',
            proposed_technologies='Add 2 lab sessions on Redis caching architectures and Pinecone / pgvector indexing for search engines.',
            academic_response='Accepted by Department Curriculum Committee. Added 3 new lab experiments on Redis & PostgreSQL pgvector for 2026-27 batch.',
            status='ACCEPTED'
        )

        # Curriculum Feedback 2
        CurriculumFeedback.objects.create(
            industry_partner=rec2_profile,
            course_name='CS401: Software Engineering Practices',
            department='Information Technology',
            observed_industry_gap='Need more hands-on emphasis on automated CI/CD pipelines, containerization (Docker), and Infrastructure as Code rather than purely waterfall documentation.',
            proposed_technologies='Integrate GitHub Actions, Docker multi-stage builds, and basic Terraform scripts into mandatory term projects.',
            academic_response='Under evaluation by Board of Studies. Pilot being introduced in Section A this semester.',
            status='UNDER_EVALUATION'
        )

        # Active Industry MoUs
        IndustryMoU.objects.create(
            company_name='Google India Private Limited',
            contact_person='Sundar Ramaswamy (Lead Campus Talent Partner)',
            email='campus-relations@google.mock',
            signing_date=date(2025, 7, 15),
            valid_upto=date(2028, 7, 14),
            focus_areas='Direct Campus Hiring, Summer Internships, Google Cloud Certification Credits, Faculty Development Programs',
            is_active=True
        )

        IndustryMoU.objects.create(
            company_name='Microsoft Corporation India',
            contact_person='Ananya Sen (University Relations Specialist)',
            email='university-india@microsoft.mock',
            signing_date=date(2024, 11, 1),
            valid_upto=date(2027, 10, 31),
            focus_areas='Student Mentorship, Capstone Project Sponsorship, Azure Cloud Labs, Hackathons',
            is_active=True
        )

        IndustryMoU.objects.create(
            company_name='Zomato Media Pvt. Ltd.',
            contact_person='Kavita Nair (Senior Tech Recruiter)',
            email='campus-tech@zomato.mock',
            signing_date=date(2025, 1, 10),
            valid_upto=date(2027, 1, 9),
            focus_areas='AI/ML Research Internships, Guest Lectures, Hackathon Sponsorship',
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS("Demo database successfully initialized with rich test data!"))
