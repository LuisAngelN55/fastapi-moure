from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime, Boolean, SmallInteger, CHAR, ForeignKey, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime



## * ------------------- BLOOD TYPES MODEL ------------------- ##
class Blood_Types(Base):
    __tablename__    = "blood_types"
    
    id               = Column(SmallInteger, primary_key=True)
    blood_type       = Column(String(2), nullable=False)
    rh               = Column(CHAR, nullable=False)
    
    athletes         = relationship('Athletes', backref="blood_type")



## * ------------------- LANGUAGES MODEL ------------------- ##language_codes.code
class Language_Codes(Base):
    __tablename__        = 'language_codes'
    
    id                   = Column(SmallInteger, primary_key=True)
    code                 = Column(String(3), nullable=False, unique=True)
    is_active            = Column(Boolean, nullable=False)
    
    countries      = relationship('Countries', back_populates='language_codes')
    doc_types      = relationship('Document_Type', back_populates='language_codes')
    genders        = relationship('Gender', back_populates='language_codes')
    lang_names     = relationship('Languages', back_populates='language_codes')



## * ------------------- LANGUAGE NAMES MODEL ------------------- ##
class Languages(Base):
    __tablename__     = 'languages'
    
    id                = Column(SmallInteger, primary_key=True)
    lang_code         = Column(String(3), ForeignKey('language_codes.code'), nullable=False)
    lang_name         = Column(String(25), nullable=False)


## * ------------------- DOCUMENT TYPES MODEL ------------------- ##
class Document_Types(Base):
    __tablename__         = "document_types"
    __table_args__        = (UniqueConstraint('doc_type_code', 'lang_code', name='unique_doc_type'), )

    
    id                    = Column(SmallInteger, primary_key=True)
    doc_type_code         = Column(String(2), nullable=False)
    doc_type_name         = Column(String(30), nullable=False)
    lang_code             = Column(String(3), ForeignKey('language_codes.code'), nullable=False)
    is_active             = Column(Boolean, nullable=False)

    document_number       = relationship('Document_Numbers')



## * ------------------- DOCUMENT NUMBERS MODEL ------------------- ##
class Document_Numbers(Base):
    __tablename__        = 'document_numbers'
    __table_args__ = (UniqueConstraint('athlete_id', 'doc_type', name='unique_doc_number'), )


    id              = Column(SmallInteger, primary_key=True)
    athlete_id      = Column(Integer, ForeignKey('athletes.id'), nullable=False)
    doc_type        = Column(SmallInteger, ForeignKey('document_types.id'), nullable=False)
    doc_number      = Column(Integer, nullable=False)
    
    athletes        = relationship('Athletes', backref='document_numbers', cascade='all, delete')



## * ------------------- COUNTRY CODES MODEL ------------------- ##
class Country_Codes(Base):
    __tablename__        = 'country_codes'


    id                   = Column(SmallInteger, primary_key=True)
    code                 = Column(String(4), nullable=False, unique=True)
    is_active            = Column(Boolean, nullable=False)

    athletes             = relationship('Athletes', backref='country_codes')
    regions              = relationship('Regions', backref='country_codes')
    phones               = relationship('Phones', backref='country_codes')


## * ------------------- COUNTRY MODEL ------------------- ##
class Countries(Base):
    __tablename__        = 'countries'
    __table_args__ = (UniqueConstraint('country_code', 'lang_code', name='unique_country'), )


    id                   = Column(SmallInteger, primary_key=True)
    country_code         = Column(String(4), ForeignKey('country_codes.code'), nullable=False)
    country_name         = Column(String(50), nullable=False)   
    lang_code            = Column(String(3), ForeignKey('language_codes.code'), nullable=False)
   


## * ------------------- REGION MODEL ------------------- ##
class Regions(Base):
    __tablename__        = 'regions'

    id                   = Column(Integer, primary_key=True)
    region_name          = Column(String(30), nullable=False)
    country_code         = Column(String(4), ForeignKey('country_codes.code'), nullable=False)
    is_active            = Column(Boolean, nullable=False)



## * ------------------- GENDER CODES MODEL ------------------- ##
class Gender_Codes(Base):
    __tablename__    = "gender_codes"
    
    id               = Column(SmallInteger, primary_key=True)
    code             = Column(String(8), unique=True)
    is_active        = Column(Boolean, nullable=False)

    athletes         = relationship('Athletes', backref="gender")
    gender_desc      = relationship('Genders', backref="gender")


## * ------------------- GENDERS MODEL ------------------- ##S
class Genders(Base):
    __tablename__    = "genders"
    __table_args__ = (UniqueConstraint('lang_code', 'gender_code', name='unique_gender'), )

    
    id               = Column(SmallInteger, primary_key=True)
    lang_code        = Column(String(3), ForeignKey('language_codes.code'))
    gender_code      = Column(String(8), ForeignKey('gender_codes.code'))
    desc             = Column(String(20), nullable=False)



# server_default=Sequence('mdata_translations_seq', start=1).next_value()
# __table_args__ = (UniqueConstraint('table_name', 'row_id', 'language_code', name='unique_translations'), )