import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SkillCategory, Skill, StudentSkill
from .forms import AddStudentSkillForm
from internships.models import Opportunity
from core.models import UserProfile

def skills_catalog(request):
    categories = SkillCategory.objects.prefetch_related('skills').all()
    q = request.GET.get('q', '')
    if q:
        filtered_skills = Skill.objects.filter(name__icontains=q).select_related('category')
    else:
        filtered_skills = None

    context = {
        'categories': categories,
        'filtered_skills': filtered_skills,
        'query': q,
    }
    return render(request, 'skills/catalog.html', context)


@login_required
def my_skills(request):
    profile = request.user.profile
    if not profile.is_student:
        messages.warning(request, "Skill profile management is for students.")
        return redirect('dashboard')

    skills = StudentSkill.objects.filter(student=profile).select_related('skill', 'skill__category')
    form = AddStudentSkillForm()

    context = {
        'student_skills': skills,
        'form': form,
    }
    return render(request, 'skills/my_skills.html', context)


@login_required
def add_student_skill(request):
    profile = request.user.profile
    if not profile.is_student:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AddStudentSkillForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            proficiency = form.cleaned_data['proficiency']
            cert_name = form.cleaned_data['certificate_name']
            cert_url = form.cleaned_data['certificate_url']

            student_skill, created = StudentSkill.objects.update_or_create(
                student=profile,
                skill=skill,
                defaults={
                    'proficiency': proficiency,
                    'certificate_name': cert_name,
                    'certificate_url': cert_url,
                    'is_verified': False  # requires re-verification on update
                }
            )
            action = "added" if created else "updated"
            messages.success(request, f"Skill '{skill.name}' successfully {action}!")
        else:
            messages.error(request, "Please check the form fields.")
    return redirect('my_skills')


@login_required
def delete_student_skill(request, pk):
    profile = request.user.profile
    skill_entry = get_object_or_404(StudentSkill, pk=pk, student=profile)
    skill_name = skill_entry.skill.name
    skill_entry.delete()
    messages.info(request, f"Skill '{skill_name}' removed from your profile.")
    return redirect('my_skills')


@login_required
def skill_gap_analysis(request, opportunity_id=None):
    profile = request.user.profile
    approved_opps = Opportunity.objects.filter(status='APPROVED').prefetch_related('skill_requirements')
    
    selected_opp = None
    if opportunity_id:
        selected_opp = get_object_or_404(Opportunity, pk=opportunity_id)
    elif approved_opps.exists():
        selected_opp = approved_opps.first()

    match_score = 0
    matching_skills = []
    missing_skills = []
    radar_data = {'labels': [], 'required': [], 'student': []}

    if selected_opp:
        match_score, matching_skills, missing_skills = selected_opp.calculate_student_match(profile)

        # Prepare Radar chart dataset
        for req in selected_opp.skill_requirements.all():
            radar_data['labels'].append(req.skill.name)
            radar_data['required'].append(req.min_proficiency)
            
            # Find student's proficiency for this skill
            st_skill = StudentSkill.objects.filter(student=profile, skill=req.skill).first()
            radar_data['student'].append(st_skill.proficiency if st_skill else 0)

    context = {
        'opportunities': approved_opps,
        'selected_opp': selected_opp,
        'match_score': match_score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'radar_json': json.dumps(radar_data),
    }
    return render(request, 'skills/gap_analysis.html', context)


@login_required
def verify_student_skill(request, pk):
    profile = request.user.profile
    if not profile.is_faculty_tpo:
        messages.error(request, "Only Faculty or TPO can verify skills.")
        return redirect('dashboard')

    student_skill = get_object_or_404(StudentSkill, pk=pk)
    student_skill.is_verified = True
    student_skill.verified_by = profile
    student_skill.save()
    messages.success(request, f"Verified skill '{student_skill.skill.name}' for {student_skill.student.user.get_full_name()}!")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


import re

@login_required
def extract_skills_from_resume(request):
    profile = request.user.profile
    if not profile.is_student:
        return redirect('dashboard')

    extracted_skills = []
    resume_text = ""

    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '')
        # Handle bulk addition of detected skills
        if 'add_detected' in request.POST:
            selected_skill_ids = request.POST.getlist('selected_skills')
            default_prof = int(request.POST.get('default_proficiency', 3))
            added_count = 0
            for sk_id in selected_skill_ids:
                sk = Skill.objects.filter(pk=sk_id).first()
                if sk:
                    StudentSkill.objects.get_or_create(
                        student=profile,
                        skill=sk,
                        defaults={'proficiency': default_prof, 'is_verified': False}
                    )
                    added_count += 1
            messages.success(request, f"Successfully mapped {added_count} extracted skills to your profile!")
            return redirect('my_skills')

        if resume_text:
            text_lower = resume_text.lower()
            all_skills = Skill.objects.select_related('category').all()
            user_skill_ids = set(StudentSkill.objects.filter(student=profile).values_list('skill_id', flat=True))

            for sk in all_skills:
                # Regex match for whole word / token
                pattern = r'\b' + re.escape(sk.name.lower()) + r'\b'
                # Also check common shorthand/synonyms (e.g., k8s for kubernetes, ml for machine learning)
                synonyms = []
                if 'kubernetes' in sk.name.lower():
                    synonyms.append('k8s')
                elif 'machine learning' in sk.name.lower():
                    synonyms.append('ml')
                elif 'react' in sk.name.lower():
                    synonyms.append('react')

                found = bool(re.search(pattern, text_lower))
                if not found:
                    for syn in synonyms:
                        if re.search(r'\b' + re.escape(syn) + r'\b', text_lower):
                            found = True
                            break

                if found:
                    extracted_skills.append({
                        'skill': sk,
                        'already_added': sk.id in user_skill_ids
                    })

    return render(request, 'skills/resume_extractor.html', {
        'resume_text': resume_text,
        'extracted_skills': extracted_skills,
    })
