from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Sequence

from ..base import Base


class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, Sequence('chapter_id_seq'), primary_key=True)
    name = Column(String)

    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<Chapter {self.name}>'
