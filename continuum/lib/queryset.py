'''manager method to be able to chain custom queries'''
from django.db import models

class MixinManager(models.Manager):
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', 'Model')
        mixins = kwargs.pop('mixins', []) # this should be a list of QuerySet subclasses, or object subclasses

        super(MixinManager, self).__init__(*args, **kwargs)

        self.qs_class = type(
            '%sQuerySet' % name,
            (models.query.QuerySet,) + mixins,
            {}
        )

    def get_query_set(self):
        return self.qs_class(self.model)

    def __getattr__(self, attr):
        return getattr(self.get_query_set(), attr)
