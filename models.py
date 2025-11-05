from django.db import models
from django.contrib.auth.models import User
import json

class TelegramAccount(models.Model):
    ACCOUNT_STATUS = (
        ('active', '活跃'),
        ('inactive', '非活跃'),
        ('banned', '封禁'),
        ('limited', '限制'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    api_id = models.CharField(max_length=100)
    api_hash = models.CharField(max_length=100)
    session_string = models.TextField()
    tdata_path = models.CharField(max_length=500, blank=True)
    
    # 账号信息
    account_year = models.IntegerField(default=2024)
    is_premium = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ACCOUNT_STATUS, default='active')
    last_active = models.DateTimeField(auto_now=True)
    
    # 设备信息
    device_model = models.CharField(max_length=100, blank=True)
    system_version = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'telegram_accounts'

class AccountFilterRule(models.Model):
    name = models.CharField(max_length=100)
    min_year = models.IntegerField(default=2010)
    max_year = models.IntegerField(default=2024)
    require_premium = models.BooleanField(default=False)
    require_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'account_filter_rules'

class USDTTransaction(models.Model):
    TRON_STATUS = (
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('failed', '失败'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=100, unique=True)
    from_address = models.CharField(max_length=100)
    to_address = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    status = models.CharField(max_length=20, choices=TRON_STATUS, default='pending')
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usdt_transactions'

class ServiceOrder(models.Model):
    ORDER_STATUS = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)
    service_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    transaction = models.ForeignKey(USDTTransaction, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'service_orders'
