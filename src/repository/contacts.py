from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


def get_all_contacts(offset: int, limit: int, db: Session) -> list[Contact]:
    return db.query(Contact).offset(offset).limit(limit).all()


def get_contact(contact_id: int, db: Session) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(body: ContactCreate, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday_date=body.birthday_date
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday_date = body.birthday_date

        db.commit()
        db.refresh(contact)

    return contact


def delete_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact


def get_contact_by_first_name(contact_first_name: str, db: Session) -> Contact | None:
    return db.query(Contact).filter(func.lower(Contact.first_name) == contact_first_name.lower()).first()


def get_contact_by_last_name(contact_last_name: str, db: Session) -> Contact | None:
    return db.query(Contact).filter(func.lower(Contact.last_name) == contact_last_name.lower()).first()


def get_contact_by_email(contact_email: str, db: Session) -> Contact | None:
    return db.query(Contact).filter(Contact.email == contact_email).first()


def get_contacts_upcoming_birthdays(db: Session):
    contacts_upcoming_birthdays = []
    date_today = datetime.today().date()
    today_plus_week = date_today + timedelta(days=7)

    contacts = db.query(Contact).all()

    for contact in contacts:
        birthday = datetime.strptime(str(contact.birthday_date), '%Y-%m-%d').date().replace(year=date_today.year)

        if date_today.timetuple().tm_yday <= birthday.timetuple().tm_yday <= today_plus_week.timetuple().tm_yday:
            contacts_upcoming_birthdays.append(contact)

    return contacts_upcoming_birthdays