from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from io import BytesIO
import base64
import tweepy
import re
import os
import math
import concurrent.futures
from collections import defaultdict
import requests
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .apps import SentimentConfig
from movietime.views import user_login_required
from movietime.models import Movie
from UserSettings.models import UserSubscription, Profile

# importing necessary libraries for data pre-processing
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from nltk.tag import StanfordNERTagger

# Create your views here.


def subscription_required(f):
    def wrap(request, *args, **kwargs):
        # This check the session if the userid key exists, if not it will redirect to login page
        if '_auth_user_id' not in request.session.keys():
            print("Session???")
            return redirect('login')

        user = Profile.objects.get(id=request.user.id)
        subscribed = UserSubscription.objects.filter(user=user).exists()

        if subscribed == False:
            messages.info(request, 'You have no subscription.',
                          extra_tags="Oh Snap! You need to upgrade your account to perform Sentiment Analysis.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            subscription = UserSubscription.objects.get(user=user)
            if subscription.active == 0:
                messages.info(request, 'You need to activate your subscription',
                              extra_tags="Oh Snap! You need to activate your account to perform Sentiment Analysis.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


@user_login_required
def index(request):
    return render(request, 'sentiment.html')


'''
This class creates the basic pipeline for the text pre-processing
It has the following steps in the pipeline:
1. Removing html from the text
2. Removing punctuation, user tags, emails, etc.
3. Removing numbers
4. Removing stop words (the, it, make, most, etc..)
5. Lemmatizing the texts
6. Generating word cloud
'''


class TextPreprocessor:

    def remove_html(text):
        soup = BeautifulSoup(text, 'lxml')
        html_free = soup.get_text(separator=' ')
        return html_free

    def remove_noise(text):
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub('@[^\s]+', 'USER', text)
        text = text.lower().replace("ё", "е")
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        return text.strip()

    def remove_numbers(text):
        result = ''.join(i for i in text if not i.isdigit())
        return result

    def remove_stopwords(text):
        stop_words = stopwords.words('english')
        stopwords_dict = Counter(stop_words)
        words = ' '.join([w for w in text.split() if w not in stopwords_dict])
        return words

    def word_lemmatizer(text):
        lemmatizer = WordNetLemmatizer()  # Instantiate lemmatizer
        lem_text = ' '.join([lemmatizer.lemmatize(i) for i in text.split()])
        return lem_text

    def generate_wordcloud(reviews):
        text = " ".join(text for text in reviews)

        # create stopword list
        stopwords = set(STOPWORDS)

        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords,
                              background_color="white").generate(text)
        plt.figure(figsize=(20, 10))
        # bilinear interpolation makes the edges of the image sharp
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        return graphic


# This functions uses the machine learning model to predict the sentiment in texts
# It returns the predicted classes, wordcloud and prediction porbabilities
def predict(reviews):
    data = pd.DataFrame(reviews, columns=['reviews'])
    # data['reviews'] = data['reviews'].apply(lambda x: TextPreprocessor.remove_html(x))
    data['reviews'] = data['reviews'].apply(
        lambda x: TextPreprocessor.remove_noise(x))
    data['reviews'] = data['reviews'].apply(
        lambda x: TextPreprocessor.remove_numbers(x))
    wordcloud = TextPreprocessor.generate_wordcloud(data['reviews'])
    data['reviews'] = data['reviews'].apply(
        lambda x: TextPreprocessor.remove_stopwords(x))
    # data['reviews'] = data['reviews'].apply(lambda x: TextPreprocessor.word_lemmatizer(x))

    return SentimentConfig.estimator.predict(data['reviews']), wordcloud, SentimentConfig.estimator.predict_proba(data['reviews'])

# This function uses the Stanford NER tagger to classify the entities in a texts
# It returns the classified entities


def classify_entity(reviews):
    model_file = os.path.join(
        settings.MODEL, 'english.all.3class.distsim.crf.ser.gz')
    jar_file = os.path.join(settings.MODEL, 'stanford-ner.jar')

    st = StanfordNERTagger(model_file, jar_file)
    classified = []
    for review in reviews:
        classified.append(st.tag(review.split()))
    entities = defaultdict(set)
    for tag_list in classified:
        for tags in tag_list:
            if tags[1] is not 'O':
                entities[tags[1]].add(tags[0])
    return entities

# Analyzing the reviews and return result to the view
@user_login_required
@subscription_required
def analysis(request, id):
    api_key = settings.TMDB_API_KEY
    movie = Movie.objects.get(id=id)
    review_id = Movie.objects.get(id=id).review_id

    try:
        reviews_response = requests.get(
            url=f'https://api.themoviedb.org/3/movie/{review_id}/reviews?api_key={api_key}&language=en-US&page=1'
        )

        movies_response = requests.get(
            url=f'https://api.themoviedb.org/3/movie/{review_id}?api_key={api_key}&language=en-US'
        )
    except requests.exceptions.RequestException as e:
        messages.info(
            request, "Internal Server Error! Sorry, cannot perform sentiment analysis. Check your internet or try again later.", extra_tags="Error")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    tmd_movies = movies_response.json()  # Get the movies
    # Get all the reviews along with the extra information
    reviews_expanded = reviews_response.json().get('results')
    reviews = [results.get('content')
               for results in reviews_expanded]  # Get only the reviews
    reviews_count = len(reviews)  # Count the number of reviews

    if reviews:
        prediction, wordcloud, prob = predict(reviews)
        entities = classify_entity(reviews)

        confidence = 0
        total_prob = len(prob)
        for values in prob:
            if values[0] > values[1]:
                confidence += values[0]
            else:
                confidence += values[1]
        confidence = round((confidence / total_prob) * 100, 0)
        print(confidence)

        pred_dist = Counter(prediction)
        total = pred_dist['positive'] + pred_dist['negative']
        positive = round(pred_dist['positive'] / total, 3)
        negative = round(pred_dist['negative'] / total, 3)

        sentiment_score = round(positive * 100, 0)

        context = {
            'title': 'Sentiment Analysis',
            'movie': movie,
            'tmd_movies': tmd_movies,
            'reviews': zip(reviews_expanded, prediction),
            'reviews_count': reviews_count,
            'positive': positive,
            'negative': negative,
            'wordcloud': wordcloud,
            'sentiment_score': sentiment_score,
            'confidence': confidence
        }

        for key, values in entities.items():
            context[key] = values

        return render(request, 'analysis.html', context)
    else:
        context = {
            'title': 'Sentiment Analysis',
            'movie': movie,
            'tmd_movies': tmd_movies,
        }
        return render(request, 'analysis.html', context)
