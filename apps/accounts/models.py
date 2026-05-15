from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Phone number is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    # Authentication (phone number as username)
    username = models.CharField(max_length=15, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)  # Optional for password reset
    
    # Personal info
    full_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True)
    
    # Account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    banned_at = models.DateTimeField(null=True, blank=True)
    
    # Account deletion (GDPR)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deletion_scheduled_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    email_notifications = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=True)
    
    # Wallet
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    
    # Security
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.phone_number
    
    def has_active_subscription(self):
        return self.subscriptions.filter(
            status='active',
            expiry_date__gt=timezone.now()
        ).exists()
    
    def get_active_subscription(self):
        return self.subscriptions.filter(
            status='active',
            expiry_date__gt=timezone.now()
        ).first()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True, db_index=True)
    
    # Device info
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=50, blank=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    
    # Location (optional, from IP)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    # Streaming tracking
    current_streaming_content = models.CharField(max_length=50, blank=True)  # movie_id or episode_id
    streaming_started_at = models.DateTimeField(null=True, blank=True)
    
    def is_expired(self):
        return timezone.now() > self.expires_at


