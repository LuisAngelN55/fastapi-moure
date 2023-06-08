from sqlalchemy import Column, Integer, String
from .declarative_base import Base
from sqlalchemy.orm import relationship
from .albumcancion import AlbumCancion



class Cancion(Base):
    __tablename__ = 'cancion'
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    minutos = Column(Integer)
    segundos = Column(Integer)
    compositor = Column(String)
    
    albumes = relationship('Album', secondary='album_cancion')
    interpretes = relationship('Interprete')