import unittest
from common.models import *

class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.list = list()
        self.list.append(Category.objects.create(name="Kernel"))
        self.list.append(Category.objects.create(name="GUI"))
        

    def testSpeaking(self):
        for cat in list:
            Category.save(cat)
