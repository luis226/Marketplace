from django.test import TestCase

# Create your tests here.
class MyTestCase(TestCase):
    def test_my_test(self):
        pass

    def test_failing_test(self):
        self.assertTrue(False)