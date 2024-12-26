from django.test import TestCase

from django.test import TestCase
from django.urls import reverse


class SampleViewTest(TestCase):
    def test_sample_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello, world!")
