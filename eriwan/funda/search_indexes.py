from haystack.indexes import *
from haystack import site
from funda.models import Question, Answer

class QuestionIndex(SearchIndex):
  text= CharField(document=True, use_template=True)

  def index_queryset(self):
    return Question.objects.all()


site.register(Question,QuestionIndex)
