from db.schemas import UsersTable, AdminsTable, AccountsTable, RedeemCodesTable
from db.repository import BaseRepository
from db import repository as repo
from db.schemas import PurchasesTable, UCPackagesTable

from sqlalchemy.orm import Session
from sqlalchemy import select
from aiogram import types

class UsersTableRepository(BaseRepository):
    table = UsersTable

    async def get_user(self, user_id, session: Session):
        query = select(UsersTable).where(UsersTable.user_id == user_id)

        with session:
            user = (
                session.execute(query)
            ).scalar_one_or_none()
        
        return user
    
    async def get_user_account(self, user_id, session: Session):
        with session:
            user = await self.get_user(user_id = user_id, session = session)
            query = select(AccountsTable).where(AccountsTable.id == user.account_id)

            account = (
                session.execute(query)
            ).scalar_one_or_none()

            return account


    async def create_user(self, user: types.User, is_logined: bool, session: Session):
        with session:
            user = self.create(
                params = {
                    "user_id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "is_logined": is_logined
                },
                session = session
            )
            
        return user

    async def set_account_to_user(self, user_id: int, account_data: dict, session: Session):        
        query = select(UsersTable).where(UsersTable.user_id == user_id)

        with session:
            user = (
                session.execute(query)
            ).scalar_one_or_none()
        
            if not user.is_logined:
                account = await repo.AccountsTableRepository().get_account(account_data, session)
                
                if account:
                    if not account.is_banned:
                        self.edit(
                            conditions={
                                "user_id": user_id
                            },
                            edits={
                                "is_logined": True,
                                "account_id": account.id
                            },
                            session = session
                        )
                    else:
                        {"error": "ACCOUNT_BANNED"}
                else:
                    return {"error": "ACCOUNT_NOT_FOUND"}



class AccountsTableRepository(BaseRepository):
    table = AccountsTable
    
    async def get_account(self, account_data: dict, session: Session):
        email = account_data.get('email')
        phone_number = None if email else account_data.get('phone_number')
        password = account_data.get('password')
        
        query = select(AccountsTable)
        
        if email:
            query = query.where(AccountsTable.email == email, AccountsTable.password == password)
        if phone_number:
            query = query.where(AccountsTable.phone_number == phone_number, AccountsTable.password == password)
        
        with session:
            account = (
                session.execute(query)
            ).scalar_one_or_none()
        
        return account
    
    async def check_email_exists(self, email: str, session: Session):
        query = select(AccountsTable).where(AccountsTable.email == email)
        
        with session:
            account = (
                session.execute(query)
            ).scalar_one_or_none()
        
        return True if account else False
    
    async def check_phone_number_exists(self, phone_number: str, session: Session):
        query = select(AccountsTable).where(AccountsTable.phone_number == phone_number)
        
        with session:
            account = (
                session.execute(query)
            ).scalar_one_or_none()
        
        return True if account else False
    
    async def create_account(self, account_data: dict, session: Session) -> AccountsTable:
        account = self.create(
            params = account_data,
            session = session
        )

        return account
    
    async def get_purchase_history_as_dict(self, account_id: int, session: Session) -> list[dict]:
        query = (
            select(
                RedeemCodesTable.code,
                UCPackagesTable.title,
                PurchasesTable.balance_type,
                PurchasesTable.created_at
            )
            .join(RedeemCodesTable, PurchasesTable.redeem_code_id == RedeemCodesTable.id)
            .join(UCPackagesTable, RedeemCodesTable.package_id == UCPackagesTable.id)
            .where(PurchasesTable.account_id == account_id)
        )

        with session:
            purchases = (
                session.execute(query)
            ).mappings().all()

        return purchases
        

class AdminsTableRepository(BaseRepository):
    table = AdminsTable
