from loader import dp
from .answer import Answer
from .chapter import Chapter
from .question import Question
from .test import Test

if __name__ == 'filters':
    dp.filters_factory.bind(Chapter)
    dp.filters_factory.bind(Test)
    dp.filters_factory.bind(Question)
    dp.filters_factory.bind(Answer)
