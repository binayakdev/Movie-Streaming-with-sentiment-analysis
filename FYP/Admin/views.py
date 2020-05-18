from django.shortcuts import render, redirect
from .forms import UserAdminRegisterForm, CustomAdminChangeForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from UserSettings.models import Profile
from movietime.models import Movie
from UserSettings.models import UserSubscription, SubscriptionPlan
from django.db.models import Q
from django.conf import settings
import stripe
from stripe.api_resources.abstract import ListableAPIResource
from datetime import datetime

# Setup Stripe python client library
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def admin_login_required(f):
    def wrap(request, *args, **kwargs):
        # This check the session if the userid key exists, if not it will redirect to login page
        if '_auth_user_id' not in request.session.keys():
            print("Session???")
            return redirect('admin-login')

        if '_auth_user_id' in request.session.keys() and not request.user.is_admin:
            print("Not staff")
            return redirect('admin-login')

        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_admin == True:
            login(request, user)
            return redirect('admin-index')
        else:
            messages.warning(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('admin-login')
    else:
        form = CustomAdminChangeForm()
        return render(request, 'admin-login.html', {'form': form})


def admin_register(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.is_superuser = True
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('admin-login')
    else:
        form = UserAdminRegisterForm()
    return render(request, 'admin-register.html', {'form': form})


def give_date(unix):
    return datetime.utcfromtimestamp(int(unix)).strftime('%Y-%b-%d')


@admin_login_required
def index(request):
    context = {}

    users_count = Profile.objects.filter(is_superuser=0).count()
    movies_count = Movie.objects.all().count()
    active_count = Profile.objects.filter(
        Q(is_active=1) & Q(is_superuser=0)).count()
    active_perc = round((active_count / users_count) * 100)

    context['title'] = 'Dashboard'
    context['users_count'] = users_count
    context['movies_count'] = movies_count
    context['active_perc'] = active_perc
    try:
        stripe_balance = stripe.Balance.retrieve()
        balance = stripe_balance.available[0].amount / 100
        subscribers = UserSubscription.objects.all().count()
        subscriber_perc = round((subscribers / users_count) * 100)
        transactions = stripe.BalanceTransaction.list()

        transaction_aggr = {}
        for transaction in transactions:
            if give_date(transaction.created) in transaction_aggr.keys():
                transaction_aggr[give_date(
                    transaction.created)] += transaction.net/100
            else:
                transaction_aggr[give_date(
                    transaction.created)] = transaction.net/100
        print(transaction_aggr)

        transaction_amount = list(transaction_aggr.values())
        transaction_date = list(transaction_aggr.keys())

        context['net_amount'] = transaction_amount
        context['transaction_date'] = transaction_date
        context['balance'] = balance
        context['subscriber_perc'] = subscriber_perc

    except stripe.error.APIConnectionError as e:
        context['stripe_error'] = e
    except stripe.error.RateLimitError as e:
        context['stripe_error'] = e
    except stripe.error.AuthenticationError as e:
        context['stripe_error'] = e
    except stripe.error.StripeError as e:
        context['stripe_error'] = e

    return render(request, 'admin-panel/panel-layout.html', context)


@admin_login_required
def admin_users(request):
    users = Profile.objects.filter(is_superuser=0)

    context = {
        'title': 'Users',
        'users': users
    }

    return render(request, 'admin-panel/panel-users.html', context)


@admin_login_required
def admin_movies(request):
    movies = Movie.objects.all()

    context = {
        'title': 'Movies',
        'movies': movies
    }

    return render(request, 'admin-panel/panel-movies.html', context)


@admin_login_required
def admin_subscribers(request):
    subscribers = UserSubscription.objects.all()
    sub = [subscriber.user.id for subscriber in subscribers]
    free_users = Profile.objects.filter(
        is_superuser=False).filter(~Q(id__in=sub))
    plans = SubscriptionPlan.objects.all()
    plan = [plan.membership_type for plan in plans]
    user_count = [len(subscribers), len(free_users)]
    context = {
        'title': 'Subscription',
        'subscribers': subscribers,
        'free_users': free_users,
        'plans': plans,
        'user_count': user_count,
        'membership': plan,
    }

    return render(request, 'admin-panel/panel-subscribers.html', context)


@admin_login_required
def admin_stripe(request):
    try:
        stripe_balance = stripe.Balance.retrieve()
        balance = stripe_balance.available[0].amount / 100
        due = stripe_balance.pending[0].amount / 100
        events = stripe.Event.list()
        products = stripe.Product.list()

        context = {
            'title': 'Stripe',
            'balance': balance,
            'due': due,
            'products': products.data[0],
            'events': events.data,
        }
        return render(request, 'admin-panel/panel-stripe.html', context)
    except stripe.error.APIConnectionError as e:
        context = {}
        context['stripe_error'] = e
        return render(request, 'admin-panel/panel-stripe.html', context)
    except stripe.error.RateLimitError as e:
        context = {}
        context['stripe_error'] = e
        return render(request, 'admin-panel/panel-stripe.html', context)
    except stripe.error.AuthenticationError as e:
        context = {}
        context['stripe_error'] = e
        return render(request, 'admin-panel/panel-stripe.html', context)
    except stripe.error.StripeError as e:
        context = {}
        context['stripe_error'] = e
        return render(request, 'admin-panel/panel-stripe.html', context)
