class SubscriptionRequiredMiddleware:
    """
    Middleware to check if user has access to content
    Applied to /api/stream/* and /api/download/* endpoints
    """
    EXEMPT_PATHS = [
        '/api/auth/',
        '/api/payments/',
        '/api/subscriptions/plans/',
        '/api/content/free/',  # Free content (trailers, previews)
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if path requires subscription
        if self.requires_subscription(request.path) and request.user.is_authenticated:
            # Check if user has active subscription
            if not request.user.has_active_subscription():
                # Check for one-time purchase for this specific content
                if not self.has_one_time_purchase(request):
                    return JsonResponse({
                        'error': 'Subscription required',
                        'redirect': '/subscription/plans/'
                    }, status=402)
        
        return self.get_response(request)
    
    def requires_subscription(self, path):
        for exempt in self.EXEMPT_PATHS:
            if path.startswith(exempt):
                return False
        return path.startswith('/api/stream/') or path.startswith('/api/download/')
