from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_postgres_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactCreate, ContactUpdate, ContactResponse

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/')
def get_all_contacts(
        offset: int = 0,
        limit: int = 50,
        db: Session = Depends(get_postgres_db)
) -> list[ContactModel]:
    contacts = repository_contacts.get_all_contacts(offset, limit, db)

    return contacts


@router.get('/{contact_id}')
def get_contact(
        contact_id: int = Path(ge=1),
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    contact = repository_contacts.get_contact(contact_id, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_contact(
        body: ContactCreate,
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    return repository_contacts.create_contact(body, db)


@router.put('/{contact_id}')
def update_contact(
        contact_id: int,
        body: ContactUpdate,
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    contact = repository_contacts.update_contact(contact_id, body, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
        contact_id: int,
        db: Session = Depends(get_postgres_db)
):
    contact = repository_contacts.delete_contact(contact_id, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.get('/search_by_first_name/')
def get_contact_by_first_name(
        contact_first_name: str = Query(),
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    contact = repository_contacts.get_contact_by_first_name(contact_first_name, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.get('/search_by_last_name/')
def get_contact_by_last_name(
        contact_last_name: str = Query(),
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    contact = repository_contacts.get_contact_by_last_name(contact_last_name, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.get('/search_by_email/')
def get_contact_by_email(
        contact_email: str = Query(),
        db: Session = Depends(get_postgres_db)
) -> ContactResponse:
    contact = repository_contacts.get_contact_by_email(contact_email, db)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact is not found')

    return contact


@router.get('/upcoming_birthdays/')
def get_contacts_upcoming_birthdays(db: Session = Depends(get_postgres_db)):
    contacts = repository_contacts.get_contacts_upcoming_birthdays(db)

    return contacts
