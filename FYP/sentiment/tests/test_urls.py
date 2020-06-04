from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sentiment.views import analysis


#  This test checks of the URL routes can be resolved to their corresponding view functions.
class TestUrls(SimpleTestCase):

    def test_sentiment_analysis_url_is_resolved(self):
        print("\nTesting the URL in the sentiment app..\n")
        url = reverse('analysis', args=[1])
        self.assertEquals(resolve(url).func, analysis)
