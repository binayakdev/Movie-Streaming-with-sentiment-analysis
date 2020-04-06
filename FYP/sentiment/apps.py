from django.apps import AppConfig
from django.conf import settings
import os
import pickle

class SentimentConfig(AppConfig):
    name = 'sentiment'

    #create path to models
    path = os.path.join(settings.MODEL, 'SVM.sav')

    # load models into separate variables
    # these will be accessible via this class
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled)

    estimator = data