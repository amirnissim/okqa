import datetime
from haystack import indexes
from models import Question, Answer

class AnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    created_at = indexes.DateTimeField(model_attr='created_at')
    place = indexes.CharField(model_attr='question__entity__slug')

    def get_model(self):
        return Answer

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # text = indexes.CharField(model_attr='subject')
    author = indexes.CharField(model_attr='author')
    created_at = indexes.DateTimeField(model_attr='created_at')
    place = indexes.CharField(model_attr='entity__slug')

    def get_model(self):
        return Question

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

