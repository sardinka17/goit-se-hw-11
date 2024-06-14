from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(15), nullable=False)
    birthday_date = Column(Date)
