import hmac
import hashlib
import time
from django.conf import settings

def generate_signed_stream_url(video_source_id, user_id, expires_in_seconds=3600):
    """
    Generate a signed URL that expires after `expires_in_seconds`
    """
    video_source = VideoSource.objects.get(id=video_source_id)
    
    expires_at = int(time.time()) + expires_in_seconds
    
    # Create signature
    message = f"{video_source_id}:{user_id}:{expires_at}"
    signature = hmac.new(
        settings.STREAM_SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Build URL
    signed_url = f"{video_source.url}?token={signature}&expires={expires_at}&user={user_id}"
    
    return signed_url

# Endpoint: GET /api/stream/get-url/?content_type=movie&content_id=123
# Returns signed URL valid for 1 hour
