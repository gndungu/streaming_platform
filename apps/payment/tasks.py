# Celery task for subscription expiry
@celery_app.task
def check_expired_subscriptions():
    """Daily task to mark expired subscriptions"""
    expired_subscriptions = UserSubscription.objects.filter(
        status='active',
        expiry_date__lt=timezone.now()
    )
    
    for subscription in expired_subscriptions:
        subscription.status = 'expired'
        subscription.save()
        
        # Send notification
        send_expiry_notification(subscription.user)
