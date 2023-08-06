import getpass
import pytz

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone


def login_user(get_response):
    def middleware(request):
        if not request.user.is_authenticated:
            username = getpass.getuser()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_superuser(username)
            login(request, user)
        response = get_response(request)
        return response
    return middleware


def activate_timezone(get_response):
    def middleware(request):
        timezone.activate(pytz.timezone('US/Pacific'))
        response = get_response(request)
        return response
    return middleware
