from datetime import date, timedelta
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, contact: ContactCreate) -> ContactResponse:
        return await self.repository.create(contact)

    async def get_contacts(self, search: Optional[str] = None) -> List[ContactResponse]:
        if search:
            return await self.repository.search(search)
        return await self.repository.get_all()

    async def get_contact(self, contact_id: int) -> Optional[ContactResponse]:
        return await self.repository.get_by_id(contact_id)

    async def update_contact(self, contact_id: int, contact_update: ContactUpdate) -> Optional[ContactResponse]:
        return await self.repository.update(contact_id, contact_update)

    async def delete_contact(self, contact_id: int) -> Optional[ContactResponse]:
        return await self.repository.delete(contact_id)

    async def get_upcoming_birthdays(self) -> List[ContactResponse]:
        return await self.repository.get_upcoming_birthdays()

    async def search_contacts(self, query: str) -> List[ContactResponse]:

        # Розширений пошук контактів з додатковою бізнес-логікою

        contacts = await self.repository.search(query)

        return contacts

    async def get_birthday_contacts(self, days: int = 7) -> List[ContactResponse]:

        # Отримання контактів з днями народження на вказану кількість днів

        today = date.today()
        end_date = today + timedelta(days=days)
        return await self.repository.get_contacts_with_birthday_between(today, end_date)
