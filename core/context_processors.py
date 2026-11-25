def user_profile_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {'user_profile': request.user.profile}
    return {'user_profile': None}
