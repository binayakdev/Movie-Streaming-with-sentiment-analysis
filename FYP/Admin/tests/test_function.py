from django.test import SimpleTestCase
import datetime
from Admin.templatetags.timetags import timestamp


class TemplateTest(SimpleTestCase):

    # Testing the helper function (template tag) that converts unix time stamp to python datetime
    def test_templatetag_timestamp(self):
        print("\nTesting the timestamp function...\n")
        result = timestamp('1583575379')  # Unix timestamp
        test_date = datetime.datetime(2020, 3, 7, 15, 47, 59)  # datetime

        self.assertEquals(result, test_date)
