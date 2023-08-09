from db.database import Base
from sqlalchemy import CheckConstraint, Column, Integer, String, BigInteger, Date, DateTime, Boolean, SmallInteger, CHAR, ForeignKey, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from models import athletes_info
from sqlalchemy.dialects.postgresql import UUID


## * ------------------- BLOOD TYPES MODEL ------------------- ##
class Blood_Types(Base):
    __tablename__    = "blood_types"
    
    id               = Column(SmallInteger, primary_key=True)
    blood_type       = Column(String(3), nullable=False, unique=True)
    
    athletes         = relationship('Athletes', backref="blood_types")



## * ------------------- LANGUAGES MODEL ------------------- ##language_codes.code
class Language_Codes(Base):
    __tablename__        = 'language_codes'
    
    id                   = Column(SmallInteger, primary_key=True)
    code                 = Column(String(3), nullable=False, unique=True)
    is_active            = Column(Boolean, nullable=False)
    
    countries             = relationship('Countries', backref='language_codes')
    doc_types             = relationship('Document_Type_Names', backref='language_codes')
    genders               = relationship('Genders', backref='language_codes')
    lang_names            = relationship('Languages', backref='language_codes')




## * ------------------- LANGUAGE NAMES MODEL ------------------- ##
class Languages(Base):
    __tablename__     = 'languages'
    
    id                = Column(SmallInteger, primary_key=True)
    lang_code         = Column(String(3), ForeignKey('language_codes.code'), nullable=False)
    lang_name         = Column(String(25), nullable=False)


## * ------------------- DOCUMENT TYPES MODEL ------------------- ##
class Document_Types(Base):
    __tablename__         = "document_types"

    id                    = Column(SmallInteger, primary_key=True)
    doc_type_code         = Column(String(5), nullable=False, unique=True)
    is_active             = Column(Boolean, nullable=False)

    doc_numbers           = relationship('Document_Numbers', backref='document_types')
    doc_type_names        = relationship('Document_Type_Names', backref='document_types')



## * ------------------- Document Type Names MODEL ------------------- ##
class Document_Type_Names(Base):
    __tablename__        = 'document_type_names'
    __table_args__ = (UniqueConstraint('doc_type_code', 'lang_code', name='unique_doctype_desc'), )


    id                   = Column(SmallInteger, primary_key=True)
    doc_type_code        = Column(String(4), ForeignKey('document_types.doc_type_code'), nullable=False)
    doc_name             = Column(String(50), nullable=False)   
    lang_code            = Column(String(3), ForeignKey('language_codes.code'), nullable=False)


## * ------------------- DOCUMENT NUMBERS MODEL ------------------- ##
class Document_Numbers(Base):
    __tablename__        = 'document_numbers'
    __table_args__       = (
                             UniqueConstraint('doc_type_code', 'doc_number', name='unique_document'),
                             CheckConstraint('num_nonnulls(athlete_id, fcenter_id) > 0'),
                           )    


    id                   = Column(SmallInteger, primary_key=True)
    athlete_id           = Column(UUID(as_uuid=True), ForeignKey('athletes.id'), nullable=False)
    fcenter_id           = Column(UUID(as_uuid=True), ForeignKey('fitness_centers.id'))
    doc_type_code        = Column(String(4), ForeignKey('document_types.doc_type_code'), nullable=False)
    doc_number           = Column(String(15), nullable=False)
    
    athlete              = relationship('Athletes', foreign_keys=[athlete_id])
    fitness_centers      = relationship('Fitness_Centers', foreign_keys=[fcenter_id])



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

    athletes         = relationship('Athletes', backref="gender_codes")
    gender_desc      = relationship('Genders', backref="gender_codes")


## * ------------------- GENDERS MODEL ------------------- ##S
class Genders(Base):
    __tablename__    = "genders"
    __table_args__ = (UniqueConstraint('lang_code', 'gender_code', name='unique_gender'), )

    
    id               = Column(SmallInteger, primary_key=True)
    lang_code        = Column(String(3), ForeignKey('language_codes.code'))
    gender_code      = Column(String(8), ForeignKey('gender_codes.code'))
    desc             = Column(String(20), nullable=False)
    
    

## * ------------------- ROLE TYPES CODES MODEL ------------------- ##
class Role_Type_Codes(Base):
    __tablename__    = "role_types_codes"
    
    id                       = Column(SmallInteger, primary_key=True)
    code                     = Column(String(8), unique=True)
    is_active                = Column(Boolean, nullable=False)
    
    athletes_fitness_center  = relationship('Relation_Athlete_FCenter', backref="role_types_codes")
    role_desc                = relationship('Role_Types', backref="role_types_codes")
    
    

## * ------------------- ROLE TYPES NAMES MODEL ------------------- ##S
class Role_Types(Base):
    __tablename__    = "role_types"
    __table_args__ = (UniqueConstraint('lang_code', 'role_type_id', name='unique_role_type'), )

    
    id               = Column(SmallInteger, primary_key=True)
    lang_code        = Column(String(3), ForeignKey('language_codes.code'))
    role_type_id     = Column(Integer, ForeignKey('role_types_codes.id'))
    desc             = Column(String(20), nullable=False)


# server_default=Sequence('mdata_translations_seq', start=1).next_value()
# __table_args__ = (UniqueConstraint('table_name', 'row_id', 'language_code', name='unique_translations'), )

