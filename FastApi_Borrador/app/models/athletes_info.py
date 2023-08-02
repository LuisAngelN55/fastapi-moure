from db.database import Base
from sqlalchemy import Column, Integer, Sequence, String, BigInteger, Date, DateTime, Boolean, ForeignKey, SmallInteger, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from models import master_models
from sqlalchemy.dialects.postgresql import UUID
import uuid


## * ------------------- ATHLETES MODEL ------------------- ##
class Athletes(Base):
    __tablename__ = "athletes"
    
    # id                   = Column( BigInteger, Sequence('athletes_table_seq', start=1), autoincrement=True)
    id                 = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username             = Column(String(50), nullable=False, unique=True)
    email                = Column(String(100), nullable=False, unique=True)
    first_name           = Column(String(50))
    last_name            = Column(String(50))
    display_name         = Column(String(30))
    hashed_password      = Column(String(80), nullable=False) 
    photo_url            = Column(String(200))
    birthday             = Column(Date)

    created_date         = Column(DateTime(timezone=True), default= datetime.now(), server_default=func.now())
    last_connection      = Column(DateTime(timezone=True))
    email_verified       = Column(Boolean, default=False, server_default='False')
    is_active            = Column(Boolean, default=True, server_default='True')
    is_superuser         = Column(Boolean, default=False, server_default='False')
    
    blood_type_id        = Column(SmallInteger, ForeignKey('blood_types.id'))
    nationality_code     = Column(String(4), ForeignKey('country_codes.code'))
    document_number_id   = Column(Integer, ForeignKey('document_numbers.id'))
    phone_id             = Column(Integer, ForeignKey('phones.id'))
    gender_code          = Column(String(4), ForeignKey('gender_codes.code'))
    
    google_sub           = Column(String(255), unique=True)
    facebook_sub         = Column(String(255), unique=True)
    
    phones               = relationship('Phones', backref='athletes', foreign_keys=[phone_id])



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

    id                    = Column(Integer, primary_key=True, autoincrement=True)
    athlete_id            = Column(UUID(as_uuid=True), ForeignKey('athletes.id'), unique=True)
    fcenter_id            = Column(Integer, ForeignKey('fitness_centers.id'), unique=True)
    country_code_id       = Column(String(4), ForeignKey('country_codes.code'))
    dial_code             = Column(String(5), nullable= False)
    phone_number          = Column(String(15), nullable=False)
    
    athlete               = relationship('Athletes', foreign_keys=[athlete_id])
    fcenter               = relationship('Fitness_Centers', foreign_keys=[fcenter_id])
    
    

## * ------------------- ATHLETES FITNESS CENTER REL MODEL ------------------- ##
class Relation_Athlete_FCenter(Base): 
    __tablename__         = 'relation_athlete_fcenter'
    __table_args__        = (
                                UniqueConstraint('athlete_id', 'fcenter_id', name='unique_athlete_relation'),
                            )

    id                    = Column(Integer, primary_key=True, autoincrement=True)
    athlete_id            = Column(UUID(as_uuid=True), ForeignKey('athletes.id'), nullable=False)
    fcenter_id            = Column(Integer, ForeignKey('fitness_centers.id'), nullable=False)
    role_type_id          = Column(Integer, ForeignKey('role_types_codes.id'), nullable=False)

    
    created_date          = Column(DateTime(timezone=True), default= datetime.now(), server_default=func.now(), nullable=False)
    
    athlete               = relationship('Athletes', foreign_keys=[athlete_id])
    fcenter               = relationship('Fitness_Centers', foreign_keys=[fcenter_id])
    