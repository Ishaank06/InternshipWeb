from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileUpdateForm
from skills.models import Skill, StudentSkill, SkillCategory
from internships.models import Opportunity, Application
from collaboration.models import CollaborationProject, CurriculumFeedback, IndustryMoU

def home(request):
    total_students = UserProfile.objects.filter(role='STUDENT').count()
    total_recruiters = UserProfile.objects.filter(role='RECRUITER').count()
    total_opportunities = Opportunity.objects.filter(status='APPROVED').count()
    total_mous = IndustryMoU.objects.filter(is_active=True).count()
    total_placed = Application.objects.filter(status='OFFERED').count()

    recent_opportunities = Opportunity.objects.filter(status='APPROVED').select_related('company')[:4]
    trending_skills = Skill.objects.filter(is_trending=True)[:8]
    collab_projects = CollaborationProject.objects.all()[:3]

    context = {
        'total_students': total_students,
        'total_recruiters': total_recruiters,
        'total_opportunities': total_opportunities,
        'total_mous': total_mous,
        'total_placed': total_placed,
        'recent_opportunities': recent_opportunities,
        'trending_skills': trending_skills,
        'collab_projects': collab_projects,
    }
    return render(request, 'core/home.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # Check for demo login button click
        demo_user = request.POST.get('demo_user')
        if demo_user:
            user = User.objects.filter(username=demo_user).first()
            if user:
                login(request, user)
                messages.success(request, f"Logged in as demo user: {user.get_full_name() or user.username} ({user.profile.get_role_display()})")
                return redirect('dashboard')

        # Standard login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            role = form.cleaned_data['role']
            UserProfile.objects.create(
                user=user,
                role=role,
                department=form.cleaned_data.get('department', ''),
                company_name=form.cleaned_data.get('company_name', '')
            )
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile:
        profile = UserProfile.objects.create(user=request.user, role='STUDENT')

    if profile.is_student:
        return student_dashboard(request, profile)
    elif profile.is_recruiter:
        return recruiter_dashboard(request, profile)
    else:
        return tpo_dashboard(request, profile)


def student_dashboard(request, profile):
    student_skills = StudentSkill.objects.filter(student=profile).select_related('skill', 'skill__category')
    applications = Application.objects.filter(student=profile).select_related('opportunity', 'opportunity__company')
    
    # Calculate recommended opportunities based on skill match
    approved_opps = Opportunity.objects.filter(status='APPROVED').prefetch_related('skill_requirements', 'skill_requirements__skill')
    recommendations = []
    for opp in approved_opps:
        score, matching, missing = opp.calculate_student_match(profile)
        # Check if already applied
        has_applied = applications.filter(opportunity=opp).exists()
        recommendations.append({
            'opportunity': opp,
            'match_score': score,
            'matching_count': len(matching),
            'missing_count': len(missing),
            'has_applied': has_applied
        })
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)

    # Key statistics
    skill_count = student_skills.count()
    verified_count = student_skills.filter(is_verified=True).count()
    applied_count = applications.count()
    interviews_count = applications.filter(status='INTERVIEW_SCHEDULED').count()
    offers_count = applications.filter(status='OFFERED').count()

    # Skill Readiness Index: Average proficiency / 5 * 100
    avg_prof = student_skills.aggregate(Avg('proficiency'))['proficiency__avg'] or 0
    readiness_index = int((avg_prof / 5.0) * 100)

    context = {
        'profile': profile,
        'student_skills': student_skills,
        'applications': applications[:5],
        'recommendations': recommendations[:4],
        'skill_count': skill_count,
        'verified_count': verified_count,
        'applied_count': applied_count,
        'interviews_count': interviews_count,
        'offers_count': offers_count,
        'readiness_index': readiness_index,
    }
    return render(request, 'core/student_dashboard.html', context)


def recruiter_dashboard(request, profile):
    opportunities = Opportunity.objects.filter(company=profile).prefetch_related('applications')
    total_postings = opportunities.count()
    total_applicants = Application.objects.filter(opportunity__company=profile).count()
    shortlisted_count = Application.objects.filter(opportunity__company=profile, status='SHORTLISTED').count()
    interview_count = Application.objects.filter(opportunity__company=profile, status='INTERVIEW_SCHEDULED').count()
    hired_count = Application.objects.filter(opportunity__company=profile, status='OFFERED').count()

    recent_applications = Application.objects.filter(opportunity__company=profile).select_related('student', 'student__user', 'opportunity').order_by('-applied_at')[:8]
    curriculum_feedbacks = CurriculumFeedback.objects.filter(industry_partner=profile)

    context = {
        'profile': profile,
        'opportunities': opportunities,
        'total_postings': total_postings,
        'total_applicants': total_applicants,
        'shortlisted_count': shortlisted_count,
        'interview_count': interview_count,
        'hired_count': hired_count,
        'recent_applications': recent_applications,
        'curriculum_feedbacks': curriculum_feedbacks,
    }
    return render(request, 'core/recruiter_dashboard.html', context)


