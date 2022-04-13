from django.test.client import Client
import unittest


class TestMicroEvidenceModel(unittest.TestCase):
    fixtures = ['fixtures/initial.json', 'fixtures/users.json']
