from main_app.models import Profile
from django.contrib.auth.models import User
from datetime import datetime


def profile_context(request):
    test = None
    date = datetime.now()
    todayDay = date.day
    todayMonth = date.month
    todayYear = date.year
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user)
        if len(profile):
            return {'profile': profile[0], 'curDay': todayDay, 'curMonth': todayMonth, 'curYear': todayYear}
        else: return {'profile': test, 'curDay': todayDay, 'curMonth': todayMonth, 'curYear': todayYear}
    else:
        return {'profile': test}