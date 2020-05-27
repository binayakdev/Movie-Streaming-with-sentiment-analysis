from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sentiment.views import analysis


class TestUrls(SimpleTestCase):

    def test_sentiment_analysis_url_is_resolved(self):
        print("\nTesting the URL in the sentiment app..\n")
        url = reverse('analysis', args=[1])
        self.assertEquals(resolve(url).func, analysis)
