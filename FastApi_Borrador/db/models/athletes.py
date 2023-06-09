from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime, Boolean, ForeignKey, SmallInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime


class Athletes(Base):
    __tablename__ = "athletes"
    
    id               = Column( BigInteger, primary_key=True)
    username         = Column(String(50), nullable=False)
    email            = Column(String(100), nullable=False)
    first_name       = Column(String(50))
    last_name        = Column(String(50))
    display_name     = Column(String(30))
    birthday         = Column(Date)
    password         = Column(String(20), nullable=False) 
    photo_url        = Column(String(200))
    birthday         = Column(Date)
    
    created_date     = Column(DateTime(timezone=True), default= datetime.now(), server_default=func.now())
    last_connection  = Column(DateTime(timezone=True))
    email_verified   = Column(Boolean, default=False, server_default='False')
    is_active        = Column(Boolean, default=True, server_default='True')
    
    blood_type_id    = Column(SmallInteger, ForeignKey('blood_type.id'))
    # nationality_id   = Column(Integer, ForeignKey('countrie.id'))
    # phone_id         = Column(Integer, ForeignKey('phone.id'))
    # gender_id        = Column(Integer, ForeignKey('gender.id'))
    
    phone_id = relationship('Document_Number', backref='athletes')