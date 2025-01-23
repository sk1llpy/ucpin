from sqlalchemy.orm import relationship, Mapped, mapped_column, Session
from sqlalchemy import ForeignKey

from db.config import BaseModel

# Create your tables here.
class UsersTable(BaseModel):
    __tablename__ = 'users_user'

    user_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('users_account.id'))
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=False)
    is_logined: Mapped[bool] = mapped_column()
    
    account: Mapped["AccountsTable"] = relationship(back_populates="users")


class AccountsTable(BaseModel):
    __tablename__ = 'users_account'

    phone_number: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    is_banned: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column()
    balance_usd: Mapped[float] = mapped_column(default=0)
    balance_uzs: Mapped[float] = mapped_column(default=0)
    admins: Mapped[list["AdminsTable"]] = relationship(back_populates='account')
    users: Mapped[list["UsersTable"]] = relationship(back_populates="account")

    purchases: Mapped[list["PurchasesTable"]] = relationship(
        back_populates="account"
    )
    top_ups: Mapped[list["TopUpsTable"]] = relationship(
        back_populates="account"
    )


class AdminsTable(BaseModel):
    __tablename__ = 'users_admin'

    account_id: Mapped[int] = mapped_column(ForeignKey('users_account.id'))    
    account: Mapped["AccountsTable"] = relationship(back_populates='admins')