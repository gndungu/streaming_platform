from django.db import models

class SubscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    price_ugx = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Features
    max_quality = models.CharField(max_length=10, default='720p')  # 360p, 720p, 1080p, 4k
    can_download = models.BooleanField(default=True)
    max_downloads_per_day = models.IntegerField(default=5)
    ad_free = models.BooleanField(default=True)
    concurrent_streams = models.IntegerField(default=1)
    
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_duration_days(self):
        mapping = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 365}
        return mapping.get(self.duration, 1)

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    
    # Dates
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField(db_index=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Auto-renewal
    auto_renew = models.BooleanField(default=False)
    renewal_failed_at = models.DateTimeField(null=True, blank=True)
    
    # Payment tracking
    payment_transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'status', 'expiry_date']),
        ]
    
    def is_active(self):
        return self.status == 'active' and self.expiry_date > timezone.now()
    
    def days_remaining(self):
        delta = self.expiry_date - timezone.now()
        return max(0, delta.days)

class OneTimePurchase(models.Model):
    """Pay-per-view or pay-per-episode"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    
    content_type = models.CharField(max_length=20)  # movie, episode
    content_id = models.PositiveIntegerField()
    
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    
    # Access expiry (optional, e.g., 30 days rental)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, default='active')  # active, expired, refunded
    
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'content_id']
    
    def is_valid(self):
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

