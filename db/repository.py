from db.repositories.base import BaseRepository
from db.repositories.users import UsersTableRepository, AdminsTableRepository, AccountsTableRepository
from db.repositories.shop import (
    TopUpsTableRepository, PurchasesTableRepository, 
    RedeemCodesTableRepository, UCPackagesTableRepository)