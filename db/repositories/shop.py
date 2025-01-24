from db.schemas import (TopUpsTable, RedeemCodesTable, 
                        PurchasesTable, UCPackagesTable)
from db.repository import BaseRepository

from sqlalchemy.orm import Session
from sqlalchemy import select


class UCPackagesTableRepository(BaseRepository):
    table = UCPackagesTable
    
    async def get_all_ucpackages(self, session: Session) -> list[UCPackagesTable]:
        query = select(UCPackagesTable)
        
        with session:
            uc_packages = (
                session.execute(query)
            ).scalars().all()
        
        return uc_packages
    
    async def get_ucpackage_by_id(self, package_id, session: Session) -> UCPackagesTable:
        query = select(UCPackagesTable).where(UCPackagesTable.id == package_id)
        
        with session:
            uc_package = (
                session.execute(query)
            ).scalar_one_or_none()
        
        return uc_package
    

class PurchasesTableRepository(BaseRepository):
    table = PurchasesTable

    async def purchase(self, account_id: int, balance_type: str, redeem_code_id: int, session: Session):
        with session:
            obj = PurchasesTable(
                account_id = account_id,
                balance_type = balance_type,
                redeem_code_id = redeem_code_id
            )

            session.add(obj)
            session.commit()
            session.refresh(obj)

            RedeemCodesTableRepository().edit(
                conditions = {"id": redeem_code_id},
                edits = {"is_used": True},
                session = session
            )

        
        return obj


class TopUpsTableRepository(BaseRepository):
    table = TopUpsTable


class RedeemCodesTableRepository(BaseRepository):
    table = RedeemCodesTable

    async def get_active_redeem_codes_by_package_id(self, package_id, session: Session):
        query = select(RedeemCodesTable).where(RedeemCodesTable.package_id == package_id, RedeemCodesTable.is_used == False)
        
        with session:
            redeem_codes = (
                session.execute(query)
            ).scalars().all()

        return redeem_codes