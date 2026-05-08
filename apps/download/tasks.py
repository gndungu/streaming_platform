from celery import shared_task

@celery_app.task
def cleanup_expired_downloads():
    """Delete expired downloads from storage"""
    expired_downloads = Download.objects.filter(
        expires_at__lt=timezone.now(),
        status='completed'
    )
    
    for download in expired_downloads:
        # Delete file from storage
        if download.storage_path:
            delete_from_storage(download.storage_path)
        
        # Mark as expired
        download.status = 'expired'
        download.save()
