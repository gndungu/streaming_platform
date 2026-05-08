from datetime import timedelta
from django.contrib.sessions.models import Session
from django.utils import timezone

from apps.accounts.models import UserSession


# Session middleware to enforce one session
class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Get current session key
            current_session_key = request.session.session_key
            
            # Get all other active sessions for this user
            other_sessions = UserSession.objects.filter(
                user=request.user
            ).exclude(
                session_key=current_session_key
            )
            
            # Delete other sessions
            for session in other_sessions:
                # Delete Django session
                Session.objects.filter(session_key=session.session_key).delete()
                # Delete our record
                session.delete()
            
            # Create/update current session record
            UserSession.objects.update_or_create(
                session_key=current_session_key,
                defaults={
                    'user': request.user,
                    'ip_address': self.get_client_ip(request),
                    'user_agent': request.META.get('HTTP_USER_AGENT', '')[:1000],
                    'expires_at': timezone.now() + timedelta(days=7),
                }
            )
        
        return self.get_response(request)



