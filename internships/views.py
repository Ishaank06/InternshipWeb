from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Opportunity, OpportunitySkillRequirement, Application
from .forms import OpportunityForm, ApplicationForm, ApplicationReviewForm
from skills.models import Skill, StudentSkill

def opportunity_list(request):
    opps = Opportunity.objects.filter(status='APPROVED').select_related('company')

    # Filtering
    opp_type = request.GET.get('type')
    work_mode = request.GET.get('mode')
    q = request.GET.get('q')

    if opp_type:
        opps = opps.filter(opportunity_type=opp_type)
    if work_mode:
        opps = opps.filter(work_mode=work_mode)
    if q:
        opps = opps.filter(Q(title__icontains=q) | Q(company__company_name__icontains=q) | Q(description__icontains=q))

    # Match scores for logged-in students
    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_student:
        student_profile = request.user.profile

    items = []
    for opp in opps:
        match_score = None
        has_applied = False
        if student_profile:
            match_score, _, _ = opp.calculate_student_match(student_profile)
            has_applied = Application.objects.filter(opportunity=opp, student=student_profile).exists()
        items.append({
            'opp': opp,
            'match_score': match_score,
            'has_applied': has_applied
        })

    context = {
        'items': items,
        'selected_type': opp_type,
        'selected_mode': work_mode,
        'query': q,
    }
    return render(request, 'internships/opportunity_list.html', context)


def opportunity_detail(request, pk):
    opp = get_object_or_404(Opportunity.objects.select_related('company'), pk=pk)
    reqs = opp.skill_requirements.select_related('skill').all()

    student_profile = None
    match_score = None
    matching_skills = []
    missing_skills = []
    has_applied = False
    application = None

    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_student:
        student_profile = request.user.profile
        match_score, matching_skills, missing_skills = opp.calculate_student_match(student_profile)
        application = Application.objects.filter(opportunity=opp, student=student_profile).first()
        has_applied = application is not None

    app_form = ApplicationForm()

    context = {
        'opp': opp,
        'reqs': reqs,
        'match_score': match_score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'has_applied': has_applied,
        'application': application,
        'app_form': app_form,
    }
    return render(request, 'internships/opportunity_detail.html', context)


@login_required
def post_opportunity(request):
    profile = request.user.profile
    if not (profile.is_recruiter or profile.is_faculty_tpo):
        messages.error(request, "Only recruiters or TPO can post opportunities.")
        return redirect('dashboard')

    skills = Skill.objects.all().order_by('category__name', 'name')

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opp = form.save(commit=False)
            opp.company = profile
            # If posted by TPO, auto-approve; if posted by recruiter, approve directly or pending
            opp.status = 'APPROVED'
            opp.save()

            # Process skill requirements from form
            selected_skills = request.POST.getlist('skills')
            for skill_id in selected_skills:
                min_prof = request.POST.get(f'prof_{skill_id}', 3)
                is_mand = request.POST.get(f'mandatory_{skill_id}') == 'on'
                sk = Skill.objects.get(pk=skill_id)
                OpportunitySkillRequirement.objects.create(
                    opportunity=opp,
                    skill=sk,
                    min_proficiency=int(min_prof),
                    is_mandatory=is_mand
                )

            messages.success(request, f"Opportunity '{opp.title}' posted successfully!")
            return redirect('opportunity_detail', pk=opp.pk)
    else:
        form = OpportunityForm()

    return render(request, 'internships/post_opportunity.html', {'form': form, 'skills': skills})


@login_required
def apply_opportunity(request, pk):
    profile = request.user.profile
    if not profile.is_student:
        messages.error(request, "Only students can apply to opportunities.")
        return redirect('dashboard')

    opp = get_object_or_404(Opportunity, pk=pk)
    if opp.status != 'APPROVED':
        messages.error(request, "This opportunity is not currently open for applications.")
        return redirect('opportunity_detail', pk=pk)

    if Application.objects.filter(opportunity=opp, student=profile).exists():
        messages.warning(request, "You have already applied for this position.")
        return redirect('opportunity_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.opportunity = opp
            app.student = profile
            match_score, _, _ = opp.calculate_student_match(profile)
            app.match_score = match_score
            app.status = 'APPLIED'
            app.save()

            messages.success(request, f"Your application for '{opp.title}' has been submitted! Match Score: {match_score}%")
            return redirect('my_applications')
    return redirect('opportunity_detail', pk=pk)


@login_required
def my_applications(request):
    profile = request.user.profile
    if not profile.is_student:
        return redirect('dashboard')

    apps = Application.objects.filter(student=profile).select_related('opportunity', 'opportunity__company').order_by('-applied_at')
    return render(request, 'internships/my_applications.html', {'applications': apps})


@login_required
def manage_applications(request, opportunity_id=None):
    profile = request.user.profile
    if not (profile.is_recruiter or profile.is_faculty_tpo):
        messages.error(request, "Access restricted to recruiters and TPO.")
        return redirect('dashboard')

    if profile.is_recruiter:
        opportunities = Opportunity.objects.filter(company=profile)
    else:
        opportunities = Opportunity.objects.all()

    selected_opp = None
    if opportunity_id:
        selected_opp = get_object_or_404(Opportunity, pk=opportunity_id)
        applications = Application.objects.filter(opportunity=selected_opp).select_related('student', 'student__user')
    else:
        if opportunities.exists():
            selected_opp = opportunities.first()
            applications = Application.objects.filter(opportunity=selected_opp).select_related('student', 'student__user')
        else:
            applications = Application.objects.none()

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    applications = applications.order_by('-match_score', '-applied_at')

    context = {
        'opportunities': opportunities,
        'selected_opp': selected_opp,
        'applications': applications,
        'status_filter': status_filter,
    }
    return render(request, 'internships/manage_applications.html', context)


@login_required
def update_application_status(request, pk):
    profile = request.user.profile
    if not (profile.is_recruiter or profile.is_faculty_tpo):
        return redirect('dashboard')

    app = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        interview_link = request.POST.get('interview_link', '')
        interview_date = request.POST.get('interview_date')
        notes = request.POST.get('recruiter_notes', '')

        if new_status:
            app.status = new_status
        app.interview_link = interview_link
        if interview_date:
            app.interview_date = interview_date
        app.recruiter_notes = notes
        app.save()

        messages.success(request, f"Updated application status for {app.student.user.get_full_name()} to '{app.get_status_display()}'")
    return redirect('manage_applications', opportunity_id=app.opportunity.id)


@login_required
def tpo_approve_opportunity(request, pk):
    profile = request.user.profile
    if not profile.is_faculty_tpo:
        messages.error(request, "Only TPO can approve drives.")
        return redirect('dashboard')

    opp = get_object_or_404(Opportunity, pk=pk)
    action = request.POST.get('action')
    if action == 'approve':
        opp.status = 'APPROVED'
        messages.success(request, f"Opportunity '{opp.title}' approved and published.")
    elif action == 'close':
        opp.status = 'CLOSED'
        messages.info(request, f"Opportunity '{opp.title}' closed.")
    opp.save()
    return redirect('dashboard')
