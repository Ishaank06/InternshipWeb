from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CollaborationProject, CurriculumFeedback, IndustryMoU
from .forms import CollaborationProjectForm, CurriculumFeedbackForm

def collaboration_hub(request):
    projects = CollaborationProject.objects.select_related('industry_partner', 'faculty_mentor').all()
    mous = IndustryMoU.objects.filter(is_active=True)
    feedbacks = CurriculumFeedback.objects.select_related('industry_partner').order_by('-created_at')

    context = {
        'projects': projects,
        'mous': mous,
        'feedbacks': feedbacks,
    }
    return render(request, 'collaboration/hub.html', context)


@login_required
def propose_project(request):
    profile = request.user.profile
    if profile.is_student:
        messages.error(request, "Joint projects can only be proposed by Industry Partners or Faculty.")
        return redirect('collaboration_hub')

    if request.method == 'POST':
        form = CollaborationProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            if profile.is_recruiter:
                project.industry_partner = profile
            else:
                project.faculty_mentor = profile
                # Assign default industry partner if faculty proposed
                first_rec = UserProfile.objects.filter(role='RECRUITER').first()
                project.industry_partner = first_rec
            project.save()
            messages.success(request, f"Collaboration Project '{project.title}' proposed successfully!")
            return redirect('collaboration_hub')
    else:
        form = CollaborationProjectForm()

    return render(request, 'collaboration/propose_project.html', {'form': form})


@login_required
def submit_curriculum_feedback(request):
    profile = request.user.profile
    if not profile.is_recruiter:
        messages.error(request, "Curriculum recommendations are submitted by industry recruiters.")
        return redirect('collaboration_hub')

    if request.method == 'POST':
        form = CurriculumFeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.industry_partner = profile
            fb.status = 'PENDING_REVIEW'
            fb.save()
            messages.success(request, f"Curriculum recommendation for '{fb.course_name}' submitted to the Board of Studies!")
            return redirect('collaboration_hub')
    else:
        form = CurriculumFeedbackForm()

    return render(request, 'collaboration/curriculum_feedback.html', {'form': form})


@login_required
def update_feedback_status(request, pk):
    profile = request.user.profile
    if not profile.is_faculty_tpo:
        messages.error(request, "Only Faculty / TPO can review curriculum feedback.")
        return redirect('collaboration_hub')

    fb = get_object_or_404(CurriculumFeedback, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        academic_response = request.POST.get('academic_response', '')
        if status:
            fb.status = status
        fb.academic_response = academic_response
        fb.save()
        messages.success(request, f"Curriculum feedback updated for {fb.course_name}!")
    return redirect('collaboration_hub')
