from .models import MasUser
from haystack import indexes


class MasUserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,
                             use_template=True)
    nick_name = indexes.CharField(model_attr='nick_name')

    def get_model(self):
        return MasUser

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
