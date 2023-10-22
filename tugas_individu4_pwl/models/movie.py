from sqlalchemy import Column, Integer, Text, Float
from .meta import Base

class Movie(Base):
    """ The SQLAlchemy declarative model class for a Movie object. """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    language = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)

    def to_dict(self):
        """ Return a dictionary representation of a Movie object. """
        return {
            'id': self.id,
            'title': self.title,
            'language': self.language,
            'status': self.status,
            'rating': self.rating,
        }