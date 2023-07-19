from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime, Boolean, ForeignKey, SmallInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from models import master_models


## * ------------------- ATHLETES MODEL ------------------- ##
class Athletes(Base):
    __tablename__ = "athletes"
    
    id               = Column( BigInteger, primary_key=True)
    username         = Column(String(50), nullable=False)
    email            = Column(String(100), nullable=False)
    first_name       = Column(String(50))
    last_name        = Column(String(50))
    display_name     = Column(String(30))
    password         = Column(String(80), nullable=False) 
    photo_url        = Column(String(200))
    birthday         = Column(Date)
    
    created_date     = Column(DateTime(timezone=True), default= datetime.now(), server_default=func.now())
    last_connection  = Column(DateTime(timezone=True))
    email_verified   = Column(Boolean, default=False, server_default='False')
    is_active        = Column(Boolean, default=True, server_default='True')
    
    blood_type_id    = Column(SmallInteger, ForeignKey('blood_types.id'))
    nationality_code   = Column(String(4), ForeignKey('country_codes.code'))
    phone_id         = Column(Integer, ForeignKey('phones.id'))
    gender_code        = Column(String(4), ForeignKey('gender_codes.code'))
    
    phones           =      relationship('Phones', backref='athletes', foreign_keys=[phone_id])



## * ------------------- FITNESS CENTERS MODEL ------------------- ##
class Fitness_Centers(Base):
    __tablename__    = 'fitness_centers'

    id               = Column(Integer, primary_key=True)
    boxname          = Column(String(50), nullable=False)
    email            = Column(String(100), nullable=False)
    display_name     = Column(String(30))
    photo_url        = Column(String(200))
    birthday         = Column(Date)
    phone_id         = Column(Integer, ForeignKey('phones.id'))
    created_date     = Column(DateTime(timezone=True), default= datetime.now(), server_default=func.now())


    phones           = relationship('Phones', backref='fitness_center', foreign_keys=[phone_id])



## * ------------------- PHONES MODEL ------------------- ##
class Phones(Base): 
    __tablename__         = 'phones'
    __table_args__        = (
                                UniqueConstraint('country_code_id', 'phone_number', name='unique_phone'),
                                CheckConstraint('num_nonnulls(athlete_id, fcenter_id) > 0'),
                            )

    id                    = Column(Integer, primary_key=True)
    athlete_id            = Column(Integer, ForeignKey('athletes.id'), ForeignKey('phones.id'))
    fcenter_id            = Column(Integer, ForeignKey('fitness_centers.id'))
    country_code_id       = Column(String(4), ForeignKey('country_codes.code'))
    phone_number          = Column(String(15), nullable=False)
    
    
    athlete               = relationship('Athletes', foreign_keys=[athlete_id])
    fcenter               = relationship('Fitness_Centers', foreign_keys=[fcenter_id])
    country_code          = relationship('Country_Codes', foreign_keys=[country_code_id])
    
