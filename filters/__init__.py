from loader import dp
from .chapter import Chapter
from .test import Test
from .question import Question

if __name__ == 'filters':
    dp.filters_factory.bind(Chapter)
    dp.filters_factory.bind(Test)
    dp.filters_factory.bind(Question)
