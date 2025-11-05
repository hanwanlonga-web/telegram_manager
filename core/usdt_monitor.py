from tronpy import Tron
from tronpy.providers import HTTPProvider
import time
import threading
from django.utils import timezone
from .models import USDTTransaction, ServiceOrder

class USDTMonitor:
    def __init__(self):
        self.client = Tron(HTTPProvider(api_key="your_api_key"))
        self.monitoring_addresses = set()
        self.is_monitoring = False
        self.thread = None
    
    def start_monitoring(self, address):
        """开始监控地址"""
        self.monitoring_addresses.add(address)
        if not self.is_monitoring:
            self.is_monitoring = True
            self.thread = threading.Thread(target=self._monitor_loop)
            self.thread.daemon = True
            self.thread.start()
    
    def _monitor_loop(self):
        """监控循环"""
        while self.is_monitoring:
            for address in list(self.monitoring_addresses):
                self._check_transactions(address)
            time.sleep(30)  # 每30秒检查一次
    
    def _check_transactions(self, address):
        """检查交易"""
        try:
            # 获取USDT交易
            transactions = self.client.get_account_transactions(
                address, 
                only_to=True, 
                only_confirmed=True
            )
            
            for tx in transactions:
                if self._is_usdt_transfer(tx):
                    self._process_usdt_transaction(tx)
                    
        except Exception as e:
            print(f"检查交易失败: {e}")
    
    def _is_usdt_transfer(self, transaction):
        """判断是否为USDT转账"""
        try:
            if transaction.get('raw_data', {}).get('contract', [{}])[0].get('type') == 'TriggerSmartContract':
                contract_data = transaction['raw_data']['contract'][0]
                # 这里需要解析USDT转账交易
                return True
        except:
            return False
        return False
    
    def _process_usdt_transaction(self, transaction):
        """处理USDT交易"""
        try:
            tx_hash = transaction['txID']
            
            # 检查是否已处理
            if USDTTransaction.objects.filter(tx_hash=tx_hash).exists():
                return
            
            # 创建交易记录
            usdt_tx = USDTTransaction.objects.create(
                tx_hash=tx_hash,
                from_address=transaction['raw_data']['contract'][0]['parameter']['value']['owner_address'],
                to_address=transaction['raw_data']['contract'][0]['parameter']['value']['to_address'],
                amount=self._parse_usdt_amount(transaction),
                status='confirmed',
                confirmed_at=timezone.now()
            )
            
            # 更新订单状态
            self._update_order_status(usdt_tx)
            
        except Exception as e:
            print(f"处理交易失败: {e}")
    
    def _parse_usdt_amount(self, transaction):
        """解析USDT金额"""
        # 实现USDT金额解析逻辑
        return 0
    
    def _update_order_status(self, usdt_tx):
        """更新订单状态"""
        try:
            # 查找匹配的订单
            orders = ServiceOrder.objects.filter(
                status='pending',
                amount=usdt_tx.amount
            )
            
            for order in orders:
                order.transaction = usdt_tx
                order.status = 'paid'
                order.save()
                
        except Exception as e:
            print(f"更新订单状态失败: {e}")
