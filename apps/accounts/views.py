from django.shortcuts import render
from django.contrib.auth import login as auth_login

from apps.content.models import UserSession


def login(request, user):
    # Delete all existing sessions for this user
    UserSession.objects.filter(user=user).delete()
    # Delete Django session records
    Session.objects.filter(
        session_key__in=UserSession.objects.filter(user=user).values('session_key')
    ).delete()
    
    # Perform normal login
    auth_login(request, user)
