from django.db import models

class Download(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('downloading', 'Downloading'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    
    content_type = models.CharField(max_length=20)  # movie, episode
    content_id = models.PositiveIntegerField()
    
    # Download details
    quality = models.CharField(max_length=10)  # 360p, 720p, etc.
    file_url = models.URLField(max_length=1000)  # Signed URL
    file_size_mb = models.FloatField()
    
    # Local storage (if stored on our servers)
    storage_path = models.CharField(max_length=500, blank=True)
    
    # Expiry
    expires_at = models.DateTimeField()  # Downloaded file stops working after this
    is_downloaded = models.BooleanField(default=False)
    downloaded_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    failure_reason = models.TextField(blank=True)
    
    # Download limits (for tracking)
    download_attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'content_id', 'quality']

class DownloadLimit(models.Model):
    """Track user's download quota"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='download_limit')
    
    # Daily limits
    daily_downloads_used = models.IntegerField(default=0)
    daily_reset_at = models.DateTimeField()
    
    # Total limits (based on subscription tier)
    max_downloads_per_day = models.IntegerField(default=5)
    max_storage_gb = models.FloatField(default=10)
    
    # Current total downloaded size
    total_downloaded_bytes = models.BigIntegerField(default=0)
    
    def can_download(self, file_size_mb):
        """Check if user can download this file"""
        # Check daily limit
        if self.daily_downloads_used >= self.max_downloads_per_day:
            return False, "Daily download limit reached"
        
        # Check storage limit
        if (self.total_downloaded_bytes + (file_size_mb * 1024 * 1024)) > (self.max_storage_gb * 1024 * 1024 * 1024):
            return False, "Download storage limit reached"
        
        return True, "OK"
    
    def record_download(self, file_size_mb):
        """Record a download"""
        self.daily_downloads_used += 1
        self.total_downloaded_bytes += int(file_size_mb * 1024 * 1024)
        self.save()

