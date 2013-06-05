from django.test import TestCase, RequestFactory
from milkman.dairy import milkman


class BaseTest(TestCase):
    '''base for all tests'''
    factory = RequestFactory()

    def deliver(self, *args, **kwargs):
        obj = milkman.deliver(*args, **kwargs)
        self.addCleanup(obj.delete)
        return obj
