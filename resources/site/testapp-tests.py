from django.test import TestCase
from testapp.models import TestModel

class TestCase(TestCase):
    def setUp(self):
        TestModel.objects.create(address="123 Fake St", state="AK", zip_code=99701)

    def test_f(self):
        record = TestModel.objects.get(address="123 Fake St", state="AK", zip_code=99701)
        self.assertEqual(record.zip_code, 99701)

