from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.config import BaseModel

# UCPackage model
class UCPackagesTable(BaseModel):
    __tablename__ = 'shop_ucpackage'

    title: Mapped[str] = mapped_column()
    price_usd: Mapped[float] = mapped_column()
    price_uzs: Mapped[float] = mapped_column()

    redeem_codes: Mapped[list["RedeemCodesTable"]] = relationship(
        back_populates="package"
    )


# RedeemCode model
class RedeemCodesTable(BaseModel):
    __tablename__ = 'shop_redeemcode'

    code: Mapped[str] = mapped_column(unique=True)
    package_id: Mapped[int] = mapped_column(ForeignKey('shop_ucpackage.id'))
    is_used: Mapped[bool] = mapped_column(default=False)

    package: Mapped["UCPackagesTable"] = relationship(
        back_populates="redeem_codes"
    )
    purchases: Mapped[list["PurchasesTable"]] = relationship(
        back_populates="redeem_code"
    )


# Purchase model
class PurchasesTable(BaseModel):
    __tablename__ = 'shop_purchase'

    account_id: Mapped[int] = mapped_column(ForeignKey('users_account.id'))
    redeem_code_id: Mapped[int] = mapped_column(
        ForeignKey('shop_redeemcode.id')
    )
    balance_type: Mapped[str] = mapped_column(nullable=True)

    account: Mapped["AccountsTable"] = relationship(back_populates="purchases")
    redeem_code: Mapped["RedeemCodesTable"] = relationship(
        back_populates="purchases"
    )


class TopUpsTable(BaseModel):
    __tablename__ = 'shop_topup'

    account_id: Mapped[int] = mapped_column(ForeignKey('users_account.id'))
    amount: Mapped[float] = mapped_column()
    balance_type: Mapped[str] = mapped_column()
    payment_type: Mapped[str] = mapped_column()
    verified: Mapped[bool] = mapped_column(default=False)

    account: Mapped["AccountsTable"] = relationship(back_populates="top_ups")