def tpo_dashboard(request, profile):
    total_students = UserProfile.objects.filter(role='STUDENT').count()
    total_placed = Application.objects.filter(status='OFFERED').values('student').distinct().count()
    placement_rate = int((total_placed / total_students) * 100) if total_students > 0 else 0
    active_mous = IndustryMoU.objects.filter(is_active=True).count()
    pending_approvals = Opportunity.objects.filter(status='PENDING')
    approved_opportunities = Opportunity.objects.filter(status='APPROVED').count()

    # Skill demand summary
    top_demanded_skills = Skill.objects.all().order_by('-industry_demand_index')[:6]
    recent_feedbacks = CurriculumFeedback.objects.all().order_by('-created_at')[:5]
    recent_applications = Application.objects.all().select_related('student', 'opportunity', 'opportunity__company').order_by('-applied_at')[:6]

    context = {
        'profile': profile,
        'total_students': total_students,
        'total_placed': total_placed,
        'placement_rate': placement_rate,
        'active_mous': active_mous,
        'pending_approvals': pending_approvals,
        'approved_opportunities': approved_opportunities,
        'top_demanded_skills': top_demanded_skills,
        'recent_feedbacks': recent_feedbacks,
        'recent_applications': recent_applications,
    }
    return render(request, 'core/tpo_dashboard.html', context)


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Update user fields
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'core/profile.html', {'form': form, 'profile': profile})


@login_required
def institutional_analytics(request):
    """Accreditation (NAAC/NBA/NIRF) & Placement Analytics Dashboard"""
    total_students = UserProfile.objects.filter(role='STUDENT').count()
    placed_students = Application.objects.filter(status='OFFERED').values('student').distinct().count()
    placement_rate = int((placed_students / total_students) * 100) if total_students > 0 else 0

    # Skill readiness across departments
    dept_stats = []
    departments = ['Computer Science & Engineering', 'Information Technology', 'Electronics & Communication Engineering']
    for dept in departments:
        count = UserProfile.objects.filter(role='STUDENT', department=dept).count()
        placed = Application.objects.filter(status='OFFERED', student__department=dept).values('student').distinct().count()
        rate = int((placed / count) * 100) if count > 0 else 0
        dept_stats.append({'name': dept, 'total': count, 'placed': placed, 'rate': rate})

    # Industry demand vs student average proficiency
    skills = Skill.objects.all().annotate(student_count=Count('student_skills'))[:7]
    skill_comparison = []
    for sk in skills:
        avg_student_prof = StudentSkill.objects.filter(skill=sk).aggregate(Avg('proficiency'))['proficiency__avg'] or 0
        skill_comparison.append({
            'name': sk.name,
            'demand_index': sk.industry_demand_index,
            'student_avg_pct': int((avg_student_prof / 5.0) * 100),
        })

    context = {
        'total_students': total_students,
        'placed_students': placed_students,
        'placement_rate': placement_rate,
        'dept_stats': dept_stats,
        'skill_comparison': skill_comparison,
        'mous': IndustryMoU.objects.all(),
        'curriculum_feedbacks': CurriculumFeedback.objects.all(),
    }
    return render(request, 'core/analytics.html', context)


import csv
from django.http import HttpResponse

@login_required
def export_placement_csv(request):
    """Generates and downloads a CSV report for TPO and NAAC accreditation audits."""
    if not request.user.profile.is_faculty_tpo:
        messages.error(request, "Only TPO / Faculty can export placement records.")
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="placement_accreditation_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Roll Number', 'Department', 'CGPA', 'Opportunity Title', 'Company', 'Package/Stipend', 'Match Score (%)', 'Status', 'Applied Date'])

    applications = Application.objects.select_related('student', 'student__user', 'opportunity', 'opportunity__company').all().order_by('-applied_at')
    for app in applications:
        writer.writerow([
            app.student.user.get_full_name() or app.student.user.username,
            app.student.roll_number,
            app.student.department,
            app.student.cgpa,
            app.opportunity.title,
            app.opportunity.company.company_name or app.opportunity.company.user.username,
            app.opportunity.stipend_salary,
            app.match_score,
            app.get_status_display(),
            app.applied_at.strftime('%Y-%m-%d')
        ])

    return response
