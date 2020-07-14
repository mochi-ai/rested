from django.test import TestCase
from api.models import Question


class AnimalTestCase(TestCase):
    def setUp(self):
        Question.objects.create(question_text="lion")
        Question.objects.create(question_text="cat")

    def test_animals_can_speak(self):
        self.assertEqual(Question.objects.count(), 2)
