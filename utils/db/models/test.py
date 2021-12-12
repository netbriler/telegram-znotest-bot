from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Sequence

from ..base import Base


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, Sequence('test_id_seq'), primary_key=True)
    name = Column(String)

    chapter_id = Column(Integer)

    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<Test {self.name}>'
