
class StreamingAccessMiddleware:
    """
    Check if user can access content before streaming starts
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only check streaming endpoints
        if request.path.startswith('/api/stream/'):
            # Extract content from URL
            content_type = request.resolver_match.kwargs.get('content_type')
            content_id = request.resolver_match.kwargs.get('content_id')
            
            user = request.user
            
            if not user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Check if user is banned
            if user.is_banned:
                return JsonResponse({'error': f'Account banned: {user.ban_reason}'}, status=403)
            
            # Check access
            has_access = False
            
            # 1. Check active subscription
            if user.has_active_subscription():
                has_access = True
            
            # 2. Check one-time purchase
            if not has_access:
                from apps.payments.models import OneTimePurchase
                has_access = OneTimePurchase.objects.filter(
                    user=user,
                    content_type=content_type,
                    content_id=content_id,
                    status='completed'
                ).exists()
            
            if not has_access:
                return JsonResponse({
                    'error': 'Subscription or one-time purchase required',
                    'requires_payment': True,
                    'content_type': content_type,
                    'content_id': content_id
                }, status=402)
            
            # Check concurrent stream limit (1 stream per session)
            current_session = UserSession.objects.filter(
                session_key=request.session.session_key
            ).first()
            
            if current_session and current_session.current_streaming_content:
                # User already has an active stream
                # Check if it's been more than 5 minutes without activity
                inactive_time = timezone.now() - current_session.streaming_started_at
                if inactive_time < timedelta(minutes=5):
                    return JsonResponse({
                        'error': 'Only one stream allowed at a time',
                        'active_stream': current_session.current_streaming_content
                    }, status=409)
            
            # Update session with current stream
            if current_session:
                current_session.current_streaming_content = f"{content_type}:{content_id}"
                current_session.streaming_started_at = timezone.now()
                current_session.save()
        
        return self.get_response(request)