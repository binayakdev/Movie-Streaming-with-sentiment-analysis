from django.test import SimpleTestCase
import datetime
from sentiment.templatetags.money import millify


class TemplateTest(SimpleTestCase):

    # This function tests if the template tag can convert amount in digits to words.
    def test_templatetag_millify(self):
        result = millify(855013954)  # 855 million in numbers
        test_amount = '855 Million'

        print("855013954 => " + test_amount)
        self.assertEquals(result, test_amount)
