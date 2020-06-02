from django.test import SimpleTestCase
from sentiment.views import predict, classify_entity
from collections import defaultdict


class SentimentModule(SimpleTestCase):

    def test_predict_function(self):
        print("\nTesting the predict function..\n")

        test_review = [
            'I loved this movie. It is the best one I have watched so far!!']
        test_review_sentiment = 'positive'

        test_review_result = predict(test_review)[0]
        print(test_review_result)

        self.assertEquals(test_review_result, test_review_sentiment)

    def test_entity_classfier_function(self):
        print("\nTesting the entity classifier..\n")

        test_text = ["Chris lives in California"]

        for text in test_text:
            print(text)

        entity = defaultdict(set)
        entity['PERSON'] = {"Chris"}
        entity['LOCATION'] = {'California'}

        entity_classifier_result = classify_entity(test_text)

        print(entity_classifier_result)

        self.assertDictEqual(entity_classifier_result, entity)


