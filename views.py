from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .serializers import *

class TelegramAccountViewSet(viewsets.ModelViewSet):
    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer
    
    @action(detail=False, methods=['post'])
    def batch_check_activity(self, request):
        account_ids = request.data.get('account_ids', [])
        accounts = TelegramAccount.objects.filter(id__in=account_ids)
        # 调用批量检查活性
        return Response({'status': 'processing'})
    
    @action(detail=False, methods=['post'])
    def convert_format(self, request):
        account_ids = request.data.get('account_ids', [])
        target_format = request.data.get('format')  # 'session' or 'tdata'
        accounts = TelegramAccount.objects.filter(id__in=account_ids)
        # 调用格式转换
        return Response({'status': 'processing'})

class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            # 返回支付地址
            return Response({
                'order': serializer.data,
                'payment_address': '你的TRON地址'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
