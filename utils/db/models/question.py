from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Sequence, Boolean

from ..base import Base


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    question_image = Column(String)
    question = Column(String)

    explanation_image = Column(String)
    explanation = Column(String)

    has_answer = Column(Boolean)

    type = Column(String)

    test_type = Column(String)
    answer_test = Column(String)

    input_count = Column(Integer)
    answer1 = Column(String)
    answer2 = Column(String)

    test_id = Column(Integer)

    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<Questions {self.id}>'
