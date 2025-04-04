from datetime import date, timedelta
from typing import Optional, Union, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, contact: ContactCreate) -> Contact:
        db_contact = Contact(**contact.model_dump())
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def get_all(self) -> List[Contact]:
        stmt = select(Contact)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars())

    async def get_by_id(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def update(self, contact_id: int, contact_update: ContactUpdate) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id)
        result = await self.db.execute(stmt)
        db_contact = result.scalar_one_or_none()
        if db_contact:
            for key, value in contact_update.model_dump(exclude_unset=True).items():
                setattr(db_contact, key, value)
            await self.db.commit()
            await self.db.refresh(db_contact)
        return db_contact

    async def delete(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        contact = contact.scalar_one_or_none()
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search(self, query: str) -> List[Contact]:
        stmt = select(Contact).filter(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars())

    async def get_upcoming_birthdays(self) -> List[Contact]:
        today = date.today()
        seven_days_later = today + timedelta(days=7)

        stmt = select(Contact).filter(
            or_(
                Contact.birthday.between(today, seven_days_later)
            )
        )
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars())

    async def get_contacts_with_birthday_between(self, start_date: date, end_date: date) -> List[Contact]:

        # Отримання контактів з днями народження між вказаними датами

        stmt = select(Contact).filter(
            or_(
                Contact.birthday.between(start_date, end_date)
            )
        )
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars())
