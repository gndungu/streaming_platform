from django.db import models

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='UGX')
    
    # Limits
    max_balance = models.DecimalField(max_digits=12, decimal_places=2, default=5000000)  # 5M UGX
    
    # Status
    is_active = models.BooleanField(default=True)
    frozen_until = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def add_funds(self, amount, transaction_ref):
        """Add funds to wallet"""
        if not self.is_active:
            raise ValueError("Wallet is inactive")
        
        if self.frozen_until and self.frozen_until > timezone.now():
            raise ValueError(f"Wallet frozen until {self.frozen_until}")
        
        new_balance = self.balance + amount
        if new_balance > self.max_balance:
            raise ValueError(f"Wallet balance would exceed maximum of {self.max_balance}")
        
        self.balance = new_balance
        self.save()
        
        # Create transaction record
        Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='credit',
            reference=transaction_ref,
            status='completed',
            description=f"Added {amount} UGX"
        )
        
        return self.balance
    
    def deduct_funds(self, amount, transaction_ref):
        """Deduct funds from wallet"""
        if not self.is_active:
            raise ValueError("Wallet is inactive")
        
        if self.frozen_until and self.frozen_until > timezone.now():
            raise ValueError(f"Wallet frozen until {self.frozen_until}")
        
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self.save()
        
        # Create transaction record
        Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='debit',
            reference=transaction_ref,
            status='completed',
            description=f"Deducted {amount} UGX"
        )
        
        return self.balance

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    reference = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment gateway specific
    payment_method = models.CharField(max_length=50, blank=True)  # mobile_money, card, etc.
    payment_gateway_response = models.JSONField(default=dict, blank=True)
    
    # For purchases
    purchase_content_type = models.CharField(max_length=50, blank=True)
    purchase_content_id = models.PositiveIntegerField(null=True, blank=True)
    
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # For refunds
    refunded_transaction = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"TXN{int(time.time())}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)


# Supported providers: MTN Mobile Money, Airtel Money
class PaymentGateway(models.Model):
    PROVIDER_CHOICES = [
        ('mtn', 'MTN Mobile Money'),
        ('airtel', 'Airtel Money'),
        ('card', 'Card (Stripe)'),
    ]
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    is_active = models.BooleanField(default=True)
    
    # API credentials (encrypted)
    api_key = models.CharField(max_length=255)  # Store encrypted
    api_secret = models.CharField(max_length=255)  # Store encrypted
    webhook_secret = models.CharField(max_length=255, blank=True)
    
    # Environment
    is_sandbox = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.PROTECT)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    
    # Request/Response data
    external_reference = models.CharField(max_length=100, unique=True, db_index=True)
    payment_reference = models.CharField(max_length=100, blank=True)  # From provider
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_reason = models.TextField(blank=True)
    
    # Webhook data
    webhook_received_at = models.DateTimeField(null=True, blank=True)
    webhook_payload = models.JSONField(default=dict, blank=True)
    
    # Result
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()  # Payment must be completed by this time
    
    def process_webhook(self, payload):
        """Process payment provider webhook"""
        # Verify signature
        # Extract payment status
        # Update this record and create transaction
        pass
