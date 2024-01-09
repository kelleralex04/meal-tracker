from main_app.models import Profile
from django.contrib.auth.models import User


def profile_context(request):
    test = None
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user)
        if len(profile):
            return {'profile': profile[0]}
        else: return {'test': test}
    else:
        return {'profile': test}