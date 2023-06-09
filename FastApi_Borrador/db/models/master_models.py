from db.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime, Boolean, SmallInteger, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


## * ------------------- BLOOD TYPE MODEL ------------------- ##
class Blood_Type(Base):
    __tablename__    = "blood_type"
    
    id               = Column(SmallInteger, primary_key=True)
    blood_type       = Column(String(2), nullable=False)
    rh               = Column(CHAR, nullable=False)
    
    athletes         = relationship('Athletes', backref="blood_type")
    


## * ------------------- DOCUMENT TYPE MODEL ------------------- ##
class Document_Type(Base):
    __tablename__         = "document_type"
    
    id                    = Column(SmallInteger, primary_key=True)
    document_type_code    = Column(String(2), nullable=False)
    text_content_id       = Column(Integer, ForeignKey('text_content.id'))
    
    document_number       = relationship('Document_Number', backref='document_type')



## * ------------------- DOCUMENT NUMBER MODEL ------------------- ##
class Document_Number(Base):
   __tablename__        = 'document_number'

   athlete_id           = Column(Integer, ForeignKey('athletes.id'), primary_key=True)
   document_type        = Column(SmallInteger, ForeignKey('document_type.id'), primary_key=True)
   document_number      = Column(Integer, primary_key=True)
   
   athletes             = relationship('Athletes', backref='document_number', cascade='all, delete')



## * ------------------- COUNTRY MODEL ------------------- ##
class Countries(Base):
   __tablename__        = 'countries'

   id                   = Column(SmallInteger, primary_key=True)
   country_code         = Column(String(4), nullable=False, unique=True)
   text_content_id      = Column(Integer, ForeignKey('text_content.id') )
   country_phone_code   = Column(String(4), nullable=False, unique=True)
   
   athletes             = relationship('Athletes', backref='countries')
   phones               = relationship('Phones', back_populates='countries', cascade='all, delete')



## * ------------------- PHONE MODEL ------------------- ##
class Phones(Base):
   __tablename__         = 'phones'

   athlete_id            = Column(Integer, ForeignKey('athletes.id'), primary_key=True)
   phone_country_code    = Column(String(4), ForeignKey('countries.country_phone_code'), primary_key=True)
   phone_number          = Column(String(15), primary_key=True)
   
   athletes              = relationship('Athletes', backref='document_number', cascade='all, delete')



## * ------------------- LANGUAGES MODEL ------------------- ##
class Languages(Base):
    __tablename__        = 'languages'
    
    code                 = Column(String(3), primary_key=True)
    language_name        = Column(String(25))
    
    text_content_id      = relationship('Text_Context')
    translations_id      = relationship('Translations')
    


## * ------------------- TRANSLATIONS MODEL ------------------- ##
class Translations(Base):
    __tablename__        = 'translations'
    
    text_content_id      = Column(BigInteger, ForeignKey('text_content.id') , primary_key=True)
    language_code        = Column(String(3), ForeignKey('languages.code'), primary_key=True)
    translation          = Column(String(200), nullable=False)
    
    
    
## * ------------------- TEXT CONTENT MODEL ------------------- ##   
class Text_Content(Base):
    __tablename__        = 'text_content'
    
    id                   = Column(BigInteger, primary_key=True)
    original_text        = Column(String(200), nullable=False)
    original_language    = Column(String(3), ForeignKey('languages.code'), nullable=False)
    table_name           = Column(String(30), nullable=False)
    
    translations_code    = relationship('Translations', cascade='all', backref='text_content')
    countries            = relationship('Countries', cascade='all, delete', backref='text_content')
    
    
    