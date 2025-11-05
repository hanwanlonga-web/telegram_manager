import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession, SQLiteSession
import os
import json
from django.conf import settings

class TelegramManager:
    def __init__(self):
        self.clients = {}
    
    async def create_client(self, account, use_tdata=False):
        """创建Telegram客户端"""
        try:
            if use_tdata and account.tdata_path:
                client = TelegramClient(
                    SQLiteSession(account.tdata_path),
                    account.api_id,
                    account.api_hash
                )
            else:
                client = TelegramClient(
                    StringSession(account.session_string),
                    account.api_id,
                    account.api_hash
                )
            
            await client.connect()
            self.clients[account.id] = client
            return client
        except Exception as e:
            print(f"创建客户端失败: {e}")
            return None
    
    async def convert_to_tdata(self, account, output_path):
        """转换Session到Tdata"""
        try:
            client = await self.create_client(account)
            if client:
                await client.session.save(file=output_path)
                account.tdata_path = output_path
                account.save()
                return True
        except Exception as e:
            print(f"转换Tdata失败: {e}")
        return False
    
    async def convert_to_session(self, account):
        """转换Tdata到Session"""
        try:
            client = await self.create_client(account, use_tdata=True)
            if client:
                session_string = client.session.save()
                account.session_string = session_string
                account.save()
                return session_string
        except Exception as e:
            print(f"转换Session失败: {e}")
        return None
    
    async def check_account_activity(self, account):
        """检查账号活性"""
        try:
            client = await self.create_client(account)
            if client:
                me = await client.get_me()
                if me:
                    return {
                        'is_active': True,
                        'username': me.username,
                        'first_name': me.first_name,
                        'last_name': me.last_name,
                        'premium': me.premium
                    }
        except Exception as e:
            print(f"检查活性失败: {e}")
        return {'is_active': False}
    
    async def kick_other_devices(self, account):
        """踢出其他设备"""
        try:
            client = await self.create_client(account)
            if client:
                result = await client(functions.account.ResetAuthorizationRequest(
                    hash=0  # 踢出所有设备，除了当前
                ))
                return True
        except Exception as e:
            print(f"踢出设备失败: {e}")
        return False
    
    async def change_2fa_password(self, account, new_password):
        """修改二次验证密码"""
        try:
            client = await self.create_client(account)
            if client:
                await client.edit_2fa(new_password=new_password)
                return True
        except Exception as e:
            print(f"修改2FA失败: {e}")
        return False
    
    async def clean_dialogs(self, account, keep_contacts=True):
        """清理对话"""
        try:
            client = await self.create_client(account)
            if client:
                async for dialog in client.iter_dialogs():
                    if keep_contacts and dialog.is_user:
                        continue
                    await dialog.delete()
                return True
        except Exception as e:
            print(f"清理对话失败: {e}")
        return False
    
    async def hide_phone_number(self, account):
        """隐藏手机号"""
        try:
            client = await self.create_client(account)
            if client:
                await client(functions.account.UpdatePrivacyRequest(
                    key=types.InputPrivacyKeyPhoneNumber(),
                    rules=[types.InputPrivacyValueAllowAll()]
                ))
                return True
        except Exception as e:
            print(f"隐藏手机号失败: {e}")
        return False

class AccountBatchProcessor:
    """账号批量处理器"""
    
    def __init__(self):
        self.manager = TelegramManager()
    
    async def batch_convert_format(self, accounts, target_format):
        """批量转换格式"""
        results = []
        for account in accounts:
            if target_format == 'tdata':
                result = await self.manager.convert_to_tdata(account, f'tdata/{account.id}')
            else:
                result = await self.manager.convert_to_session(account)
            results.append({
                'account_id': account.id,
                'success': bool(result),
                'result': result
            })
        return results
    
    async def batch_check_activity(self, accounts):
        """批量检查活性"""
        results = []
        for account in accounts:
            activity = await self.manager.check_account_activity(account)
            results.append({
                'account_id': account.id,
                **activity
            })
        return results
    
    async def batch_kick_devices(self, accounts):
        """批量踢出设备"""
        results = []
        for account in accounts:
            success = await self.manager.kick_other_devices(account)
            results.append({
                'account_id': account.id,
                'success': success
            })
        return results
