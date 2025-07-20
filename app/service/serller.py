from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller


password_context = CryptContext(schemes=["bcrypt"])


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller_credentials: SellerCreate) -> Seller:
        seller = Seller(
            **seller_credentials.model_dump(exclude=["password"]),
            password_hash=password_context.hash(seller_credentials.password),  # type: ignore
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
