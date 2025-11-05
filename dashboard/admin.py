from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *

@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'account_year', 'is_premium', 'status', 'last_active']
    list_filter = ['status', 'is_premium', 'account_year']
    search_fields = ['phone_number']
    actions = ['check_activity', 'convert_to_tdata']
    
    def check_activity(self, request, queryset):
        # 批量检查活性
        pass
    
    def convert_to_tdata(self, request, queryset):
        # 批量转换Tdata
        pass

@admin.register(AccountFilterRule)
class AccountFilterRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_year', 'max_year', 'require_premium']
    
@admin.register(USDTTransaction)
class USDTTransactionAdmin(admin.ModelAdmin):
    list_display = ['tx_hash', 'from_address', 'to_address', 'amount', 'status']
    readonly_fields = ['tx_hash', 'from_address', 'to_address', 'amount']
    
@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'service_type', 'amount', 'status']
    list_filter = ['status', 'service_type']
